import os
import unittest
import logging
from copy import deepcopy


from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.nestedlib.NlInfoExtractor import (nl_info_dict,
                                              check_lang_support,
                                              generate_lang_bear_dict,
                                              generate_arg_list, get_orig_file,
                                              get_temp_file_lang)


class NlInfoExtractor(unittest.TestCase):

    def setUp(self):
        self.arg_parser = default_arg_parser()
        self.test_dir_path = os.path.abspath(__file__ + '/../..')
        self.test_bear_path = os.path.join(self.test_dir_path, 'test_bears')
        # Both the upper case and lower case is supported in `languages`
        # argument
        self.args = self.arg_parser.parse_args([
                                '-f', 'test.py.jj2,test2.py.jj2',
                                '-b',
                                'PEP8TestBear,Jinja2TestBear,LineCountTestBear',
                                '--handle-nested', '--languages',
                                'PYTHON,Jinja2',
                                '--bear-dirs='+self.test_bear_path])

    def test_nl_info_dict(self):

        nl_info_dictionay = nl_info_dict(self.args)
        expected_dictionary = {
            'bears': ['PEP8TestBear', 'Jinja2TestBear', 'LineCountTestBear'],
            'bear_dirs': [self.test_bear_path],
            'files': ['test.py.jj2', 'test2.py.jj2'],
            'languages': ['python', 'jinja2'],
            'lang_bear_dict': {
                             'jinja2': ['Jinja2TestBear', 'LineCountTestBear'],
                             'python': ['PEP8TestBear', 'LineCountTestBear']

            }
        }

        self.assertEqual(nl_info_dictionay, expected_dictionary)

    def test_check_lang_support(self):
        lang_list = ['PYTHON', 'JINAJA21']
        # If wrong languages are passed - Exit from the execution
        logger = logging.getLogger()
        with self.assertLogs(logger, 'ERROR') as cm:
            with self.assertRaises(SystemExit):
                check_lang_support(lang_list)
                self.assertRegex(
                    cm.output[0],
                    'The language combination are not supported. '
                    'Please check if the languages are provided with'
                    'the correct names')

        uut_lang_list = ['PYTHON', 'JiNjA2']
        check_lang_support(uut_lang_list)

    def test_generate_lang_bear_dict(self):
        nl_info_dictionay = nl_info_dict(self.args)
        uut_lang_bear_dict = generate_lang_bear_dict(nl_info_dictionay)
        expected_lang_bear_dict = {
                             'jinja2': ['Jinja2TestBear', 'LineCountTestBear'],
                             'python': ['PEP8TestBear', 'LineCountTestBear']

                        }
        self.assertEqual(uut_lang_bear_dict, expected_lang_bear_dict)

    """
    def test_bear_dirs(self):
        section = Section('section', None)
        empty_bear_dirs_len = len(section.bear_dirs())
        section.append(Setting('bear_dirs', 'test1, test2 (1)'))
        self.assertEqual(len(section.bear_dirs()), empty_bear_dirs_len + 2)
        # Verify if bear directories are properly escaped
        root = get_config_directory(section)
        path = os.path.join(glob_escape(root), glob_escape('test2 (1)'), '**')
        self.assertIn(path, section.bear_dirs())
    """

    def test_generate_arg_list(self):

        self.maxDiff = None

        arg_list = []
        # First Argument object
        arg1 = deepcopy(self.args)
        arg1.__dict__['files'] = 'test.py.jj2_nl_python'
        arg1.__dict__['bears'] = 'PEP8TestBear,LineCountTestBear'
        arg_list.append(arg1)

        # Second Argument object
        arg2 = deepcopy(self.args)
        arg2.__dict__['files'] = 'test2.py.jj2_nl_python'
        arg2.__dict__['bears'] = 'PEP8TestBear,LineCountTestBear'
        arg_list.append(arg2)

        # Third Argument Object
        arg3 = deepcopy(self.args)
        arg3.__dict__['files'] = 'test.py.jj2_nl_jinja2'
        arg3.__dict__['bears'] = 'Jinja2TestBear,LineCountTestBear'
        arg_list.append(arg3)

        # Fourth Argument Object
        arg4 = deepcopy(self.args)
        arg4.__dict__['files'] = 'test2.py.jj2_nl_jinja2'
        arg4.__dict__['bears'] = 'Jinja2TestBear,LineCountTestBear'
        arg_list.append(arg4)

        # Expected nl_info_dict
        expected_nl_info = {
            'bears': ['PEP8TestBear', 'Jinja2TestBear', 'LineCountTestBear'],
            'bear_dirs': [self.test_bear_path],
            'files': ['test.py.jj2', 'test2.py.jj2'],
            'lang_bear_dict': {
                                'jinja2': ['Jinja2TestBear',
                                           'LineCountTestBear'],
                                'python': ['PEP8TestBear', 'LineCountTestBear']
                            },
            'languages': ['python', 'jinja2'],
            'nl_file_info': {'test.py.jj2': {
                                            'python': 'test.py.jj2_nl_python',
                                            'jinja2': 'test.py.jj2_nl_jinja2'
                                        },

                             'test2.py.jj2': {
                                            'python': 'test2.py.jj2_nl_python',
                                            'jinja2': 'test2.py.jj2_nl_jinja2'
                                        }
                             }
        }

        uut_arg_list, uut_nl_info = generate_arg_list(self.args)

        self.assertEqual(uut_arg_list, arg_list)
        self.assertEqual(uut_nl_info, expected_nl_info)

    def test_get_orig_file(self):
        uut_arg_list, uut_nl_info = generate_arg_list(self.args)
        uut_temp_file_name = 'test2.py.jj2_nl_python'
        uut_file = get_orig_file(uut_nl_info, uut_temp_file_name)
        self.assertEqual(uut_file, 'test2.py.jj2')

    def test_get_temp_file_lang(self):
        uut_arg_list, uut_nl_info = generate_arg_list(self.args)
        uut_temp_file_name = 'test.py.jj2_nl_jinja2'
        uut_temp_file_lang = get_temp_file_lang(
            uut_nl_info, uut_temp_file_name)
        self.assertEqual(uut_temp_file_lang, 'jinja2')
