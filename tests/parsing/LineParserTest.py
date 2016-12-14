import unittest
import logging

from coalib.parsing.LineParser import LineParser


class LineParserTest(unittest.TestCase):

    def setUp(self):
        self.uut = LineParser(comment_separators=('#', ';'))

    def test_empty_line(self):
        self.check_data_set('')
        self.check_data_set('\n \n \n')

    def test_comment_parsing(self):
        self.check_data_set('# comment only$§\n',
                            output_comment='# comment only$§')
        self.check_data_set('   ; comment only  \n',
                            output_comment='; comment only')
        self.check_data_set('   ; \\comment only  \n',
                            output_comment='; comment only')
        self.check_data_set('#', output_comment='#')

    def test_section_override(self):
        self.check_data_set(r'a.b, \a\.\b\ c=',
                            output_keys=[('a', 'b'), ('', r'\a.\b c')])

    def test_escaping(self):
        self.check_data_set("hello = world\ # yes here's a space",
                            output_keys=[('', 'hello')],
                            output_value='world\\ ',
                            output_comment="# yes here's a space")

    def test_multi_value_parsing(self):
        self.check_data_set(
            'a, b\\ \\=, section.c= = :()&/ \\\\#heres a comment \n',
            output_section='',
            output_keys=[('', 'a'), ('', 'b ='), ('section', 'c')],
            output_value='= :()&/ \\\\',
            output_comment='#heres a comment')

    def test_multi_line_parsing(self):
        self.check_data_set(' a,b,d another value ',
                            output_value='a,b,d another value')
        self.check_data_set(' a,b,d\\= another value ',
                            output_value='a,b,d\\= another value')

    def test_section_name_parsing(self):
        self.check_data_set(' [   a section name   ]      # with comment   \n',
                            'a section name',
                            output_comment='# with comment')
        self.check_data_set(' [   a section name]   ]         \n',
                            'a section name]')
        self.check_data_set(' [   a section name\\]   ]         \n',
                            'a section name]')
        self.check_data_set(' [   a section name\\;   ]         \n',
                            'a section name;')

        self.uut.section_name_surroundings['Section:'] = ''
        self.check_data_set('[  sec]; thats a normal section',
                            output_section='sec',
                            output_comment='; thats a normal section')
        self.check_data_set('  Section:  sEc]\\\\; thats a new section',
                            output_section='sEc]\\',
                            output_comment='; thats a new section')
        self.check_data_set('  Section:  sec]\\\\\\\\; thats a new section',
                            output_section='sec]\\\\',
                            output_comment='; thats a new section')
        self.check_data_set('  Section:  sec]\\\\\\; thats a new section',
                            output_section='sec]\\; thats a new section')

    def test_append_value_parsing(self):
        self.check_data_set('a += b',
                            output_keys=[('', 'a')],
                            output_value='b',
                            output_append=True)
        self.check_data_set('a = b',
                            output_keys=[('', 'a')],
                            output_value='b')
        self.check_data_set('a \\+\\= b',
                            output_value='a \\+\\= b')

    def check_data_set(self,
                       line,
                       output_section='',
                       output_keys=None,
                       output_value='',
                       output_append=False,
                       output_comment=''):
        output_keys = output_keys or []

        section_name, keys, value, append, comment = self.uut._parse(line)

        self.assertEqual(section_name, output_section)
        self.assertEqual(keys, output_keys)
        self.assertEqual(value, output_value)
        self.assertEqual(append, output_append)
        self.assertEqual(comment, output_comment)

    def test_deprecation(self):
        logger = logging.getLogger()

        with self.assertLogs(logger, 'WARNING') as cm:
            self.uut.parse('')

        self.assertRegex(cm.output[0], 'WARNING:root:The parse method of '
                                       'LineParser is deprecated\.*')
