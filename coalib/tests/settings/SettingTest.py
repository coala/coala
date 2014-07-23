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

from coalib.settings.Setting import Setting, path


class SettingTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = Setting("key", " 22\n", ".", True)

    def test_path(self):
        self.assertEqual(path(self.uut), os.path.join(".", "22"))

    def test_inherited_conversions(self):
        self.assertEqual(str(self.uut), "22")
        self.assertEqual(int(self.uut), 22)
        self.assertRaises(ValueError, bool, self.uut)


if __name__ == '__main__':
    unittest.main(verbosity=2)
