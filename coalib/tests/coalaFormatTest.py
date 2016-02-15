import sys
import os
import unittest

from coalib import coala_format
from coalib.tests.TestUtilities import execute_coala
from coalib.misc.ContextManagers import prepare_file


class coalaFormatTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_line_count(self):
        with prepare_file(["#fixme"], None) as (lines, filename):
            bear = "LineCountBear"
            retval, output = execute_coala(
                             coala_format.main,
                            "coala-format", "-c", os.devnull,
                            "--settings", "files=" + filename,
                            "bears=" + bear)
            self.assertRegex(output,
                             r'msg:This file has [0-9]+ lines.',
                             "coala-format output for line count should"
                             " not be empty")
            self.assertEqual(retval,
                             1,
                             "coala-format must return exitcode 1 when it "
                             "yields results")
