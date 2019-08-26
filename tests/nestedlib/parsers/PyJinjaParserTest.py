import os
import unittest
from os.path import abspath
from coalib.io.File import File

from coalib.nestedlib.parsers.PyJinjaParser import PyJinjaParser
TEST_FILE_DIR = os.path.join(os.path.split(__file__)[0], 'file_test_files')
TEST_OUTPUT_DIR = os.path.join(os.path.split(__file__)[0], 'file_test_output')


class PyJinjaParserTest(unittest.TestCase):

    def setUp(self):
        self.file_test_dir = TEST_FILE_DIR
        self.file_test_output = TEST_OUTPUT_DIR
        self.test_filename1 = 'test-jinja-py.py.jj2.txt'
        self.test_file1_path = os.path.join(self.file_test_dir,
                                            self.test_filename1)
        self.abs_test_file1_path = abspath(self.test_file1_path)

        self.test_file1 = File(self.abs_test_file1_path)
        self.test_file1_lines = (self.test_file1).lines

        self.parser = PyJinjaParser()

    def test_parse(self):
        uut_sections = self.parser.parse(self.abs_test_file1_path)
        uut_section_list = []

        nl_section_list = [
            self.abs_test_file1_path + ': 1: python: L1 C1: L1 C11:' +
            ' L1 C1: L1 C11',
            self.abs_test_file1_path + ': 2: jinja2: L2 C1: L5 C10:' +
            ' L2 C1: L5 C10',
            self.abs_test_file1_path + ': 3: jinja2: L6 C1: L6 C13:' +
            ' L6 C1: L6 C13',
            self.abs_test_file1_path + ': 4: python: L6 C14: L6 C32:' +
            ' L6 C14: L6 C32'
        ]

        for nl_section in uut_sections:
            uut_section_list.append(str(nl_section))

        self.assertEqual(nl_section_list, uut_section_list)

    def test_parse_line_1_pure_python(self):
        # Pure Python Line
        # line = 'for x in y:'
        test_file_line1 = self.test_file1.lines[0]
        uut_nl_section = self.parser.parse_line(line=test_file_line1,
                                                nl_sections=[],
                                                line_number=1,
                                                file=self.test_filename1)

        expected_nl_section_str = ('.*test-jinja-py.py.jj2.txt' +
                                   ': 1: python: L1 C1: L1 C11: L1 C1: L1 C11')

        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_str)

    def test_parse_line_2_pure_jinja(self):
        # Pure Jinja Line
        # line = '{% if x is True %}'
        test_file_line1 = self.test_file1.lines[1]
        uut_nl_section = self.parser.parse_line(line=test_file_line1,
                                                nl_sections=[],
                                                line_number=2,
                                                file=self.test_filename1)

        expected_nl_section_str = ('.*test-jinja-py.py.jj2.txt' +
                                   ': 1: jinja2: L2 C1: L2 C18: L2 C1: L2 C18')

        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_str)

    def test_parse_line_5_mixed_line(self):
        # A Line with python and Jinja
        # line = '    {{ var }} = print("Bye Bye")'
        test_file_line1 = self.test_file1.lines[5]
        uut_nl_section = self.parser.parse_line(line=test_file_line1,
                                                nl_sections=[],
                                                line_number=5,
                                                file=self.test_filename1)

        expected_nl_section_1_str = (
                                    '.*test-jinja-py.py.jj2.txt' +
                                    ': 1: jinja2: L5 C1: L5 C13: L5 C1: L5 C13'
                                )

        expected_nl_section_2_str = (
                                  '.*test-jinja-py.py.jj2.txt' +
                                  ': 2: python: L5 C14: L5 C32: L5 C14: L5 C32'
                                  )

        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_1_str)
        self.assertRegex(str(uut_nl_section[1]), expected_nl_section_2_str)

    def test_parse_line_impure_line_conditions(self):

        # Test condition: match.start() == cursor and match.end() < end_column
        # line = '{% set x = 12 %} print(x)'
        line = '{% set x = 12 %} print(x)\n'
        uut_nl_section = self.parser.parse_line(line=line,
                                                nl_sections=[],
                                                line_number=1,
                                                file=self.test_filename1)

        expected_nl_section_1_str = (
                                    '.*test-jinja-py.py.jj2.txt' +
                                    ': 1: jinja2: L1 C1: L1 C16: L1 C1: L1 C16')

        expected_nl_section_2_str = (
                                '.*test-jinja-py.py.jj2.txt' +
                                ': 2: python: L1 C17: L1 C25: L1 C17: L1 C25'
                                )

        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_1_str)
        self.assertRegex(str(uut_nl_section[1]), expected_nl_section_2_str)

        # Test condition: match.start() > cursor and match.end() == end_column
        # line = '   {% set x = 12 %} print(x)'
        line = '   {% set x = 12 %} print(x)\n'
        uut_nl_section = self.parser.parse_line(line=line,
                                                nl_sections=[],
                                                line_number=1,
                                                file=self.test_filename1)

        expected_nl_section_1_str = (
                                    '.*test-jinja-py.py.jj2.txt' +
                                    ': 1: jinja2: L1 C1: L1 C19: L1 C1: L1 C19')

        expected_nl_section_2_str = (
                                '.*test-jinja-py.py.jj2.txt' +
                                ': 2: python: L1 C20: L1 C28: L1 C20: L1 C28')

        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_1_str)
        self.assertRegex(str(uut_nl_section[1]), expected_nl_section_2_str)

        line = 'print(x) {% set x = 12 %}\n'
        uut_nl_section = self.parser.parse_line(line=line,
                                                nl_sections=[],
                                                line_number=1,
                                                file=self.test_filename1)

        expected_nl_section_1_str = ('.*test-jinja-py.py.jj2.txt' +
                                     ': 1: python: L1 C1: L1 C9: L1 C1: L1 C9')

        expected_nl_section_2_str = (
                                '.*test-jinja-py.py.jj2.txt' +
                                ': 2: jinja2: L1 C10: L1 C25: L1 C10: L1 C25')

        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_1_str)
        self.assertRegex(str(uut_nl_section[1]), expected_nl_section_2_str)

    def test_impure_lines_two_jinja_elements(self):

        # Test Contition1: match.start() > cursor and match.end() < end_column
        # Test Condition2: num_jinja_elem > 1
        # line = '{% set x = 12 %} print(x) {% if x > 40 %}'

        line = '{% set x = 12 %} print(x) {% if x > 40 %}  print(x)\n'
        uut_nl_section = self.parser.parse_line(line=line,
                                                nl_sections=[],
                                                line_number=1,
                                                file=self.test_filename1)

        expected_nl_section_1_str = (
                                    '.*test-jinja-py.py.jj2.txt' +
                                    ': 1: jinja2: L1 C1: L1 C16: L1 C1: L1 C16')

        expected_nl_section_2_str = (
                                '.*test-jinja-py.py.jj2.txt' +
                                ': 2: python: L1 C17: L1 C26: L1 C17: L1 C26')

        expected_nl_section_3_str = (
                                '.*test-jinja-py.py.jj2.txt' +
                                ': 3: jinja2: L1 C27: L1 C41: L1 C27: L1 C41')

        expected_nl_section_4_str = (
                                '.*test-jinja-py.py.jj2.txt' +
                                ': 4: python: L1 C42: L1 C51: L1 C42: L1 C51')

        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_1_str)
        self.assertRegex(str(uut_nl_section[1]), expected_nl_section_2_str)
        self.assertRegex(str(uut_nl_section[2]), expected_nl_section_3_str)
        self.assertRegex(str(uut_nl_section[3]), expected_nl_section_4_str)

    def test_parse_line_spaces_at_end(self):

        # Test condition: if not cursor == end_column and
        #                                      content_after_match.isspace()
        # line = '{% set y = 10 %} z = 30   '
        line = '{% set y = 10 %}   \n'
        uut_nl_section = self.parser.parse_line(line=line,
                                                nl_sections=[],
                                                line_number=1,
                                                file=self.test_filename1)

        expected_nl_section_1_str = (
                                    '.*test-jinja-py.py.jj2.txt' +
                                    ': 1: jinja2: L1 C1: L1 C19: L1 C1: L1 C19')

        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_1_str)

    def test_parse_line_empty_line(self):

        # Test condition: not line.strip()
        # line = '\n'
        line = '\n'
        uut_nl_section = self.parser.parse_line(line=line,
                                                nl_sections=[],
                                                line_number=1,
                                                file=self.test_filename1)

        expected_nl_section_1_str = ('.*test-jinja-py.py.jj2.txt' +
                                     ': 1: jinja2: L1 C1: L1 C1: L1 C1: L1 C1')
        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_1_str)

    def test_parse_pure_jinja_white_space_before_after(self):

        # Test Condition: if content_before_match.isspace() and
        #                      content_after_match.isspace()
        # If the pure line has spaces before the element and after the element
        # line = '    {{ var }}    \n'

        line = '    {{ var }}    \n'
        uut_nl_section = self.parser.parse_line(line=line,
                                                nl_sections=[],
                                                line_number=1,
                                                file=self.test_filename1)

        expected_nl_section_1_str = (
                                    '.*test-jinja-py.py.jj2.txt' +
                                    ': 1: jinja2: L1 C1: L1 C17: L1 C1: L1 C17')
        self.assertRegex(str(uut_nl_section[0]), expected_nl_section_1_str)

    def test_coala_setup_template(self):

        # Test the setup template of coala present in the moban repository
        # The expected output of the parser is saved in another file.

        test_filename = 'test-setup-py.py.jj2.txt'
        test_file_path = os.path.join(self.file_test_dir, test_filename)
        abs_test_file_path = abspath(test_file_path)

        test_output_filename = 'coala-setup-parser-output.txt'
        test_file_ouput_path = os.path.join(self.file_test_output,
                                            test_output_filename)
        abs_test_file_output_path = abspath(test_file_ouput_path)
        test_ouput_file = File(abs_test_file_output_path)

        uut_sections = self.parser.parse(abs_test_file_path)
        nl_section_string = ''
        expected_string = ''

        for nl_section in uut_sections:
            nl_section_string += (str(nl_section)+'\n')

        for line in test_ouput_file.lines:
            expected_string += (abs_test_file_path + line)

        self.assertEqual(nl_section_string, expected_string)

    def test_coala_setup_template_output(self):

        # Generates text using the values generated by the parser
        # Check if the generated text is equal to the original file

        test_filename = 'test-setup-py.py.jj2.txt'
        test_file_path = os.path.join(self.file_test_dir, test_filename)
        abs_test_file_path = abspath(test_file_path)

        original_file = File(abs_test_file_path)
        original_file_content = original_file.string

        uut_sections = self.parser.parse(abs_test_file_path)
        generated_file_contents = ''

        for nl_section in uut_sections:

            start_line = nl_section.start.line
            start_column = nl_section.start.column
            end_line = nl_section.end.line
            end_column = nl_section.end.column

            for line_nr in range(start_line, end_line+1):
                if (line_nr == end_line and line_nr == start_line):
                    generated_file_contents += (
                        original_file[line_nr-1][start_column-1:end_column])
                    if end_column == len(original_file[line_nr-1]) - 1:
                        generated_file_contents += '\n'
                else:
                    generated_file_contents += original_file[line_nr-1][:]

        self.assertEqual(original_file_content, generated_file_contents)
