import os
import unittest
import logging
from unittest import mock
from coalib.parsing.DefaultArgParser import default_arg_parser

from coalib.nestedlib.NlCore import (get_parser,
                                     get_nl_coala_sections,
                                     nested_language,
                                     remove_position_markers,
                                     get_temp_file_content,
                                     generate_linted_file_dict,
                                     get_original_file_path,
                                     apply_patches_to_nl_file)
from coalib.nestedlib.parsers.PyJinjaParser import PyJinjaParser
from coalib.nestedlib.NlInfoExtractor import generate_arg_list


class NlCoreTest(unittest.TestCase):

    def setUp(self):
        self.arg_parser = default_arg_parser()
        self.test_dir_path = os.path.abspath(__file__ + '/../..')
        self.test_bear_path = os.path.join(self.test_dir_path, 'test_bears')
        self.arg_list = ['--no-config', '--handle-nested',
                         '--bears=PEP8TestBear,Jinja2TestBear',
                         '--languages=python,jinja2', '--files=test.py',
                         '--bear-dirs='+self.test_bear_path
                         ]
        self.args = self.arg_parser.parse_args(self.arg_list)

    def test_get_parser_PyJinjaParser(self):
        uut_lang_comb = 'python,jinja2'
        parser = get_parser(uut_lang_comb)
        assert isinstance(parser, PyJinjaParser)

        # Test for parser not found
        uut_lang_comb = 'python,cpp'
        logger = logging.getLogger()
        with self.assertLogs(logger, 'ERROR') as cm:
            with self.assertRaises(SystemExit):
                parser = get_parser(uut_lang_comb)
                self.assertRegex(
                    cm.output[0],
                    'No Parser found for the languages combination')

    def test_get_nl_coala_sections(self):

        self.maxDiff = None
        uut_nl_sections = get_nl_coala_sections(args=self.args)
        self.assertEqual(
            str(uut_nl_sections['cli_nl_section: test.py_nl_python']),
            "cli_nl_section: test.py_nl_python {targets : '', " +
            "bear_dirs : '" + self.test_bear_path + "', " +
            "bears : 'PEP8TestBear', files : 'test.py_nl_python', " +
            "handle_nested : 'True', languages : 'python,jinja2', " +
            "no_config : 'True', file_lang : 'python', " +
            "orig_file_name : 'test.py'}")

        # When arg_list is passed
        uut_nl_sections = get_nl_coala_sections(arg_list=self.arg_list)
        self.assertEqual(
            str(uut_nl_sections['cli_nl_section: test.py_nl_python']),
            "cli_nl_section: test.py_nl_python {targets : '', " +
            "bear_dirs : '" + self.test_bear_path + "', " +
            "bears : 'PEP8TestBear', files : 'test.py_nl_python', " +
            "handle_nested : 'True', languages : 'python,jinja2', " +
            "no_config : 'True', file_lang : 'python', " +
            "orig_file_name : 'test.py'}")

    def test_nested_language(self):
        # When --handle-nested is present
        handle_nested = nested_language(args=self.args)
        self.assertTrue(handle_nested)

        # When --handle-nested is passed via arg_list
        handle_nested = nested_language(arg_list=self.arg_list)
        self.assertTrue(handle_nested)

        # When --handle-nested is not present
        handle_nested = nested_language(arg_list=[])
        self.assertFalse(handle_nested)

    def test_get_temp_file_content(self):
        nl_file_dicts = {
            'cli_nl_section: test.py_nl_python':
                {'test.py_nl_python': ['!!! Start Nl Section: 1\n', '\n', '\n',
                                       'def hello():\n', '\n', '\n',
                                       '!!! End Nl Section: 1\n', '\n', '\n',
                                       ]},

            'cli_nl_section: test.py_nl_jinja2':
                {'test.py_nl_jinja2': ['\n',
                                       '!!! Start Nl Section: 2\n',
                                       '    {{ x }} asdasd {{ Asd }}\n',
                                       '!!! End Nl Section: 2\n',
                                       ]},
        }

        uut_temp_file_name = 'test.py_nl_python'
        expected_file_content = ['!!! Start Nl Section: 1\n', '\n', '\n',
                                 'def hello():\n', '\n', '\n',
                                 '!!! End Nl Section: 1\n', '\n', '\n',
                                 ]

        file_content = get_temp_file_content(nl_file_dicts,
                                             uut_temp_file_name)

        self.assertEqual(expected_file_content, file_content)

    def test_remove_position_markers(self):

        uut_temp_file_contents = ['!!! Start Nl Section: 1\n',
                                  '\n',
                                  'print("Hello world")\n',
                                  'def hello():\n',
                                  '\n',
                                  '!!! End Nl Section: 1\n',
                                  '\n']

        expected_output = {1: ['\n',
                               'print("Hello world")\n',
                               'def hello():\n',
                               '\n'
                               ]
                           }

        section_index_lines_dict = remove_position_markers(
                                            uut_temp_file_contents)

        self.assertEqual(expected_output, section_index_lines_dict)

    def test_generate_linted_file_dict(self):
        linted_temp_nl_file_dicts = {
            'cli_nl_section: test.py_nl_python':
                {'test.py_nl_python': ['!!! Start Nl Section: 1\n',
                                       'def hello():\n',
                                       '\n',
                                       '\n',
                                       '!!! End Nl Section: 1\n',
                                       '\n',
                                       '\n',
                                       ]},

            'cli_nl_section: test.py_nl_jinja2':
                {'test.py_nl_jinja2': ['\n',
                                       '!!! Start Nl Section: 2\n',
                                       '    {{ x }} asdasd {{ Asd }}\n',
                                       '!!! End Nl Section: 2\n',
                                       ]},

            'cli_nl_section: test2.py_nl_python':
                {'test2.py_nl_python': ['!!! Start Nl Section: 1\n',
                                        'print("Hello Thanos)\n',
                                        '!!! End Nl Section: 1\n',
                                        ]},

            'cli_nl_section: test2.py_nl_jinja2':
                {'test2.py_nl_jinja2': ['\n',
                                        '!!! Start Nl Section: 2',
                                        '{% set x = {{var}} %}\n',
                                        '!!! End Nl Section: 2\n',
                                        ]},

        }

        nl_file_info_dict = {'test.py': {
                                        'python': 'test.py_nl_python',
                                        'jinja2': 'test.py_nl_jinja2'
                                         },

                             'test2.py': {
                                        'python': 'test2.py_nl_python',
                                        'jinja2': 'test2.py_nl_jinja2'
                                      }
                             }

        expected_ouput = {
                'test.py': ['def hello():\n',
                            '\n',
                            '\n',
                            '    {{ x }} asdasd {{ Asd }}\n',
                            ],

                'test2.py': ['print("Hello Thanos)\n',
                             '{% set x = {{var}} %}\n'
                             ]

            }

        linted_file_dict = generate_linted_file_dict(
                                            linted_temp_nl_file_dicts,
                                            nl_file_info_dict)

        self.assertEqual(expected_ouput, linted_file_dict)

    def test_get_original_file_path(self):

        config_path = os.path.abspath(os.path.dirname(__file__))

        # When the filename is present in nl section
        os.path.join(config_path, 'test.py')

        uut_arg_list = ['--no-config', '--handle-nested',
                        '--bears=PEP8TestBear,Jinja2TestBear',
                        '--languages=python,jinja2',
                        '--files=test.py',
                        '--bear-dirs='+self.test_bear_path
                        ]
        uut_args = self.arg_parser.parse_args(uut_arg_list)
        uut_nl_sections = get_nl_coala_sections(uut_args)
        file_path = get_original_file_path(uut_nl_sections, 'test.py')
        expected_file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__) + '/../..'), 'test.py')
        self.assertEqual(expected_file_path, file_path)

        # When the filename is not present in nl section
        os.path.join(config_path, 'test2.py')

        uut_arg_list = ['--no-config', '--handle-nested',
                        '--bears=PEP8TestBear,Jinja2TestBear',
                        '--languages=python,jinja2',
                        '--files=test2.py',
                        '--bear-dirs='+self.test_bear_path
                        ]
        uut_args = self.arg_parser.parse_args(uut_arg_list)
        uut_nl_sections = get_nl_coala_sections(uut_args)
        file_path = get_original_file_path(uut_nl_sections, 'test.py')
        expected_file_path = ''
        self.assertEqual(expected_file_path, file_path)

    def test_apply_patches_to_nl_file(self):
        # The path for test file

        linted_temp_nl_file_dicts = {
            'cli_nl_section: test.py_nl_python':
            {'test.py_nl_python': ['!!! Start Nl Section: 1\n',
                                   'print("Hello Thanos")\n',
                                   '!!! End Nl Section: 1\n',
                                   ]},

            'cli_nl_section: test.py_nl_jinja2':
            {'test.py_nl_jinja2': ['\n',
                                   '!!! Start Nl Section: 2',
                                   '{% set x = {{var}} %}\n',
                                   '!!! End Nl Section: 2\n',
                                   ]}
            }

        uut_arg_list = ['--no-config', '--handle-nested',
                        '--bears=PEP8TestBear,Jinja2TestBear',
                        '--languages=python,jinja2',
                        '--files=test.py',
                        '--bear-dirs='+self.test_bear_path
                        ]

        uut_args = self.arg_parser.parse_args(uut_arg_list)
        uut_nl_sections = get_nl_coala_sections(uut_args)

        expected_linted_file_dict = {'test.py':
                                     ['print("Hello Thanos")\n',
                                      '{% set x = {{var}} %}\n']}

        import_path = 'coalib.nestedlib.NlCore.write_patches_to_orig_nl_file'

        # When args and nl_info_dict is None
        with mock.patch(
                import_path,
                return_value=expected_linted_file_dict) as write_patches_func:
            linted_file_dict = apply_patches_to_nl_file(
                nl_file_dicts=linted_temp_nl_file_dicts,
                sections=uut_nl_sections,
                arg_list=uut_arg_list,
                args=None,
                nl_info_dict=None)

            self.assertEqual(write_patches_func.call_count, 1)

            self.assertEqual(expected_linted_file_dict,
                             linted_file_dict)

        # Another tests where args and nl_info_dict is not none
        uut_args = self.arg_parser.parse_args(uut_arg_list)
        uut_arg_list, uut_nl_info_dict = generate_arg_list(uut_args)

        with mock.patch(
                import_path,
                return_value=expected_linted_file_dict) as write_patches_func:
            linted_file_dict = apply_patches_to_nl_file(
                nl_file_dicts=linted_temp_nl_file_dicts,
                sections=uut_nl_sections,
                args=uut_args,
                nl_info_dict=uut_nl_info_dict)

            self.assertEqual(write_patches_func.call_count, 1)

            self.assertEqual(expected_linted_file_dict,
                             linted_file_dict)
