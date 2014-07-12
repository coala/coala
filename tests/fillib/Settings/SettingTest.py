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
import sys
sys.path.append(".")
from coalib.fillib.settings.Setting import Setting
import unittest


class SettingTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = Setting("key", "value", "origin")

    def test_conversions(self):
        self.uut.set_value("   adw   ")
        self.assertEqual(str(self.uut), "adw")
        self.uut.set_value("  7  ")
        self.assertEqual(int(self.uut), 7)
        self.uut.set_value(" tRuE ")
        self.assertEqual(bool(self.uut), True)
        self.uut.set_value(" fALSE ")
        self.assertEqual(bool(self.uut), False)


if __name__ == '__main__':
    unittest.main()
