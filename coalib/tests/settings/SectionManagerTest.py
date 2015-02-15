import os
import sys
import tempfile
import unittest
sys.path.insert(0, ".")

from coalib.misc.StringConstants import StringConstants
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.SectionManager import SectionManager
from coalib.output.printers.NullPrinter import NullPrinter


class SectionManagerTestCase(unittest.TestCase):
    def test_run(self):
        defaults = ConfParser().parse(os.path.abspath(os.path.join(StringConstants.coalib_root, "default_coafile")))

        uut = SectionManager()
        # We need to use a bad filename or this will parse coalas .coafile
        conf_sections = uut.run(
            arg_list=['-S', "test=5", "-c", "some_bad_filename"])[0]

        self.assertEqual(str(conf_sections["default"]),
                         "Default {config : some_bad_filename, test : 5}")
        self.assertEqual(str(conf_sections["default"].defaults),
                         str(defaults["default"]))

        local_bears = uut.run(arg_list=['-S test=5',
                                        '-c bad_filename',
                                        '-b LineCountBear'])[1]
        self.assertEqual(len(local_bears["default"]), 1)

    def test_nonexistent_file(self):
        filename = "bad.one/test\neven with bad chars in it"
        # Shouldn't throw an exception
        SectionManager().run(arg_list=['-S', "config=" + filename])

        tmp = StringConstants.coalib_root
        StringConstants.coalib_root = filename
        self.assertRaises(SystemExit, SectionManager().run)
        StringConstants.coalib_root = tmp

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
