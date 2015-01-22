import os
import sys
import tempfile
import unittest
sys.path.insert(0, ".")

from coalib.misc.StringConstants import StringConstants
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.SectionManager import SectionManager
from coalib.output.NullPrinter import NullPrinter


class SectionManagerTestCase(unittest.TestCase):
    def test_run(self):
        defaults = ConfParser().parse(os.path.abspath(os.path.join(StringConstants.coalib_root, "default_coafile")))

        uut = SectionManager()
        conf_sections = uut.run(arg_list=["test=5"])[0]

        self.assertEqual(str(conf_sections["default"]), "Default {test : 5}")
        self.assertEqual(str(conf_sections["default"].defaults), str(defaults["default"]))

    def test_nonexistent_file(self):
        filename = "bad.one/test\neven with bad chars in it"
        SectionManager().run(arg_list=["config=" + filename])  # Shouldn't throw an exception

        tmp = StringConstants.coalib_root
        StringConstants.coalib_root = filename
        self.assertRaises(SystemExit, SectionManager().run)
        StringConstants.coalib_root = tmp

    def test_back_saving(self):
        filename = os.path.join(tempfile.gettempdir(), "SectionManagerTestFile")

        SectionManager().run(arg_list=["save=" + filename])

        with open(filename, "r") as f:
            lines = f.readlines()
        self.assertEqual(["[Default]\n"], lines)

        SectionManager().run(arg_list=["save=true", "config=" + filename, "test.value=5"])

        with open(filename, "r") as f:
            lines = f.readlines()
        os.remove(filename)
        self.assertEqual(["[Default]\n",
                          "config = " + filename + "\n",
                          "[test]\n",
                          "value = 5\n"], lines)

    def test_logging_objects(self):
        conf_sections, n, m = SectionManager().run(arg_list=["log_type=none"])
        self.assertIsInstance(conf_sections["default"].log_printer, NullPrinter)


if __name__ == '__main__':
    unittest.main(verbosity=2)
