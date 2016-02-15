import sys
import os
import unittest
import re
import json

from coalib import coala_json
from coalib.tests.TestUtilities import execute_coala
from coalib.misc.ContextManagers import prepare_file


class coalaJSONTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv
        self.unescaped_coafile = os.path.abspath("./.coafile")
        self.coafile = re.escape(self.unescaped_coafile)

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
        with prepare_file(["#todo this is todo"], None) as (lines, filename):
            bear = "KeywordBear"
            retval, output = execute_coala(coala_json.main, "coala-json", "-c",
                                           os.devnull, "-S",
                                           "ci_keywords=#TODO",
                                           "cs_keywords=#todo",
                                           "bears=" + bear, "-f", filename)
            output = json.loads(output)
            self.assertEqual(output["results"]["default"][0]["message"],
                             "The line contains the keyword `#todo`.",
                             "coala-json output should match the keyword #todo")
            self.assertNotEqual(retval,
                                0, "coala-json must return nonzero when "
                                "matching `#todo` keyword")

    def test_fail_acquire_settings(self):
        retval, output = execute_coala(
            coala_json.main, 'coala-json', '-b',
            'SpaceConsistencyBear', '-c', os.devnull)
        output = json.loads(output)
        found = False
        for msg in output["logs"]:
            if "During execution, we found that some" in msg["message"]:
                found = True
        self.assertTrue(found)

    def test_version(self):
        retval, output = execute_coala(coala_json.main, 'coala-json', '-v')
        self.assertEquals(retval, 0)
        self.assertNotIn("{", output)

    def test_text_logs(self):
        retval, output = execute_coala(
            coala_json.main, 'coala-json', '--text-logs', '-c', 'nonex')
        self.assertRegex(
            output,
            ".*\\[ERROR\\].*The requested coafile '.*' does not exist.\n")
