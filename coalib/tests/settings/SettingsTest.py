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

    def test_append(self):
        uut = Settings(StringConstants.COMPLEX_TEST_STRING, None)
        self.assertRaises(TypeError, uut.append, 5)
        uut.append(Setting(5, 5, 5))


if __name__ == '__main__':
    unittest.main(verbosity=2)
