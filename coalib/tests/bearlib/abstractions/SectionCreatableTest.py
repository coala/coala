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
from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable


class SectionCreatableTestCase(unittest.TestCase):
    def test_api(self):
        uut = SectionCreatable()
        self.assertRaises(NotImplementedError, uut.from_section, 5)
        self.assertEqual(uut.get_non_optional_settings(), {})
        self.assertEqual(uut.get_optional_settings(), {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
