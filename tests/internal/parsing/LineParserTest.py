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
        self.check_data_set("# comment only$§\n", output_comment="# comment only$§")
        self.check_data_set("   ; comment only  \n", output_comment="; comment only")

    def test_multi_value_parsing(self):
        self.check_data_set("a, b c= = :()&/ #heres a comment \n",
                            '',
                            ['a', 'b', 'c'],
                            '= :()&/',
                            '#heres a comment')

    def test_section_name_parsing(self):
        self.check_data_set(" [   a section name   ]      # with comment   \n",
                            'a section name',
                            output_comment="# with comment")

        self.uut.section_name_surroundings["Section:"] = ''
        self.check_data_set("[  sec]; thats a normal section",
                            "sec",
                            output_comment="; thats a normal section")
        self.check_data_set("  Section:  sec]; thats a new section",
                            "sec]",
                            output_comment="; thats a new section")

    def check_data_set(self, line, output_section="", output_keys=[], output_value='', output_comment=''):
        section_name, keys, value, comment = self.uut.parse(line)

        self.assertEqual(section_name, output_section)
        self.assertEqual(keys, output_keys)
        self.assertEqual(value, output_value)
        self.assertEqual(comment, output_comment)


if __name__ == '__main__':
    unittest.main()
