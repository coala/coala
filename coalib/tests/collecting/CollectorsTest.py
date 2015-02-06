import inspect
import os
import sys

import unittest

sys.path.insert(0, ".")
from coalib.collecting.Collectors import collect_files, collect_dirs


class CollectFilesTestCase(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                "collectors_test_dir")

    def test_file_empty(self):
        self.assertRaises(TypeError, collect_files)

    def test_file_invalid(self):
        self.assertEqual(collect_files(["invalid_path"]), [])

    def test_file_collection(self):
        self.assertEqual(collect_files([os.path.join(self.collectors_test_dir,
                                                     "others",
                                                     "*",
                                                     "*2.py")]),
                         [os.path.join(self.collectors_test_dir,
                                       "others",
                                       "py_files",
                                       "file2.py")])


class CollectDirsTestCase(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                "collectors_test_dir")

    def test_dir_empty(self):
        self.assertRaises(TypeError, collect_dirs)

    def test_dir_invalid(self):
        self.assertEqual(collect_dirs(["invalid_path"]), [])

    def test_dir_collection(self):
        self.assertEqual(
            sorted(collect_dirs([os.path.join(self.collectors_test_dir,
                                              "**")])),
            sorted([os.path.join(self.collectors_test_dir, "bears"),
                os.path.join(self.collectors_test_dir, "others"),
                os.path.join(self.collectors_test_dir, "others", "c_files"),
                os.path.join(self.collectors_test_dir, "others", "py_files"),
                self.collectors_test_dir]))


if __name__ == '__main__':
    unittest.main(verbosity=2)
