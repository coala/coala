import os
import sys
import unittest
from mock import patch
from collections import OrderedDict

from importlib.machinery import (
    ModuleSpec,
    SourceFileLoader,
)
from inspect import isclass

from coalib.collecting.Importers import import_objects


class ImportObjectsTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.test_dir = os.path.join(current_dir, 'importers_test_dir')
        self.testfile1_path = os.path.join(self.test_dir,
                                           'file_one.py')
        self.testfile2_path = os.path.join(self.test_dir,
                                           'file_two.py')

    def check_imported_file_one_test(self, obj):
        self.assertTrue(isclass(obj))

        self.assertEqual(obj.__name__, 'test')
        self.assertEqual(obj.__module__, 'file_one')

        instance = obj()
        self.assertIsInstance(instance, list)

    def test_no_file(self):
        self.assertEqual(import_objects([]), [])

    def test_file_one_internal_structure(self):
        objs = import_objects(self.testfile1_path)
        self.assertIsInstance(objs, list)
        self.assertEqual(len(objs), 12)

        # [0] is the module __dict__
        self.assertIsInstance(objs[0], dict)
        self.assertIn('__name__', objs[0])
        self.assertEqual(objs[0]['__name__'], 'builtins')
        self.assertIn('copyright', objs[0])
        # [1] is full filename
        self.assertIsInstance(objs[1], str)
        self.assertTrue(objs[1].endswith('.pyc'))
        self.assertTrue(objs[1].startswith(self.test_dir))
        # [2] is __doc__
        self.assertIsNone(objs[2])
        # [3] is the filename
        self.assertIsInstance(objs[3], str)
        self.assertEqual(objs[3], self.testfile1_path)
        # [4] is the loader
        self.assertIsInstance(objs[4], SourceFileLoader)
        # [5] is the module name
        self.assertIsInstance(objs[5], str)
        self.assertEqual(objs[5], 'file_one')
        # [6] is the package name
        self.assertIsInstance(objs[6], str)
        self.assertEqual(objs[6], '')
        # [7] is the module spec object
        self.assertIsInstance(objs[7], ModuleSpec)
        # [8] and [9] are module members 'a' and 'b'
        self.assertIsInstance(objs[8], list)
        self.assertEqual(objs[8], [1, 2, 3])
        self.assertIsInstance(objs[9], list)
        self.assertEqual(objs[9], [1, 2, 4])
        # [10] is the module member 'name'
        self.assertIsInstance(objs[10], bool)
        self.assertIs(objs[10], True)
        # [11] is the module member 'test'
        self.check_imported_file_one_test(objs[11])

    def test_name_import(self):
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               names='name')),
            2)
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               names='last_name')),
            0)

    def test_type_import(self):
        objs = import_objects(self.testfile1_path, types=list, verbose=True)
        self.assertEqual(len(objs), 2)
        self.assertIsInstance(objs[0], list)
        self.assertEqual(objs[0], [1, 2, 3])
        self.assertIsInstance(objs[1], list)
        self.assertEqual(objs[1], [1, 2, 4])

        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               names='name',
                               types=OrderedDict,
                               verbose=True)),
            0)

    def test_class_import(self):
        objs = import_objects((self.testfile1_path, self.testfile2_path),
                              supers=list, verbose=True)
        self.assertEqual(len(objs), 1)
        self.check_imported_file_one_test(objs[0])

        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               supers=str,
                               verbose=True)),
            0)

    def test_attribute_import(self):
        objs = import_objects((self.testfile1_path, self.testfile2_path),
                              attributes='method',
                              local=True,
                              verbose=True)
        self.assertEqual(len(objs), 1)
        self.check_imported_file_one_test(objs[0])

        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               attributes='something',
                               verbose=True)),
            0)

    def test_local_definition(self):
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               attributes='method',
                               verbose=True)),
            2)
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               attributes='method',
                               local=True,
                               verbose=True)),
            1)

    def test_invalid_file(self):
        with self.assertRaises(ImportError):
            import_objects('some/invalid/path',
                           attributes='method',
                           local=True,
                           verbose=True)

        with self.assertRaises(ImportError):
            import_objects('some/invalid/path',
                           attributes='method',
                           local=True,
                           verbose=False)

    def test_clean_sys_path(self):
        with patch.object(sys, 'path', ['/dir1']):
            import_objects(self.testfile1_path)
            self.assertEqual(sys.path, ['/dir1'])
