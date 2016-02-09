import os
import unittest
from pyprint.ConsolePrinter import ConsolePrinter

from coalib.output.printers.LogPrinter import LogPrinter
from coalib.collecting.Collectors import (collect_files,
                                          collect_dirs,
                                          collect_bears)


class CollectFilesTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
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
                         [os.path.normcase(os.path.join(
                             self.collectors_test_dir,
                             "others",
                             "py_files",
                             "file2.py"))])

    def test_file_string_collection(self):
        self.assertEqual(collect_files(os.path.join(self.collectors_test_dir,
                                                    "others",
                                                    "*",
                                                    "*2.py")),
                         [os.path.normcase(os.path.join(
                             self.collectors_test_dir,
                             "others",
                             "py_files",
                             "file2.py"))])

    def test_ignored(self):
        self.assertEqual(collect_files([os.path.join(self.collectors_test_dir,
                                                     "others",
                                                     "*",
                                                     "*2.py"),
                                        os.path.join(self.collectors_test_dir,
                                                     "others",
                                                     "*",
                                                     "*2.py")],
                                       [os.path.join(self.collectors_test_dir,
                                                     "others",
                                                     "py_files",
                                                     "file2.py")]),
                         [])

    def test_limited(self):
        self.assertEqual(
            collect_files([os.path.join(self.collectors_test_dir,
                                        "others",
                                        "*",
                                        "*py")],
                          limit_file_paths=[os.path.join(
                                                self.collectors_test_dir,
                                                "others",
                                                "*",
                                                "*2.py")]),
            [os.path.normcase(os.path.join(self.collectors_test_dir,
                                           "others",
                                           "py_files",
                                           "file2.py"))])


class CollectDirsTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                "collectors_test_dir")

    def test_dir_empty(self):
        self.assertRaises(TypeError, collect_dirs)

    def test_dir_invalid(self):
        self.assertEqual(collect_dirs(["invalid_path"]), [])

    def test_dir_collection(self):
        self.assertEqual(
            sorted(i for i in
                   collect_dirs([os.path.join(self.collectors_test_dir,
                                              "**")])
                   if "__pycache__" not in i),
            sorted([os.path.normcase(os.path.join(
                self.collectors_test_dir, "bears")),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              "others")),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              "others",
                                              "c_files")),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              "others",
                                              "py_files")),
                os.path.normcase(self.collectors_test_dir+os.sep)]))

    def test_dir_string_collection(self):
        self.assertEqual(
            sorted(i for i in
                   collect_dirs(os.path.join(self.collectors_test_dir,
                                             "**"))
                   if "__pycache__" not in i),
            sorted([os.path.normcase(os.path.join(
                self.collectors_test_dir, "bears")),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              "others")),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              "others",
                                              "c_files")),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              "others",
                                              "py_files")),
                os.path.normcase(self.collectors_test_dir+os.sep)]))

    def test_ignored(self):
        self.assertEqual(
            sorted(i for i in
                   collect_dirs([os.path.join(self.collectors_test_dir,
                                              "**")],
                                [os.path.normcase(os.path.join(
                                    self.collectors_test_dir,
                                    "others",
                                    "py_files"))])
                   if "__pycache__" not in i),

            sorted([os.path.normcase(os.path.join(
                self.collectors_test_dir, "bears")),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              "others")),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              "others",
                                              "c_files")),
                os.path.normcase(self.collectors_test_dir+os.sep)]))


class CollectBearsTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                "collectors_test_dir")

        self.log_printer = LogPrinter(ConsolePrinter())

    def test_bear_empty(self):
        self.assertRaises(TypeError, collect_bears)

    def test_bear_invalid(self):
        self.assertEqual(collect_bears(["invalid_paths"],
                                       ["invalid_name"],
                                       ["invalid kind"],
                                       self.log_printer), [])

    def test_simple_single(self):
        self.assertEqual(len(collect_bears(
            [os.path.join(self.collectors_test_dir, "bears")],
            ["bear1"],
            ["kind"],
            self.log_printer)), 1)

    def test_string_single(self):
        self.assertEqual(len(collect_bears(
            os.path.join(self.collectors_test_dir, "bears"),
            ["bear1"],
            ["kind"],
            self.log_printer)), 1)

    def test_reference_single(self):
        self.assertEqual(len(collect_bears(
            [os.path.join(self.collectors_test_dir, "bears")],
            ["metabear"],
            ["kind"],
            self.log_printer)), 1)

    def test_no_duplications(self):
        self.assertEqual(len(collect_bears(
            [os.path.join(self.collectors_test_dir, "bears", "**")],
            ["*"],
            ["kind"],
            self.log_printer)), 2)

    def test_wrong_kind(self):
        self.assertEqual(len(collect_bears(
            [os.path.join(self.collectors_test_dir, "bears", "**")],
            ["*"],
            ["other_kind"],
            self.log_printer)), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
