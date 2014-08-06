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
from collections import OrderedDict
import os

import sys
sys.path.insert(0, ".")
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.Setting import Setting
from coalib.settings.Settings import Settings
import unittest
import tempfile


class LineParserTestCase(unittest.TestCase):
    example_file = "to be ignored \n\
    a_default, another = val \n\
    TEST = tobeignored  # do you know that thats a comment \n\
    test = push \n\
    t = \n\
    [MakeFiles] \n\
     j  , another = a \n\
                   multiline \n\
                   value \n\
    ; just a omment \n\
    ; just a omment \n\
    "
    def setUp(self):
        self.file = os.path.join(tempfile.gettempdir(), "ConfParserTestFile")
        self.nonexistentfile = os.path.join(tempfile.gettempdir(), "NonExistentTestFile")
        filehandler = open(self.file, "w", encoding='utf-8')
        filehandler.write(self.example_file)
        filehandler.close()
        self.uut = ConfParser()
        try:
            os.remove(self.nonexistentfile)
        except FileNotFoundError:
            pass

    def tearDown(self):
        os.remove(self.file)

    def test_parse(self):
        default_should = OrderedDict([
            ('a_default', 'val'),
            ('another', 'val'),
            ('comment0', '# do you know that thats a comment'),
            ('test', 'push'),
            ('t', '')
        ])

        makefiles_should = OrderedDict([
            ('j', 'a\nmultiline\nvalue'),
            ('another', 'a\nmultiline\nvalue'),
            ('comment1', '; just a omment'),
            ('comment2', '; just a omment'),
            ('a_default', 'val'),
            ('comment0', '# do you know that thats a comment'),
            ('test', 'push'),
            ('t', '')
        ])

        self.assertNotEqual(self.uut.parse(self.nonexistentfile), None)
        self.assertEqual(self.uut.parse(self.file), None)
        self.assertEqual(self.uut.reparse(self.file), None)

        sections = self.uut.export_to_settings()

        key, val = sections.popitem(last=False)
        self.assertTrue(isinstance(val, Settings))
        self.assertEqual(key, 'default')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, default_should)

        key, val = sections.popitem(last=False)
        self.assertTrue(isinstance(val, Settings))
        self.assertEqual(key, 'makefiles')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, makefiles_should)

        self.assertRaises(IndexError, self.uut.get_section, "inexistent section")


if __name__ == '__main__':
    unittest.main(verbosity=2)
