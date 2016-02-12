import sys
import os
import unittest
import re
import json
from coalib import coala_json
from coalib.tests.TestUtilities import execute_coala


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
        retval, output = execute_coala(
            coala_json.main, "coala-json", "todos", "-c",
            self.coafile)
        output = json.loads(output)
        self.assertRegex(output["results"]["todos"][0]["message"],
                         r'The line contains the keyword `# \w+`.',
                         "coala-json output should be empty when running "
                         "over its own code. (Target section: todos)")
        self.assertNotEqual(retval,
                            0,
                            "coala-json must return nonzero when running over "
                            "its own code. (Target section: todos)")

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
