import inspect
import os
import sys

import unittest

sys.path.insert(0, ".")
from coalib.collecting.Importers import import_objects
from collections import OrderedDict


class ImportObjectsTestCase(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        self.testfile1_path = os.path.join(current_dir,
                                           "importers_test_dir",
                                           "file_one.py")
        self.testfile2_path = os.path.join(current_dir,
                                           "importers_test_dir",
                                           "file_two.py")

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
    def test_invalid_file(self):
        self.assertEqual(
            len(import_objects("some/invalid/path",
                               attributes="method",
                               local=True,
                               verbose=True)),
            0)
        self.assertEqual(
            len(import_objects("some/invalid/path",
                               attributes="method",
                               local=True,
                               verbose=False)),
            0)
if __name__ == '__main__':
    unittest.main(verbosity=2)
