"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import tempfile
import unittest
sys.path.insert(0, ".")

from coalib.misc.StringConstants import StringConstants
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.SectionManager import SectionManager


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

if __name__ == '__main__':
    unittest.main(verbosity=2)
