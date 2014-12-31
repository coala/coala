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
import os

import sys

sys.path.insert(0, ".")
from coalib.output.ConfWriter import ConfWriter
from coalib.parsing.ConfParser import ConfParser
import unittest
import tempfile


class ConfWriterTestCase(unittest.TestCase):
    example_file = "to be ignored \n\
    a_default, another = val \n\
    TEST = tobeignored  # do you know that thats a comment \n\
    test = push \n\
    t = \n\
    \n\
    [MakeFiles] \n\
     j  , another = a \n\
                   multiline \n\
                   value \n\
    ; just a omment \n\
    ; just a omment \n"

    def setUp(self):
        self.file = os.path.join(tempfile.gettempdir(), "ConfParserTestFile")
        filehandler = open(self.file, "w", encoding='utf-8')
        filehandler.write(self.example_file)
        filehandler.close()
        self.conf_parser = ConfParser()
        self.write_file_name = os.path.join(tempfile.gettempdir(), "ConfWriterTestFile")
        self.uut = ConfWriter(self.write_file_name)

    def tearDown(self):
        os.remove(self.file)

    def test_exceptions(self):
        self.assertRaises(TypeError, self.uut.write_section, 5)

    def test_write(self):
        result_file = ["[Default]\n",
                       "a_default, another = val\n",
                       "# do you know that thats a comment\n",
                       "test = push\n",
                       "t = \n",
                       "\n",
                       "[makefiles]\n",
                       "j, another = a\n",
                       "multiline\n",
                       "value\n",
                       "; just a omment\n",
                       "; just a omment\n"]
        self.uut.write_sections(self.conf_parser.reparse(self.file))
        del self.uut

        f = open(self.write_file_name, "r")
        lines = f.readlines()
        f.close()
        self.assertEqual(result_file, lines)


if __name__ == '__main__':
    unittest.main(verbosity=2)
