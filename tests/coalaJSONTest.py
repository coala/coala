import json
import os
import re
import sys
import unittest
import unittest.mock
from pkg_resources import VersionConflict

from coalib import coala, coala_json
from coala_utils.ContextManagers import prepare_file
from tests.TestUtilities import bear_test_module, execute_coala


class coalaJSONTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_deprecation_log(self):
        retval, output = execute_coala(
            coala_json.main, 'coala-json', '--help')
        self.assertIn('Use of `coala-json` binary is deprecated', output)

    def test_nonexistent(self):
        retval, output = execute_coala(
            coala.main, 'coala', '--json', '-c', 'nonex', 'test')
        self.assertRegex(output, ".*requested coafile '.*' does not exist. .+")

    def test_find_issues(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, output = execute_coala(coala.main, 'coala', '--json',
                                           '-c', os.devnull,
                                           '-b', 'LineCountTestBear',
                                           '-f', re.escape(filename))
            output = json.loads(output)
            self.assertEqual(output['results']['default'][0]['message'],
                             'This file has 1 lines.')
            self.assertEqual(output['results']['default'][0]
                             ['message_arguments'],
                             {})
            self.assertNotEqual(retval, 0,
                                'coala-json must return nonzero when '
                                'results found')

    def test_fail_acquire_settings(self):
        with bear_test_module():
            retval, output = execute_coala(coala.main, 'coala', '--json',
                                           '-c', os.devnull,
                                           '-b', 'SpaceConsistencyTestBear')
            self.assertIn('During execution, we found that some',
                          output, 'Missing settings not logged')

    def test_show_all_bears(self):
        with bear_test_module():
            retval, output = execute_coala(coala.main, 'coala', '--json', '-B')
            self.assertEqual(retval, 0)
            output = json.loads(output)
            self.assertEqual(len(output['bears']), 6)

    def test_show_language_bears(self):
        with bear_test_module():
            retval, output = execute_coala(
                coala.main, 'coala', '--json', '-B', '-l', 'java',
                stdout_only=True)
            self.assertEqual(retval, 0)
            output = json.loads(output)
            self.assertEqual(len(output['bears']), 2)

    def test_show_bears_attributes(self):
        with bear_test_module():
            retval, output = execute_coala(coala.main, 'coala', '--json', '-B',
                                           stdout_only=True)
            self.assertEqual(retval, 0)
            output = json.loads(output)
            # Get JavaTestBear
            bear = ([bear for bear in output['bears']
                     if bear['name'] == 'JavaTestBear'][0])
            self.assertTrue(bear, 'JavaTestBear was not found.')
            self.assertEqual(bear['LANGUAGES'], ['java'])
            self.assertEqual(bear['LICENSE'], 'AGPL-3.0')
            self.assertEqual(bear['metadata']['desc'],
                             'Bear to test that collecting of languages works.'
                             )
            self.assertTrue(bear['metadata']['optional_params'])
            self.assertFalse(bear['metadata']['non_optional_params'])

    @unittest.mock.patch('coalib.parsing.DefaultArgParser.get_all_bears_names')
    @unittest.mock.patch('coalib.collecting.Collectors.icollect_bears')
    def test_version_conflict_in_collecting_bears(self, import_fn, _):
        with bear_test_module():
            import_fn.side_effect = VersionConflict('msg1', 'msg2')
            retval, _ = execute_coala(coala.main, 'coala', '--json', '-B')
            self.assertEqual(retval, 13)

    def test_text_logs(self):
        retval, output = execute_coala(
            coala.main, 'coala', '--json', '-c', 'nonex')
        self.assertRegex(
            output,
            ".*\\[ERROR\\].*The requested coafile '.*' does not exist. .+\n")

    def test_output_file(self):
        with prepare_file(['#todo this is todo'], None) as (lines, filename):
            retval, output = execute_coala(coala.main, 'coala', '--json',
                                           '-c', os.devnull,
                                           '-b', 'LineCountTestBear',
                                           '-f', re.escape(filename),
                                           '--log-json',
                                           stdout_only=True)
            execute_coala(coala.main, 'coala', '--json', '-c', os.devnull,
                          '-b', 'LineCountTestBear', '-f', re.escape(filename),
                          '-o', 'file.json', '--log-json')

        with open('file.json') as fp:
            data = json.load(fp)

        output = json.loads(output)
        # Remove 'time' key from both as we cant compare them
        for log_index in range(len(data['logs'])):
            del data['logs'][log_index]['timestamp']
            del output['logs'][log_index]['timestamp']

        self.assertEqual(data, output)
        os.remove('file.json')
