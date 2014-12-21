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
sys.path.insert(0, ".")
import unittest
from coalib.settings.Section import Section
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.settings.Setting import Setting


class SpacingHelperTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = SpacingHelper()

    def test_needed_settings(self):
        self.assertEqual(list(self.uut.get_needed_settings()), ["tab_width"])
        self.assertEqual(list(self.uut.get_minimal_needed_settings()), [])

    def test_construction(self):
        section = Section("test section")
        self.assertRaises(TypeError, SpacingHelper, "no integer")
        self.assertRaises(TypeError, self.uut.from_section, 5)
        self.assertRaises(ValueError, self.uut.from_section, section, tab_width="invalid")

        self.assertEqual(self.uut.tab_width, self.uut.from_section(section).tab_width)
        self.assertEqual(3, self.uut.from_section(section, tab_width=3).tab_width)
        self.assertEqual(3, self.uut.from_section(section, tab_width=3).tab_width)

        section.append(Setting("tab_width", 5))
        self.assertEqual(5, self.uut.from_section(section, tab_width=3).tab_width)
        section.append(Setting("tab_width", "invalid"))
        self.assertRaises(ValueError, self.uut.from_section, section)


if __name__ == '__main__':
    unittest.main(verbosity=2)
