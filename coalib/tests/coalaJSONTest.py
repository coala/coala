import json
import os
import re
import sys
import unittest

from coalib import coala_json
from coalib.misc.ContextManagers import prepare_file
from coalib.tests.TestUtilities import bear_test_module, execute_coala


class coalaJSONTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_nonexistent(self):
        retval, output = execute_coala(
            coala_json.main, "coala-json", "-c", 'nonex', "test")
        output = json.loads(output)
        self.assertRegex(
            output["logs"][0]["message"],
            "The requested coafile '.*' does not exist.")

    def test_find_issues(self):
        with bear_test_module(), \
                prepare_file(["#fixme"], None) as (lines, filename):
            retval, output = execute_coala(coala_json.main, "coala-json",
                                           "-c", os.devnull,
                                           "-b", "LineCountTestBear",
                                           "-f", re.escape(filename))
            output = json.loads(output)
            self.assertEqual(output["results"]["default"][0]["message"],
                             "This file has 1 lines.")
            self.assertNotEqual(retval, 0,
                                "coala-json must return nonzero when "
                                "results found")

    def test_fail_acquire_settings(self):
        with bear_test_module():
            retval, output = execute_coala(coala_json.main, 'coala-json',
                                           '-c', os.devnull,
                                           '-b', 'SpaceConsistencyTestBear')
            output = json.loads(output)
            found = False
            for msg in output["logs"]:
                if "During execution, we found that some" in msg["message"]:
                    found = True
            self.assertTrue(found, "Missing settings not logged")

    def test_version(self):
        with self.assertRaises(SystemExit):
            execute_coala(coala_json.main, 'coala-json', '-v')

    def test_text_logs(self):
        retval, output = execute_coala(
            coala_json.main, 'coala-json', '--text-logs', '-c', 'nonex')
        self.assertRegex(
            output,
            ".*\\[ERROR\\].*The requested coafile '.*' does not exist.\n")

    def test_output_file(self):
        with prepare_file(["#todo this is todo"], None) as (lines, filename):
            retval, output = execute_coala(coala_json.main, "coala-json",
                                           "-c", os.devnull,
                                           "-b", "LineCountTestBear",
                                           "-f", re.escape(filename))
            exp_retval, exp_output = execute_coala(coala_json.main,
                                                   "coala-json",
                                                   "-c", os.devnull,
                                                   "-b", "LineCountTestBear",
                                                   "-f", re.escape(filename),
                                                   "-o", "file.json")

        with open('file.json') as fp:
            data = json.load(fp)

        output = json.loads(output)

        self.assertEqual(data['logs'][0]['log_level'],
                         output['logs'][0]['log_level'])
        os.remove('file.json')
