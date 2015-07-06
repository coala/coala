import os
import sys
import tempfile
import unittest
sys.path.insert(0, ".")

from coalib.misc.StringConstants import StringConstants
from coalib.settings.ConfigurationGathering import (gather_configuration,
                                                    find_user_config)
from coalib.output.printers.NullPrinter import NullPrinter
from coalib.output.ClosableObject import close_objects
import re


class ConfigurationGatheringTest(unittest.TestCase):
    def setUp(self):
        self.log_printer = NullPrinter()

    def tearDown(self):
        close_objects(self.log_printer)

    def test_gather_configuration(self):
        # We need to use a bad filename or this will parse coalas .coafile
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=['-S', "test=5", "-c", "some_bad_filename"])

        self.assertEqual(str(sections["default"]),
                         "Default {config : some_bad_filename, test : 5}")

        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=['-S test=5', '-c bad_filename', '-b LineCountBear'])
        self.assertEqual(len(local_bears["default"]), 1)

    def test_default_coafile_parsing(self):
        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "section_manager_test_files",
            "default_coafile"))
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(lambda *args: True,
                                         self.log_printer)
        self.assertEqual(str(sections["test"]),
                         "test {value : 1, testval : 5}")
        StringConstants.system_coafile = tmp

    def test_user_coafile_parsing(self):
        tmp = StringConstants.user_coafile
        StringConstants.user_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "section_manager_test_files",
            "default_coafile"))
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(lambda *args: True,
                                         self.log_printer)
        self.assertEqual(str(sections["test"]),
                         "test {value : 1, testval : 5}")
        StringConstants.user_coafile = tmp

    def test_nonexistent_file(self):
        filename = "bad.one/test\neven with bad chars in it"
        # Shouldn't throw an exception
        gather_configuration(lambda *args: True,
                             self.log_printer,
                             arg_list=['-S', "config=" + filename])

        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = filename
        # Shouldn't throw an exception
        gather_configuration(lambda *args: True,
                             self.log_printer)
        StringConstants.system_coafile = tmp

    def test_merge(self):
        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "section_manager_test_files",
            "default_coafile"))

        config = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "section_manager_test_files",
            ".coafile"))
        # Check merging of default_coafile and .coafile
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(lambda *args: True,
                                         self.log_printer,
                                         arg_list=["-c", re.escape(config)])
        self.assertEqual(str(sections["test"]),
                         "test {value : 2}")
        self.assertEqual(str(sections["test-2"]),
                         "test-2 {files : ., bears : LineCountBear}")
        # Check merging of default_coafile, .coafile and cli
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(lambda *args: True,
                                         self.log_printer,
                                         arg_list=["-c",
                                                   re.escape(config),
                                                   "-S",
                                                   "test.value=3",
                                                   "test-2.bears=",
                                                   "test-5.bears=TestBear2"])
        self.assertEqual(str(sections["test"]), "test {value : 3}")
        self.assertEqual(str(sections["test-2"]),
                         "test-2 {files : ., bears : }")
        self.assertEqual(str(sections["test-3"]),
                         "test-3 {files : MakeFile}")
        self.assertEqual(str(sections["test-4"]),
                         "test-4 {bears : TestBear}")
        self.assertEqual(str(sections["test-5"]),
                         "test-5 {bears : TestBear2}")
        StringConstants.system_coafile = tmp

    def test_merge_defaults(self):
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=["-S", "value=1", "test.value=2", "-c", "bad_file_name"])
        self.assertEqual(sections["default"],
                         sections["test"].defaults)

    def test_back_saving(self):
        filename = os.path.join(tempfile.gettempdir(),
                                "SectionManagerTestFile")

        # We need to use a bad filename or this will parse coalas .coafile
        gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=['-S',
                      "save=" + re.escape(filename),
                      "-c=some_bad_filename"])

        with open(filename, "r") as f:
            lines = f.readlines()
        self.assertEqual(["[Default]\n", "config = some_bad_filename\n"],
                         lines)

        gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=['-S',
                      "save=true",
                      "config=" + re.escape(filename),
                      "test.value=5"])

        with open(filename, "r") as f:
            lines = f.readlines()
        os.remove(filename)
        self.assertEqual(["[Default]\n",
                          "config = " + filename + "\n",
                          "\n",
                          "[test]\n",
                          "value = 5\n"], lines)

    def test_targets(self):
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(lambda *args: True,
                                         self.log_printer,
                                         arg_list=["default",
                                                   "test1",
                                                   "test2"])
        self.assertEqual(targets, ["default", "test1", "test2"])

    def test_find_user_config(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        c_file = os.path.join(current_dir,
                              "section_manager_test_files",
                              "project",
                              "test.c")

        retval = find_user_config(c_file, 1)
        self.assertEqual("", retval)

        retval = find_user_config(c_file, 2)
        self.assertEqual(os.path.join(current_dir,
                                      "section_manager_test_files",
                                      ".coafile"), retval)


if __name__ == '__main__':
    unittest.main(verbosity=2)
