import unittest

from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.nestedlib.NlCliParsing import (parse_nl_cli, check_conflicts)


class NlCliParsingTest(unittest.TestCase):

    def setUp(self):
        self.arg_list = ['--no-config', '--handle-nested',
                         '--bears=PEP8Bear',
                         '--languages=python,jinja2',
                         '--files=test.py_nl_python',
                         '-S', 'section1.key1,section2.key2=value1,value2',
                         'section2.key2=only_this_value',
                         'SECTION2.key2a=k2a',
                         'invalid.=shouldnt_be_shown',
                         '.=not_either',
                         '.key=only_in_cli',
                         'default_key1,default_key2=single_value',
                         'default_key3=first_value,second_value']

        self.arg_parser = default_arg_parser()
        self.args = self.arg_parser.parse_args(self.arg_list)
        self.nl_info_dict = {
                'bears': ['PEP8Bear', 'Jinja2Bear'],
                'files': ['test.py'],
                'lang_bear_dict': {
                                    'jinja2': ['Jinja2Bear'],
                                    'python': ['PEP8Bear']
                                  },
                'languages': ['python', 'jinja2'],
                'nl_file_info': {'test.py': {
                                                'python': 'test.py_nl_python',
                                                'jinja2': 'test.py_nl_jinja2'
                                              },
                                 }
                }

    @staticmethod
    def dict_from_sections(parsed_sections):
        parsed_dict = {}
        for section_name, section in parsed_sections.items():
            parsed_dict[section_name] = (
                set([(key,
                      str(value)) for key, value in section.contents.items()]))
        return parsed_dict

    def test_parse_cli(self):
        parsed_sections = parse_nl_cli(
                            args=self.args,
                            nl_section_name='cli_nl_section: test.py_nl_python',
                            nl_info_dict=self.nl_info_dict)
        expected_dict = {
            'cli_nl_section: test.py_nl_python': {
                                            ('bears', 'PEP8Bear'),
                                            ('default_key1', 'single_value'),
                                            ('default_key2', 'single_value'),
                                            ('default_key3',
                                             'first_value,second_value'),
                                            ('files', 'test.py_nl_python'),
                                            ('handle_nested', 'True'),
                                            ('key', 'only_in_cli'),
                                            ('languages', 'python,jinja2'),
                                            ('no_config', 'True'),
                                            ('targets', '')},
            'section1': {('key1', 'value1,value2')},
            'section2': {('key2', 'only_this_value'), ('key2a', 'k2a')}}

        self.assertEqual(
            parsed_sections['cli_nl_section: test.py_nl_python'].name,
            'cli_nl_section: test.py_nl_python')

        self.maxDiff = None
        self.assertEqual(self.dict_from_sections(parsed_sections),
                         expected_dict)

    def test_check_conflicts(self):
        arg_parser = default_arg_parser()

        arg_list = ['--save', '--no-config']
        args = arg_parser.parse_args(arg_list)
        sections = parse_nl_cli(args=args, nl_info_dict=self.nl_info_dict)
        with self.assertRaisesRegex(SystemExit, '2') as cm:
            check_conflicts(sections)
            self.assertEqual(cm.exception.code, 2)

        arg_list = ['--no-config', '-S', 'val=42']
        args = arg_parser.parse_args(arg_list)
        sections = parse_nl_cli(args=args, nl_info_dict=self.nl_info_dict)
        self.assertTrue(check_conflicts(sections))

        arg_list = ['--relpath']
        args = arg_parser.parse_args(arg_list)
        sections = parse_nl_cli(args=args, nl_info_dict=self.nl_info_dict)
        with self.assertRaisesRegex(SystemExit, '2') as cm:
            check_conflicts(sections)
            self.assertEqual(cm.exception.code, 2)

        arg_list = ['--output', 'iraiseValueError']
        args = arg_parser.parse_args(arg_list)
        sections = parse_nl_cli(args=args, nl_info_dict=self.nl_info_dict)
        with self.assertRaisesRegex(SystemExit, '2') as cm:
            check_conflicts(sections)
            self.assertEqual(cm.exception.code, 2)

        arg_list = ['--no-config', '--config', '.coafile']
        args = arg_parser.parse_args(arg_list)
        sections = parse_nl_cli(args=args, nl_info_dict=self.nl_info_dict)
        with self.assertRaisesRegex(SystemExit, '2') as cm:
            check_conflicts(sections)
            self.assertEqual(cm.exception.code, 2)
