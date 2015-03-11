import inspect
import os
import sys
import tempfile
import unittest
sys.path.insert(0, ".")

from coalib.misc.StringConstants import StringConstants
from coalib.settings.SectionManager import SectionManager
from coalib.output.printers.NullPrinter import NullPrinter


class SectionManagerTestCase(unittest.TestCase):
    def test_run(self):
        uut = SectionManager()
        # We need to use a bad filename or this will parse coalas .coafile
        conf_sections = uut.run(
            arg_list=['-S', "test=5", "-c", "some_bad_filename"])[0]

        self.assertEqual(str(conf_sections["default"]),
                         "Default {config : some_bad_filename, test : 5}")

        local_bears = uut.run(arg_list=['-S test=5',
                                        '-c bad_filename',
                                        '-b LineCountBear'])[1]
        self.assertEqual(len(local_bears["default"]), 1)

    def test_default_coafile_parsing(self):
        uut = SectionManager()
        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionManagerTestCase)),
            "section_manager_test_files",
            "default_coafile"))
        uut.run()
        conf_sections = uut.default_sections
        self.assertEqual(str(conf_sections["test"]), "test {value : 1}")
        StringConstants.system_coafile = tmp

    @staticmethod
    def test_nonexistent_file():
        filename = "bad.one/test\neven with bad chars in it"
        # Shouldn't throw an exception
        SectionManager().run(arg_list=['-S', "config=" + filename])

        tmp = StringConstants.system_coafile
        StringConstants.system_coafile = filename
        # Shouldn't throw an exception
        SectionManager().run()
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
        conf_sections = uut.run(arg_list=["-c", config])[0]
        self.assertEqual(str(conf_sections["test"]),
                         "test {value : 2}")
        self.assertEqual(str(conf_sections["test-2"]),
                         "test-2 {files : ., bears : LineCountBear}")
        # Check merging of default_coafile, .coafile and cli
        conf_sections = uut.run(arg_list=["-c",
                                          config,
                                          "-S",
                                          "test.value=3",
                                          "test-2.bears=",
                                          "test-5.bears=TestBear2"])[0]
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
        conf_sections = uut.run(arg_list=["-S",
                                          "value=1",
                                          "test.value=2",
                                          "-c",
                                          "some_bad_file_name"])[0]
        self.assertEqual(conf_sections["default"],
                         conf_sections["test"].defaults)

    def test_back_saving(self):
        filename = os.path.join(tempfile.gettempdir(),
                                "SectionManagerTestFile")

        # We need to use a bad filename or this will parse coalas .coafile
        SectionManager().run(
            arg_list=['-S', "save=" + filename, "-c", "some_bad_filename"])

        with open(filename, "r") as f:
            lines = f.readlines()
        self.assertEqual(["[Default]\n", "config = some_bad_filename\n"],
                         lines)

        SectionManager().run(
            arg_list=['-S', "save=true", "config=" + filename, "test.value=5"])

        with open(filename, "r") as f:
            lines = f.readlines()
        os.remove(filename)
        self.assertEqual(["[Default]\n",
                          "config = " + filename + "\n",
                          "\n",
                          "[test]\n",
                          "value = 5\n"], lines)

    def test_logging_objects(self):
        conf_sections = SectionManager().run(arg_list=['-S',
                                                       "log_type=none"])[0]
        self.assertIsInstance(conf_sections["default"].log_printer,
                              NullPrinter)

    def test_targets(self):
        targets = SectionManager().run(arg_list=["default",
                                                 "test1",
                                                 "test2"])[3]
        self.assertEqual(targets, ["default", "test1", "test2"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
