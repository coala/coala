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

    def test_construction(self):
        self.assertRaises(TypeError, StringConverter, "test", strip_whitespaces=5)
        self.assertRaises(TypeError, StringConverter, "test", list_delimiters=5)

    def test_whitespace_stripping(self):
        self.assertEqual(str(self.uut), "1")

        self.uut = StringConverter("\n 1 \n", strip_whitespaces=False)
        self.assertEqual(str(self.uut), "\n 1 \n")

    def test_int_conversion(self):
        self.assertEqual(int(self.uut), 1)
        self.uut = StringConverter(" not an int ")
        self.assertRaises(ValueError, int, self.uut)

    def test_len(self):
        self.assertEqual(len(self.uut), 1)

    def test_iterator(self):
        self.uut = StringConverter("a, test with!!some challenge", list_delimiters=[",", " ", "!!"])
        self.assertEqual(list(self.uut), ["a", "test", "with", "some", "challenge"])
        self.uut = StringConverter("a, test with!some challenge", list_delimiters=", !")
        self.assertEqual(list(self.uut), ["a", "test", "with", "some", "challenge"])
        self.uut = StringConverter("a\\n,bug¸g", list_delimiters=["\\", ",", "¸"])
        self.assertEqual(list(self.uut), ["a", "n", "bug", "g"])

        self.assertTrue("bug" in self.uut)
        self.assertFalse("but" in self.uut)

    def test_bool_conversion(self):
        self.assertEqual(bool(self.uut), True)
        self.uut = StringConverter(_("yeah"))
        self.assertEqual(bool(self.uut), True)
        self.uut = StringConverter("y")
        self.assertEqual(bool(self.uut), True)
        self.uut = StringConverter(_("nope"))
        self.assertEqual(bool(self.uut), False)

        self.uut = StringConverter(" i dont know ")
        self.assertRaises(ValueError, bool, self.uut)


if __name__ == '__main__':
    unittest.main(verbosity=2)
