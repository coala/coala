import inspect
import os
import sys
import tempfile
import unittest
sys.path.insert(0, ".")

from coalib.misc.StringConstants import StringConstants
from coalib.settings.SectionManager import SectionManager
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.output.ConsoleInteractor import ConsoleInteractor
from coalib.output.NullInteractor import NullInteractor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.output.printers.FilePrinter import FilePrinter
from coalib.output.printers.NullPrinter import NullPrinter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL


class SectionManagerTestCase(unittest.TestCase):
    def test_run(self):
        uut = SectionManager()
        # We need to use a bad filename or this will parse coalas .coafile
        results = uut.run(
            arg_list=['-S', "test=5", "-c", "some_bad_filename"])
        results[4].close()
        results[5].close()
        self.assertEqual(str(results[0]["default"]),
                         "Default {config : some_bad_filename, test : 5}")

        results = uut.run(arg_list=['-S test=5',
                                    '-c bad_filename',
                                    '-b LineCountBear'])
        results[4].close()
        results[5].close()
        self.assertEqual(len(results[1]["default"]), 1)

    def test_default_coafile_parsing(self):
        uut = SectionManager()
        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionManagerTestCase)),
            "section_manager_test_files",
            "default_coafile"))

        results = uut.run()
        results[4].close()
        results[5].close()

        results = uut.run()
        results[4].close()
        results[5].close()

        conf_sections = uut.default_sections
        self.assertEqual(str(conf_sections["test"]), "test {value : 1, "
                                                     "testval : 5}")
        StringConstants.system_coafile = tmp

    def test_user_coafile_parsing(self):
        uut = SectionManager()
        tmp = StringConstants.user_coafile
        StringConstants.user_coafile = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionManagerTestCase)),
            "section_manager_test_files",
            "default_coafile"))

        results = uut.run()
        results[4].close()
        results[5].close()

        conf_sections = uut.default_sections
        self.assertEqual(str(conf_sections["test"]),
                         "test {value : 1, testval : 5}")
        StringConstants.user_coafile = tmp

    @staticmethod
    def test_nonexistent_file():
        filename = "bad.one/test\neven with bad chars in it"
        # Shouldn't throw an exception
        results = SectionManager().run(arg_list=['-S', "config=" + filename])
        results[4].close()
        results[5].close()

        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = filename
        # Shouldn't throw an exception
        results = SectionManager().run()
        results[4].close()
        results[5].close()
        StringConstants.system_coafile = tmp

    def test_merge(self):
        uut = SectionManager()
        tmp = StringConstants.system_coafile
        StringConstants.system_coafile=os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionManagerTestCase)),
            "section_manager_test_files",
            "default_coafile"))

        config = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionManagerTestCase)),
            "section_manager_test_files",
            ".coafile"))
        # Check merging of default_coafile and .coafile
        results = uut.run(arg_list=["-c", config])
        conf_sections = results[0]
        results[4].close()
        results[5].close()

        self.assertEqual(str(conf_sections["test"]),
                         "test {value : 2}")
        self.assertEqual(str(conf_sections["test-2"]),
                         "test-2 {files : ., bears : LineCountBear}")
        # Check merging of default_coafile, .coafile and cli
        results = uut.run(arg_list=["-c",
                                    config,
                                    "-S",
                                    "test.value=3",
                                    "test-2.bears=",
                                    "test-5.bears=TestBear2"])
        conf_sections = results[0]
        results[4].close()
        results[5].close()

        self.assertEqual(str(conf_sections["test"]), "test {value : 3}")
        self.assertEqual(str(conf_sections["test-2"]),
                         "test-2 {files : ., bears : }")
        self.assertEqual(str(conf_sections["test-3"]),
                         "test-3 {files : MakeFile}")
        self.assertEqual(str(conf_sections["test-4"]),
                         "test-4 {bears : TestBear}")
        self.assertEqual(str(conf_sections["test-5"]),
                         "test-5 {bears : TestBear2}")
        StringConstants.system_coafile = tmp

    def test_merge_defaults(self):
        uut = SectionManager()
        results = uut.run(arg_list=["-S",
                                    "value=1",
                                    "test.value=2",
                                    "-c",
                                    "some_bad_file_name"])
        conf_sections = results[0]
        results[4].close()
        results[5].close()
        self.assertEqual(conf_sections["default"],
                         conf_sections["test"].defaults)

    def test_back_saving(self):
        filename = os.path.join(tempfile.gettempdir(),
                                "SectionManagerTestFile")

        # We need to use a bad filename or this will parse coalas .coafile
        results = SectionManager().run(
            arg_list=['-S', "save=" + filename, "-c", "some_bad_filename"])
        results[4].close()
        results[5].close()

        with open(filename, "r") as f:
            lines = f.readlines()
        self.assertEqual(["[Default]\n", "config = some_bad_filename\n"],
                         lines)

        results = SectionManager().run(
            arg_list=['-S', "save=true", "config=" + filename, "test.value=5"])
        results[4].close()
        results[5].close()

        with open(filename, "r") as f:
            lines = f.readlines()
        os.remove(filename)
        self.assertEqual(["[Default]\n",
                          "config = " + filename + "\n",
                          "\n",
                          "[test]\n",
                          "value = 5\n"], lines)

    def test_logging_objects(self):
        results = SectionManager().run(arg_list=['--log-type',
                                                 "none",
                                                 "--output",
                                                 "none"])
        self.assertIsInstance(results[5], NullPrinter)
        self.assertIsInstance(results[4], NullInteractor)
        results[4].close()
        results[5].close()

    def test_targets(self):
        results = SectionManager().run(arg_list=["default",
                                                 "test1",
                                                 "test2"])
        results[4].close()
        results[5].close()
        self.assertEqual(results[3], ["default", "test1", "test2"])

    def test_outputting(self):
        uut = SectionManager()
        uut.retrieve_logging_objects(Section("default"))
        self.assertIsInstance(uut.interactor, ConsoleInteractor)

        test_section = Section("default")
        test_section.append(Setting(key="output", value="none"))
        uut.retrieve_logging_objects(test_section)
        self.assertIsInstance(uut.interactor, NullInteractor)

        test_section = Section("default")
        test_section.append(Setting(key="output", value="anything else"))
        uut.retrieve_logging_objects(test_section)
        self.assertIsInstance(uut.interactor, ConsoleInteractor)

    def test_logging(self):
        uut = SectionManager()
        test_section = Section("default")
        test_section.append(Setting(key="log_TYPE", value="conSole"))
        uut.retrieve_logging_objects(test_section)
        self.assertIsInstance(uut.log_printer, ConsolePrinter)

        test_section = Section("default")
        test_section.append(Setting(key="log_TYPE", value="NONE"))
        uut.retrieve_logging_objects(test_section)
        self.assertIsInstance(uut.log_printer, NullPrinter)

        test_section = Section("default")
        test_section.append(Setting(key="log_TYPE",
                                    value="./invalid path/@#$%^&*()_"))
        uut.retrieve_logging_objects(test_section)  # Should throw a warning
        self.assertIsInstance(uut.log_printer, ConsolePrinter)
        self.assertEqual(uut.log_printer.log_level, LOG_LEVEL.WARNING)
        test_section.append(Setting(key="LOG_LEVEL", value="DEBUG"))
        uut.retrieve_logging_objects(test_section)  # Should throw a warning
        self.assertEqual(uut.log_printer.log_level, LOG_LEVEL.DEBUG)

        filename = tempfile.gettempdir() + os.path.sep + "log_test~"
        test_section = Section("default")
        test_section.append(Setting(key="log_TYPE", value=filename))
        uut.retrieve_logging_objects(test_section)
        self.assertIsInstance(uut.log_printer, FilePrinter)
        os.remove(filename)


if __name__ == '__main__':
    unittest.main(verbosity=2)
