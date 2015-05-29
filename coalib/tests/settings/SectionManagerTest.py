import inspect
import os
import sys
import tempfile
import unittest
sys.path.insert(0, ".")

from coalib.misc.StringConstants import StringConstants
from coalib.settings.SectionManager import (gather_configuration,
                                            retrieve_logging_objects,
                                            close_objects)
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.output.ConsoleInteractor import ConsoleInteractor
from coalib.output.NullInteractor import NullInteractor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.output.printers.FilePrinter import FilePrinter
from coalib.output.printers.NullPrinter import NullPrinter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
import re


class SectionManagerTest(unittest.TestCase):
    def test_run(self):
        # We need to use a bad filename or this will parse coalas .coafile
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(
            arg_list=['-S', "test=5", "-c", "some_bad_filename"])
        close_objects(interactor, log_printer)

        self.assertEqual(str(sections["default"]),
                         "Default {config : some_bad_filename, test : 5}")

        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(
            arg_list=['-S test=5', '-c bad_filename', '-b LineCountBear'])
        close_objects(interactor, log_printer)
        self.assertEqual(len(local_bears["default"]), 1)

    def test_default_coafile_parsing(self):
        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionManagerTest)),
            "section_manager_test_files",
            "default_coafile"))
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration()
        close_objects(interactor, log_printer)
        self.assertEqual(str(sections["test"]),
                         "test {value : 1, testval : 5}")
        StringConstants.system_coafile = tmp

    def test_user_coafile_parsing(self):
        tmp = StringConstants.user_coafile
        StringConstants.user_coafile = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionManagerTest)),
            "section_manager_test_files",
            "default_coafile"))
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration()
        close_objects(interactor, log_printer)
        self.assertEqual(str(sections["test"]),
                         "test {value : 1, testval : 5}")
        StringConstants.user_coafile = tmp

    @staticmethod
    def test_nonexistent_file():
        filename = "bad.one/test\neven with bad chars in it"
        # Shouldn't throw an exception
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(arg_list=['-S',
                                                       "config=" + filename])
        close_objects(interactor, log_printer)

        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = filename
        # Shouldn't throw an exception
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration()
        close_objects(interactor, log_printer)
        StringConstants.system_coafile = tmp

    def test_merge(self):
        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionManagerTest)),
            "section_manager_test_files",
            "default_coafile"))

        config = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionManagerTest)),
            "section_manager_test_files",
            ".coafile"))
        # Check merging of default_coafile and .coafile
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(arg_list=["-c", re.escape(config)])
        close_objects(interactor, log_printer)
        self.assertEqual(str(sections["test"]),
                         "test {value : 2}")
        self.assertEqual(str(sections["test-2"]),
                         "test-2 {files : ., bears : LineCountBear}")
        # Check merging of default_coafile, .coafile and cli
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(arg_list=["-c",
                                          re.escape(config),
                                          "-S",
                                          "test.value=3",
                                          "test-2.bears=",
                                          "test-5.bears=TestBear2"])
        close_objects(interactor, log_printer)
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
         targets,
         interactor,
         log_printer) = gather_configuration(arg_list=["-S",
                                          "value=1",
                                          "test.value=2",
                                          "-c",
                                          "some_bad_file_name"])
        close_objects(interactor, log_printer)
        self.assertEqual(sections["default"],
                         sections["test"].defaults)

    def test_back_saving(self):
        filename = os.path.join(tempfile.gettempdir(),
                                "SectionManagerTestFile")

        # We need to use a bad filename or this will parse coalas .coafile
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(
            arg_list=['-S',
                      "save=" + re.escape(filename),
                      "-c=some_bad_filename"])
        close_objects(interactor, log_printer)

        with open(filename, "r") as f:
            lines = f.readlines()
        self.assertEqual(["[Default]\n", "config = some_bad_filename\n"],
                         lines)

        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(
            arg_list=['-S',
                      "save=true",
                      "config=" + re.escape(filename),
                      "test.value=5"])
        close_objects(interactor, log_printer)

        with open(filename, "r") as f:
            lines = f.readlines()
        os.remove(filename)
        self.assertEqual(["[Default]\n",
                          "config = " + filename + "\n",
                          "\n",
                          "[test]\n",
                          "value = 5\n"], lines)

    def test_logging_objects(self):
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(arg_list=['-S', "log_type=none"])
        close_objects(interactor, log_printer)
        self.assertIsInstance(log_printer, NullPrinter)

        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(arg_list=['-S', "output=none"])
        close_objects(interactor, log_printer)
        self.assertIsInstance(interactor, NullInteractor)

    def test_targets(self):
        (sections,
         local_bears,
         global_bears,
         targets,
         interactor,
         log_printer) = gather_configuration(arg_list=["default",
                                                       "test1",
                                                       "test2"])
        close_objects(interactor, log_printer)
        self.assertEqual(targets, ["default", "test1", "test2"])

    def test_outputting(self):
        interactor, log_printer = retrieve_logging_objects(Section("default"))
        self.assertIsInstance(interactor, ConsoleInteractor)
        close_objects(interactor, log_printer)

        test_section = Section("default")
        test_section.append(Setting(key="output", value="none"))
        interactor, log_printer = retrieve_logging_objects(test_section)
        self.assertIsInstance(interactor, NullInteractor)
        close_objects(interactor, log_printer)

        test_section = Section("default")
        test_section.append(Setting(key="output", value="anything else"))
        interactor, log_printer = retrieve_logging_objects(test_section)
        self.assertIsInstance(interactor, ConsoleInteractor)
        close_objects(interactor, log_printer)

    def test_logging(self):
        test_section = Section("default")
        test_section.append(Setting(key="log_TYPE", value="conSole"))
        interactor, log_printer = retrieve_logging_objects(test_section)
        self.assertIsInstance(log_printer, ConsolePrinter)
        close_objects(interactor, log_printer)

        test_section = Section("default")
        test_section.append(Setting(key="log_TYPE", value="NONE"))
        interactor, log_printer = retrieve_logging_objects(test_section)
        self.assertIsInstance(log_printer, NullPrinter)
        close_objects(interactor, log_printer)

        filename = tempfile.gettempdir() + os.path.sep + "log_test~"
        test_section = Section("default")
        test_section.append(Setting(key="log_TYPE", value=re.escape(filename)))
        interactor, log_printer = retrieve_logging_objects(test_section)
        self.assertIsInstance(log_printer, FilePrinter)
        close_objects(interactor, log_printer)
        os.remove(filename)

        test_section = Section("default")
        test_section.append(Setting(key="log_TYPE",
                                    value="./invalid path/@#$%^&*()_"))
        # Should throw a warning
        interactor, log_printer = retrieve_logging_objects(test_section)
        self.assertIsInstance(log_printer, ConsolePrinter)
        self.assertEqual(log_printer.log_level, LOG_LEVEL.WARNING)
        close_objects(interactor, log_printer)

        test_section.append(Setting(key="LOG_LEVEL", value="DEBUG"))
        # Should throw a warning
        interactor, log_printer = retrieve_logging_objects(test_section)
        self.assertEqual(log_printer.log_level, LOG_LEVEL.DEBUG)
        close_objects(interactor, log_printer)


if __name__ == '__main__':
    unittest.main(verbosity=2)
