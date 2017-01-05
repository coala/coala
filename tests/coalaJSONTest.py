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
        retval, stdout, stderr = execute_coala(
            coala_json.main, 'coala-json', '--help')
        self.assertIn('Use of `coala-json` binary is deprecated', stderr)
        self.assertIn('usage: coala', stdout)

    def test_nonexistent(self):
        retval, stdout, stderr = execute_coala(
            coala.main, 'coala', '--json', '-c', 'nonex', 'test')
        test_text = '{\n  "results": {}\n}\n'
        self.assertEqual(stdout, test_text)
        self.assertRegex(stderr, ".*requested coafile '.*' does not exist. .+")

    def test_find_issues(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--json', '-c', os.devnull,
                                                   '-b', 'LineCountTestBear',
                                                   '-f', re.escape(filename))
            output = json.loads(stdout)
            self.assertEqual(output['results']['cli'][0]['message'],
                             'This file has 1 lines.')
            self.assertEqual(output['results']['cli'][0]
                             ['message_arguments'],
                             {})
            self.assertNotEqual(retval, 0,
                                'coala-json must return nonzero when '
                                'results found')
            self.assertFalse(stderr)

    def test_fail_acquire_settings(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--json', '-c', os.devnull,
                                                   '-b',
                                                   'SpaceConsistencyTestBear')
            test_text = '{\n  "results": {}\n}\n'
            self.assertEqual(stdout, test_text)
            self.assertIn('During execution, we found that some',
                          stderr, 'Missing settings not logged')

    def test_show_all_bears(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '--json', '-B', '-I')
            self.assertEqual(retval, 0)
            output = json.loads(stdout)
            self.assertEqual(len(output['bears']), 6)
            self.assertFalse(stderr)

    def test_show_language_bears(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '--json', '-B', '-l', 'java', '-I')
            self.assertEqual(retval, 0)
            output = json.loads(stdout)
            self.assertEqual(len(output['bears']), 2)
            self.assertFalse(stderr)

    def test_show_bears_attributes(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '--json', '-B', '-I')
            self.assertEqual(retval, 0)
            output = json.loads(stdout)
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
            self.assertFalse(stderr)

    @unittest.mock.patch('coalib.parsing.DefaultArgParser.get_all_bears_names')
    @unittest.mock.patch('coalib.collecting.Collectors.icollect_bears')
    def test_version_conflict_in_collecting_bears(self, import_fn, _):
        with bear_test_module():
            import_fn.side_effect = VersionConflict('msg1', 'msg2')
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '--json', '-B')
            self.assertEqual(retval, 13)

    def test_text_logs(self):
        retval, stdout, stderr = execute_coala(
            coala.main, 'coala', '--json', '-c', 'nonex')
        test_text = '{\n  "results": {}\n}\n'
        self.assertRegex(
            stderr,
            ".*\\[ERROR\\].*The requested coafile '.*' does not exist. .+\n")
        self.assertEqual(stdout, test_text)

    def test_output_file(self):
        with prepare_file(['#todo this is todo'], None) as (lines, filename):
            args = (coala.main, 'coala', '--json', '-c', os.devnull, '-b',
                    'LineCountTestBear', '-f', re.escape(filename),
                    '--log-json')
            retval1, stdout1, stderr1 = execute_coala(*args)
            retval2, stdout2, stderr2 = execute_coala(*(args +
                                                        ('-o', 'file.json')))

        with open('file.json') as fp:
            data = json.load(fp)
        output = json.loads(stdout1)
        self.assertFalse(stderr1)
        # Remove 'time' key from both as we cant compare them
        for log_index in range(len(data['logs'])):
            del data['logs'][log_index]['timestamp']
            del output['logs'][log_index]['timestamp']

        self.assertEqual(data, output)
        self.assertFalse(retval2)
        self.assertFalse(stdout2)
        self.assertFalse(stderr2)
        os.remove('file.json')
