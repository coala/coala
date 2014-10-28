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
from coalib.collecting.Collector import Collector


class TestEmptyBasicCollector(unittest.TestCase):
    def setUp(self):
        self.uut = Collector()

    def test_raises(self):
        self.assertRaises(NotImplementedError, self.uut.collect)

        self.assertRaises(ValueError, iter, self.uut)
        self.assertRaises(ValueError, list, self.uut)
        self.assertRaises(ValueError, len, self.uut)
        self.assertRaises(ValueError, self.uut.__getitem__, 90)
        self.assertRaises(ValueError, reversed, self.uut)


class TestCollectedBasicCollector(unittest.TestCase):
    def setUp(self):
        self.uut = Collector()
        self.uut._items = [1, 2, 3]

    def test_list(self):
        self.assertEqual(list(self.uut), [1, 2, 3])

    def test_len(self):
        self.assertEqual(len(self.uut), 3)

    def test_getitem(self):
        self.assertEqual(self.uut[0], 1)
        self.assertEqual(self.uut[2], 3)
        self.assertEqual(self.uut[-1], 3)

        self.assertRaises(IndexError, self.uut.__getitem__, 90)

    def test_reversed(self):
        self.assertEqual(list(reversed(self.uut)), [3, 2, 1])


if __name__ == '__main__':
    unittest.main(verbosity=2)
