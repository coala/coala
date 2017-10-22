import os
import tempfile
import unittest

from coalib.output.ConfWriter import ConfWriter
from coalib.settings.Section import Section
from coalib.settings.ConfigurationGathering import load_configuration
from coalib.output.printers.LogPrinter import LogPrinter
from coala_utils.string_processing import escape


class ConfWriterTest(unittest.TestCase):
    example_file = ('to be ignored \n'
                    '    save=true\n'
                    '    a_default, another = val \n'
                    '    TEST = tobeignored  # thats a comment \n'
                    '    test = push \n'
                    '    t = \n'
                    '    [Section] \n'
                    '    [MakeFiles] \n'
                    '     j  , ANother = a \n'
                    '                   multiline \n'
                    '                   value \n'
                    '    ; just a omment \n'
                    '    ; just a omment \n'
                    '    key\\ space = value space\n'
                    '    key\\=equal = value=equal\n'
                    '    key\\\\backslash = value\\\\backslash\n'
                    '    key\\,comma = value,comma\n'
                    '    key\\#hash = value\\#hash\n'
                    '    key\\.dot = value.dot\n'
                    '    a_default = val, val2\n')

    append_example_file = ('[defaults]\n'
                           'a = 4\n'
                           'b = 4,5,6\n'
                           'c = 4,5\n'
                           'd = 4\n'
                           '[defaults.new]\n'
                           'a = 4,5,6,7\n'
                           'b = 4,5,6,7\n'
                           'c = 4,5,6,7\n'
                           'd = 4,5,6,7\n')

    def setUp(self):
        self.file = os.path.join(tempfile.gettempdir(), 'ConfParserTestFile')
        with open(self.file, 'w', encoding='utf-8') as file:
            file.write(self.example_file)

        self.log_printer = LogPrinter()
        self.write_file_name = os.path.join(tempfile.gettempdir(),
                                            'ConfWriterTestFile')
        self.uut = ConfWriter(self.write_file_name)

    def tearDown(self):
        self.uut.close()
        os.remove(self.file)
        os.remove(self.write_file_name)

    def test_exceptions(self):
        self.assertRaises(TypeError, self.uut.write_section, 5)

    def test_write(self):
        result_file = ['[Section]\n',
                       '[MakeFiles]\n',
                       'j, ANother = a\n',
                       'multiline\n',
                       'value\n',
                       '; just a omment\n',
                       '; just a omment\n',
                       'key\\ space = value space\n',
                       'key\\=equal = value=equal\n',
                       'key\\\\backslash = value\\\\backslash\n',
                       'key\\,comma = value,comma\n',
                       'key\\#hash = value\\#hash\n',
                       'key\\.dot = value.dot\n',
                       'a_default += val2\n',
                       '[cli]\n',
                       'save = true\n',
                       'a_default, another = val\n',
                       '# thats a comment\n',
                       'test = push\n',
                       't = \n']
        sections = load_configuration(['-c', escape(self.file, '\\')],
                                      self.log_printer)[0]
        del sections['cli'].contents['config']
        self.uut.write_sections(sections)
        self.uut.close()

        with open(self.write_file_name, 'r') as f:
            lines = f.readlines()

        self.assertEqual(result_file, lines)

    def test_append(self):
        with open(self.file, 'w', encoding='utf-8') as file:
            file.write(self.append_example_file)

        result_file = ['[defaults]\n',
                       'a = 4\n',
                       'b = 4,5,6\n',
                       'c = 4,5\n',
                       'd = 4\n',
                       '[defaults.new]\n',
                       'b += 7\n',
                       'c += 6, 7\n',
                       'a, d += 5, 6, 7\n',
                       '[cli]\n']

        sections = load_configuration(['-c', escape(self.file, '\\')],
                                      self.log_printer)[0]
        del sections['cli'].contents['config']
        self.uut.write_sections(sections)
        self.uut.close()

        with open(self.write_file_name, 'r') as f:
            lines = f.readlines()

        self.assertEqual(result_file, lines)

    def test_write_with_dir(self):
        self.uut_dir = ConfWriter(tempfile.gettempdir())
        self.uut_dir.write_sections({'name': Section('name')})
        self.uut_dir.close()

        with open(os.path.join(tempfile.gettempdir(), '.coafile'), 'r') as f:
            lines = f.readlines()

        self.assertEqual(['[name]\n'], lines)
        os.remove(os.path.join(tempfile.gettempdir(), '.coafile'))
