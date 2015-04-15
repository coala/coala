import inspect
import os
import sys
import unittest

sys.path.insert(0, ".")
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.collecting.Collectors import collect_files, \
                                         collect_dirs, \
                                         collect_bears


class CollectFilesTestCase(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                "collectors_test_dir")
        self.log_printer = ConsolePrinter()

    def test_file_empty(self):
        self.assertRaises(TypeError, collect_files)

    def test_file_invalid(self):
        self.assertEqual(collect_files(["invalid_path"], self.log_printer), [])

    def test_expression_invalid(self):
        self.assertRaises(SystemExit, collect_files, ["**d"], self.log_printer)

    def test_file_collection(self):
        self.assertEqual(collect_files([os.path.join(self.collectors_test_dir,
                                                     "others",
                                                     "*",
                                                     "*2.py")],
                                       self.log_printer),
                         [os.path.join(self.collectors_test_dir,
                                       "others",
                                       "py_files",
                                       "file2.py")])


class CollectDirsTestCase(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                "collectors_test_dir")

        self.log_printer = ConsolePrinter()

    def test_dir_empty(self):
        self.assertRaises(TypeError, collect_dirs)

    def test_dir_invalid(self):
        self.assertEqual(collect_dirs(["invalid_path"], self.log_printer), [])

    def test_expression_invalid(self):
        self.assertRaises(SystemExit, collect_files, ["**d"], self.log_printer)

    def test_dir_collection(self):
        self.assertEqual(
            sorted(collect_dirs([os.path.join(self.collectors_test_dir,
                                              "**")],
                                self.log_printer)),
            sorted([os.path.join(self.collectors_test_dir, "bears"),
                os.path.join(self.collectors_test_dir, "bears", "__pycache__"),
                os.path.join(self.collectors_test_dir, "others"),
                os.path.join(self.collectors_test_dir, "others", "c_files"),
                os.path.join(self.collectors_test_dir, "others", "py_files"),
                self.collectors_test_dir]))


class CollectBearsTestCase(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                "collectors_test_dir")

        self.log_printer = ConsolePrinter()

    def test_bear_empty(self):
        self.assertRaises(TypeError, collect_bears)

    def test_bear_invalid(self):
        self.assertEqual(collect_bears(["invalid_paths"],
                                       ["invalid_name"],
                                       ["invalid kind"],
                                       self.log_printer), [])

    def test_expression_invalid(self):
        self.assertRaises(SystemExit, collect_files, ["**d"], self.log_printer)

    def test_simple_single(self):
        self.assertEqual(len(collect_bears(
            [os.path.join(self.collectors_test_dir, "bears")],
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
