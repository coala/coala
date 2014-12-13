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
import unittest

sys.path.insert(0, ".")

from coalib.settings.Setting import Setting, path, path_list


class SettingTestCase(unittest.TestCase):
    def test_construction(self):
        self.assertRaises(ValueError, Setting, "", 2, 2)

    def test_path(self):
        self.uut = Setting("key", " 22\n", ".", True)
        self.assertEqual(path(self.uut), os.path.join(".", "22"))

        abspath = os.path.abspath(".")
        self.uut = Setting("key", abspath)
        self.assertEqual(path(self.uut), abspath)

        self.uut = Setting("key", " 22", "")
        self.assertRaises(ValueError, path, self.uut)
        self.assertEqual(path(self.uut, origin="test"), os.path.join("test", "22"))

    def test_path_list(self):
        abspath = os.path.abspath(".")
        self.uut = Setting("key", "., " + abspath, origin="test")
        self.assertEqual(path_list(self.uut), [os.path.join("test", "."), abspath])

    def test_inherited_conversions(self):
        self.uut = Setting("key", " 22\n", ".", True)
        self.assertEqual(str(self.uut), "22")
        self.assertEqual(int(self.uut), 22)
        self.assertRaises(ValueError, bool, self.uut)


if __name__ == '__main__':
    unittest.main(verbosity=2)
