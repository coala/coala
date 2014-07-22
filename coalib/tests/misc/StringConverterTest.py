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
from coalib.misc.StringConverter import StringConverter
from coalib.misc.i18n import _
import unittest


class ProcessTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = StringConverter("\n 1 \n ")

    def test_whitespace_stripping(self):
        self.assertEqual(str(self.uut), "1")

    def test_int_conversion(self):
        self.assertEqual(int(self.uut), 1)

    def test_bool_conversion(self):
        self.assertEqual(bool(self.uut), True)
        self.uut = StringConverter(_(" yeah "))
        self.assertEqual(bool(self.uut), True)
        self.uut = StringConverter(" y ")
        self.assertEqual(bool(self.uut), True)
        self.uut = StringConverter(_(" nope "))
        self.assertEqual(bool(self.uut), False)

        self.uut = StringConverter(_(" i dont know "))
        self.assertRaises(AttributeError, bool, self.uut)


if __name__ == '__main__':
    unittest.main(verbosity=2)
