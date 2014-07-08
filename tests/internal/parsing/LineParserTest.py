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
import unittest
from coalib.internal.parsing.LineParser import LineParser


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = LineParser()

    def test_comment_parsing(self):
        section_name, keys, value, comment = self.uut.parse("# comment only")
        self.assertEqual(section_name, '')
        self.assertEqual(keys, [])
        self.assertEqual(value, '')
        self.assertEqual(comment, '# comment only')


        section_name, keys, value, comment = self.uut.parse("   ; comment only  ")
        self.assertEqual(section_name, '')
        self.assertEqual(keys, [])
        self.assertEqual(value, '')
        self.assertEqual(comment, '; comment only')

    def test_multi_value_parsing(self):
        section_name, keys, value, comment = self.uut.parse("a, b c= :()&/ #heres a comment ")
        self.assertEqual(section_name, '')
        self.assertEqual(keys, ['a', 'b', 'c'])
        self.assertEqual(value, ':()&/')
        self.assertEqual(comment, '#heres a comment')

    def test_section_name_parsing(self):
        section_name, keys, value, comment = self.uut.parse(" [   a section name   ]      # with comment   ")
        self.assertEqual(section_name, 'a section name')
        self.assertEqual(keys, [])
        self.assertEqual(value, '')
        self.assertEqual(comment, '# with comment')

if __name__ == '__main__':
    unittest.main()
