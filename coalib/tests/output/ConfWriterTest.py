import os

import sys

sys.path.insert(0, ".")
from coalib.output.ConfWriter import ConfWriter
from coalib.parsing.ConfParser import ConfParser
import unittest
import tempfile


class ConfWriterTestCase(unittest.TestCase):
    example_file = "to be ignored \n\
    save=true\n\
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
        with open(self.file, "w", encoding='utf-8') as filehandler:
            filehandler.write(self.example_file)

        self.conf_parser = ConfParser()
        self.write_file_name = os.path.join(tempfile.gettempdir(), "ConfWriterTestFile")
        self.uut = ConfWriter(self.write_file_name)

    def tearDown(self):
        os.remove(self.file)

    def test_exceptions(self):
        self.assertRaises(TypeError, self.uut.write_section, 5)

    def test_write(self):
        result_file = ["[Default]\n",
                       "save = true\n",
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

        with open(self.write_file_name, "r") as f:
            lines = f.readlines()

        self.assertEqual(result_file, lines)


if __name__ == '__main__':
    unittest.main(verbosity=2)
