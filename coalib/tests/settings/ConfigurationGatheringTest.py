import os
import re
import tempfile
import unittest
from pyprint.NullPrinter import NullPrinter
from pyprint.ClosableObject import close_objects

from coalib.misc import Constants
from coalib.parsing.StringProcessing import escape
from coalib.settings.ConfigurationGathering import (gather_configuration,
                                                    find_user_config)
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.misc.ContextManagers import make_temp


class ConfigurationGatheringTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = LogPrinter(NullPrinter())

    def tearDown(self):
        close_objects(self.log_printer)

    def test_gather_configuration(self):
        args = (lambda *args: True, self.log_printer)

        # Passing the default coafile name only triggers a warning.
        gather_configuration(*args, arg_list=["-c abcdefghi/invalid/.coafile"])

        # Using a bad filename explicitly exits coala.
        with self.assertRaises(SystemExit):
            gather_configuration(
                *args,
                arg_list=["-S", "test=5", "-c", "some_bad_filename"])

        with make_temp() as temporary:
            sections, local_bears, global_bears, targets = (
                gather_configuration(
                    *args,
                    arg_list=["-S",
                              "test=5",
                              "-c",
                              escape(temporary, "\\"),
                              "-s"]))

        self.assertEqual(str(sections["default"]),
                         "Default {config : " + repr(temporary) + ", save : "
                         "'True', test : '5'}")

        with make_temp() as temporary:
            sections, local_bears, global_bears, targets = (
                gather_configuration(*args,
                                     arg_list=["-S test=5",
                                               "-c " + escape(temporary, "\\"),
                                               "-b LineCountBear -s"]))

        self.assertEqual(len(local_bears["default"]), 0)

    def test_default_coafile_parsing(self):
        tmp = Constants.system_coafile

        Constants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "section_manager_test_files",
            "default_coafile"))

        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=[])

        self.assertEqual(str(sections["test"]),
                         "test {value : '1', testval : '5'}")

        Constants.system_coafile = tmp

    def test_user_coafile_parsing(self):
        tmp = Constants.user_coafile

        Constants.user_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "section_manager_test_files",
            "default_coafile"))

        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=[])

        self.assertEqual(str(sections["test"]),
                         "test {value : '1', testval : '5'}")

        Constants.user_coafile = tmp

    def test_nonexistent_file(self):
        filename = "bad.one/test\neven with bad chars in it"
        with self.assertRaises(SystemExit):
            gather_configuration(lambda *args: True,
                                 self.log_printer,
                                 arg_list=['-S', "config=" + filename])

        tmp = Constants.system_coafile
        Constants.system_coafile = filename

        with self.assertRaises(SystemExit):
            gather_configuration(lambda *args: True,
                                 self.log_printer,
                                 arg_list=[])

        Constants.system_coafile = tmp

    def test_merge(self):
        tmp = Constants.system_coafile
        Constants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "section_manager_test_files",
            "default_coafile"))

        config = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "section_manager_test_files",
            ".coafile"))

        # Check merging of default_coafile and .coafile
        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=["-c", re.escape(config)])

        self.assertEqual(str(sections["test"]),
                         "test {value : '2'}")
        self.assertEqual(str(sections["test-2"]),
                         "test-2 {files : '.', bears : 'LineCountBear'}")

        # Check merging of default_coafile, .coafile and cli
        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=["-c",
                      re.escape(config),
                      "-S",
                      "test.value=3",
                      "test-2.bears=",
                      "test-5.bears=TestBear2"])

        self.assertEqual(str(sections["test"]), "test {value : '3'}")
        self.assertEqual(str(sections["test-2"]),
                         "test-2 {files : '.', bears : ''}")
        self.assertEqual(str(sections["test-3"]),
                         "test-3 {files : 'MakeFile'}")
        self.assertEqual(str(sections["test-4"]),
                         "test-4 {bears : 'TestBear'}")
        self.assertEqual(str(sections["test-5"]),
                         "test-5 {bears : 'TestBear2'}")

        Constants.system_coafile = tmp

    def test_merge_defaults(self):
        with make_temp() as temporary:
            sections, local_bears, global_bears, targets = (
                gather_configuration(lambda *args: True,
                                     self.log_printer,
                                     arg_list=["-S",
                                               "value=1",
                                               "test.value=2",
                                               "-c",
                                               escape(temporary, "\\")]))

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
        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=["default", "test1", "test2"])

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

        sections, dummy, dummy, dummy = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=["--find-config"])

        self.assertRegex(str(sections["default"]),
                         ".*find_config : 'True'.*, config : '.*'")


if __name__ == '__main__':
    unittest.main(verbosity=2)
