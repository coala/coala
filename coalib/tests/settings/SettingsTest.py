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

import unittest
import sys

sys.path.insert(0, ".")

from coalib.settings.Settings import Settings, Setting
from coalib.misc.StringConstants import StringConstants


class SettingsTestCase(unittest.TestCase):
    def test_construction(self):
        uut = Settings(StringConstants.COMPLEX_TEST_STRING, None)
        uut = Settings(StringConstants.COMPLEX_TEST_STRING, uut)
        self.assertRaises(TypeError, Settings, "irrelevant", 5)
        self.assertRaises(ValueError, uut.__init__, "name", uut)

    def test_append(self):
        uut = Settings(StringConstants.COMPLEX_TEST_STRING, None)
        self.assertRaises(TypeError, uut.append, 5)
        uut.append(Setting(5, 5, 5))
        self.assertEqual(str(uut.get("5 ")), "5")
        self.assertEqual(int(uut.get("nonexistent", 5)), 5)

    def test_iter(self):
        defaults = Settings("default", None)
        uut = Settings("name", defaults)
        uut.append(Setting(5, 5, 5))
        uut._add_or_create_setting(Setting("TEsT", 4, 5))
        defaults.append(Setting("tEsT", 1, 3))
        defaults.append(Setting(" great   ", 3, 8))
        defaults.append(Setting(" great   ", 3, 8), custom_key="custom")
        uut._add_or_create_setting(Setting(" NEW   ", "val", 8))
        uut._add_or_create_setting(Setting(" NEW   ", "vl", 8), allow_appending=False)
        uut._add_or_create_setting(Setting("new", "val", 9),
                                   custom_key="teSt ",
                                   allow_appending=True)
        self.assertEqual(list(uut), ["5", "test", "new", "great", "custom"])

        for index in uut:
            t = uut[index]
            self.assertNotEqual(t, None)

        self.assertEqual(True, "teST" in defaults)
        self.assertEqual(True, "       GREAT" in defaults)
        self.assertEqual(False, "       GrEAT !" in defaults)
        self.assertEqual(False, "" in defaults)
        self.assertEqual(str(uut['test']), "4\nval")
        self.assertEqual(int(uut["GREAT "]), 3)
        self.assertRaises(IndexError, uut.__getitem__, "doesnotexist")
        self.assertRaises(IndexError, uut.__getitem__, "great", True)
        self.assertRaises(IndexError, uut.__getitem__, " ")


if __name__ == '__main__':
    unittest.main(verbosity=2)
