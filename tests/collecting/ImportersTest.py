import os
import unittest
from collections import OrderedDict

from coalib.collecting.Importers import _import_module, import_objects


class ImportModuleTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.dirname(os.path.relpath(__file__, '.'))
        self.non_existing_path = os.path.join(current_dir,
                                              'importers_test_dir',
                                              'non_existing.py')
        self.non_python_path = os.path.join(current_dir,
                                            'importers_test_dir',
                                            'test.nonpy')

    def test_non_existing(self):
        with self.assertRaisesRegex(ImportError, (
                r"^can't import non-existing file '{}'$"
                .format(os.path.realpath(self.non_existing_path)
                        # make Windows paths work
                        .replace('\\', r'\\\\')))):
            _import_module(self.non_existing_path)

    def test_non_python(self):
        with self.assertRaisesRegex(ImportError, (
                r"^'{}' doesn't seem to be a python module$"
                .format(os.path.realpath(self.non_python_path)
                        # make Windows paths work
                        .replace('\\', r'\\\\')))):
            _import_module(self.non_python_path)


class ImportObjectsTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.testfile1_path = os.path.join(current_dir,
                                           'importers_test_dir',
                                           'file_one.py')
        self.testfile2_path = os.path.join(current_dir,
                                           'importers_test_dir',
                                           'file_two.py')

    def test_no_file(self):
        self.assertEqual(import_objects([]), [])

    def test_no_data(self):
        self.assertEqual(len(import_objects(self.testfile1_path)), 12)

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
        self.assertEqual(
            len(import_objects(self.testfile1_path,
                               types=list,
                               verbose=True)),
            2)
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               names='name',
                               types=OrderedDict,
                               verbose=True)),
            0)

    def test_class_import(self):
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               supers=list,
                               verbose=True)),
            1)
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               supers=str,
                               verbose=True)),
            0)

    def test_attribute_import(self):
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               attributes='method',
                               local=True,
                               verbose=True)),
            1)
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
