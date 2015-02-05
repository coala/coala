import os
import sys
import tempfile
import unittest

sys.path.insert(0, ".")
from coalib.collecting.Importers import import_objects
from collections import OrderedDict


class ImportObjectsTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix='coala_import_test_dir_')
        (self.testfile1, self.testfile1_path) = \
            tempfile.mkstemp(suffix='.py',
                             prefix='impobj1_',
                             dir=self.tmp_dir)
        (self.testfile2, self.testfile2_path) = \
            tempfile.mkstemp(suffix='.py',
                             prefix='impobj2_',
                             dir=self.tmp_dir)
        os.close(self.testfile1)
        os.close(self.testfile2)
        test_file_string_1 = """
class test(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    @staticmethod
    def method():
        pass

a = [1, 2, 3]
b = [1, 2, 4]

name = True
"""
        test_file_string_2 = """
from {} import test
name = False
a = test()
""".format(os.path.splitext(os.path.basename(self.testfile1_path))[0])
        with open(self.testfile1_path, 'w') as test_file_1:
            test_file_1.write(test_file_string_1)
        with open(self.testfile2_path, 'w') as test_file_2:
            test_file_2.write(test_file_string_2)

    def test_no_file(self):
        self.assertEqual(import_objects([]), [])

    def test_no_data(self):
        self.assertEqual(import_objects(self.testfile1_path), [])

    def test_name_import(self):
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               names="name")),
            2)
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               names="last_name")),
            0)

    def test_type_import(self):
        self.assertEqual(
            len(import_objects(self.testfile1_path,
                               types=list,
                               verbose=True)),
            2)
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               names="name",
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
                               attributes="method",
                               local=True,
                               verbose=True)),
            1)
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               attributes="something",
                               verbose=True)),
            0)

    def test_local_definition(self):
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               attributes="method",
                               verbose=True)),
            2)
        self.assertEqual(
            len(import_objects((self.testfile1_path, self.testfile2_path),
                               attributes="method",
                               local=True,
                               verbose=True)),
            1)
if __name__ == '__main__':
    unittest.main(verbosity=2)
