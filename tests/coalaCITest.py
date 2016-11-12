import os
import re
import sys
import unittest

from coalib import coala_ci
from coalib.misc.ContextManagers import prepare_file
from tests.TestUtilities import bear_test_module, execute_coala


class coalaCITest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv
        self.unescaped_coafile = os.path.abspath("./.coafile")
        self.coafile = re.escape(self.unescaped_coafile)

    def tearDown(self):
        sys.argv = self.old_argv

    def test_nonexistent(self):
        retval, output = execute_coala(
            coala_ci.main, "coala-ci", "-c", 'nonex', "test")
        self.assertRegex(
            output,
            ".*\\[ERROR\\].*The requested coafile '.*' does not exist. .+\n")

    def test_find_no_issues(self):
        with bear_test_module(), \
                prepare_file(["#include <a>"], None) as (lines, filename):
            retval, output = execute_coala(coala_ci.main, "coala-ci",
                                           '-c', os.devnull,
                                           '-f', re.escape(filename),
                                           '-b', 'SpaceConsistencyTestBear',
                                           "--settings", "use_spaces=True")
            self.assertIn("Executing section Default", output)
            self.assertEqual(retval, 0,
                             "coala-ci must return zero when successful")

    def test_find_issues(self):
        with bear_test_module(), \
                prepare_file(["#fixme"], None) as (lines, filename):
            retval, output = execute_coala(coala_ci.main, "coala-ci",
                                           "-c", os.devnull,
                                           "-b", "LineCountTestBear",
                                           "-f", re.escape(filename))
            self.assertIn("This file has 1 lines.",
                          output,
                          "The output should report count as 1 lines")
            self.assertNotEqual(retval, 0,
                                "coala-ci was expected to return non-zero")

    def test_show_patch(self):
        with bear_test_module(), \
             prepare_file(["\t#include <a>"], None) as (lines, filename):
            retval, output = execute_coala(
                coala_ci.main, "coala-ci",
                "-c", os.devnull,
                "-f", re.escape(filename),
                "-b", "SpaceConsistencyTestBear",
                "--settings", "use_spaces=True")
            self.assertIn("Line contains ", output)  # Result message is shown
            self.assertIn("Applied 'ShowPatchAction'", output)
            self.assertEqual(retval, 5,
                             "coala-ci must return exitcode 5 when it "
                             "autofixes the code.")

    def test_fail_acquire_settings(self):
        with bear_test_module():
            retval, output = execute_coala(coala_ci.main, "coala-ci",
                                           "-b", 'SpaceConsistencyTestBear',
                                           '-c', os.devnull)
            self.assertIn("During execution, we found that some", output)
