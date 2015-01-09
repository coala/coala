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
from coalib.bears.results.Result import Result, RESULT_SEVERITY
import unittest


class ResultTestCase(unittest.TestCase):
    def test_wrong_types(self):
        uut = Result('b', 'b')
        self.assertNotEqual(uut, 0)
        self.assertRaises(TypeError, uut.__ge__, 0)
        self.assertRaises(TypeError, uut.__le__, 0)
        self.assertRaises(TypeError, uut.__gt__, 0)
        self.assertRaises(TypeError, uut.__lt__, 0)

    def test_string_conversion(self):
        uut = Result('a', 'b', 'c')
        self.assertEqual(str(uut), "Result:\n origin: 'a'\n file: 'c'\n severity: 1\n'b'")
        self.assertEqual(str(uut), repr(uut))

    def test_ordering(self):
        """
        Tests the ordering routines of Result. This tests enough to have all branches covered. Not every case may be
        covered but I want to see the (wo)man who writes comparison routines that match these criteria and are wrong to
        the specification. (Given he does not engineer the routine to trick the test explicitly.)
        """
        medium = Result(origin='b', message='b', file='b', severity=RESULT_SEVERITY.NORMAL)
        medium_too = Result(origin='b', message='b', file='b', severity=RESULT_SEVERITY.NORMAL)
        self.assert_equal(medium, medium_too)

        bigger_file = Result(origin='b', message='b', file='c', severity=RESULT_SEVERITY.NORMAL)
        self.assert_ordering(bigger_file, medium)

        no_file = Result(origin='b', message='b', file=None, severity=RESULT_SEVERITY.NORMAL)
        self.assert_ordering(medium, no_file)

        no_file_and_unsevere = Result(origin='b', message='b', file=None, severity=RESULT_SEVERITY.INFO)
        self.assert_ordering(no_file_and_unsevere, no_file)
        self.assert_ordering(medium, no_file_and_unsevere)

        greater_origin = Result(origin='c', message='b', file='b', severity=RESULT_SEVERITY.NORMAL)
        self.assert_ordering(greater_origin, medium)

    def assert_equal(self, first, second):
        self.assertGreaterEqual(first, second)
        self.assertEqual(first, second)
        self.assertLessEqual(first, second)

    def assert_ordering(self, greater, lesser):
        self.assertGreater(greater, lesser)
        self.assertGreaterEqual(greater, lesser)
        self.assertNotEqual(greater, lesser)
        self.assertLessEqual(lesser, greater)
        self.assertLess(lesser, greater)


if __name__ == '__main__':
    unittest.main(verbosity=2)
