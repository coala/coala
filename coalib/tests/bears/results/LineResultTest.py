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
from coalib.bears.results.LineResult import Result, LineResult
import unittest


class ResultTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = LineResult("origin", 1, "line", "message", "file")

    def test_equality(self):
        cmp = LineResult("origin", 1, "line", "message", "file")
        self.assertEqual(cmp, self.uut)
        cmp = Result("origin", "message")
        self.assertNotEqual(cmp, self.uut)
        cmp = LineResult("origin", 1, "lineswrong", "message", "file")
        self.assertNotEqual(cmp, self.uut)

    def test_str_conversion(self):
        self.assertEqual(self.uut.__str__(), """LineResult:
 origin: 'origin'
 file: 'file'
 severity: 1
 line: 'line'
 line nr: 1
'message'""")


if __name__ == '__main__':
    unittest.main(verbosity=2)
