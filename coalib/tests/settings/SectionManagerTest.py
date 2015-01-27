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
        # We need to use a bad filename or this will parse the .coafile we use for coala
        conf_sections = uut.run(arg_list=['-S', "test=5", "-c", "some_bad_filename"])[0]

        self.assertEqual(str(conf_sections["default"]), "Default {config : some_bad_filename, test : 5}")
        self.assertEqual(str(conf_sections["default"].defaults), str(defaults["default"]))

    def test_nonexistent_file(self):
        filename = "bad.one/test\neven with bad chars in it"
        SectionManager().run(arg_list=['-S', "config=" + filename])  # Shouldn't throw an exception

        tmp = StringConstants.coalib_root
        StringConstants.coalib_root = filename
        self.assertRaises(SystemExit, SectionManager().run)
        StringConstants.coalib_root = tmp

    def test_back_saving(self):
        filename = os.path.join(tempfile.gettempdir(), "SectionManagerTestFile")

        # We need to use a bad filename or this will parse the .coafile we use for coala
        SectionManager().run(arg_list=['-S', "save=" + filename, "-c", "some_bad_filename"])

        with open(filename, "r") as f:
            lines = f.readlines()
        self.assertEqual(["[Default]\n", "config = some_bad_filename\n"], lines)

        SectionManager().run(arg_list=['-S', "save=true", "config=" + filename, "test.value=5"])

        with open(filename, "r") as f:
            lines = f.readlines()
        os.remove(filename)
        self.assertEqual(["[Default]\n",
                          "config = " + filename + "\n",
                          "[test]\n",
                          "value = 5\n"], lines)

    def test_logging_objects(self):
        conf_sections, n, m = SectionManager().run(arg_list=['-S', "log_type=none"])
        self.assertIsInstance(conf_sections["default"].log_printer, NullPrinter)


if __name__ == '__main__':
    unittest.main(verbosity=2)
