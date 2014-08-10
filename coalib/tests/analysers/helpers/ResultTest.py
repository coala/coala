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
from coalib.analysers.helpers.Result import Result


class ResultTestCase(unittest.TestCase):
    def setUp(self):
        self.line_2 = Result("same name", 2, "test")
        self.line_3 = Result("same name", 3, "testl")
        self.line_3_alternated = Result("same name", 3, "tes")
        self.other_file = Result("other file", 3, "tes")

    def test_equality(self):
        self.assertEqual(self.line_3, self.line_3)
        self.assertNotEqual(self.line_3, self.line_3_alternated)

    def test_l(self):
        self.assertLess(self.line_2, self.line_3)
        self.assertLessEqual(self.line_2, self.line_3)
        self.assertLessEqual(self.line_3, self.line_3)

    def test_g(self):
        self.assertGreater(self.line_3, self.line_2)
        self.assertGreaterEqual(self.line_3, self.line_2)
        self.assertGreaterEqual(self.line_3, self.line_3)

    def test_exceptions(self):
        self.assertRaises(AttributeError, self.line_3.__eq__, self.other_file)
        self.assertRaises(TypeError, self.line_3.__eq__, 4)


if __name__ == '__main__':
    unittest.main(verbosity=2)
