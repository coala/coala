import os
import re
import sys
import unittest

from coalib.tests.TestUtilities import execute_coala
from coalib.misc.ContextManagers import prepare_file
from coalib import coala


class coalaTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_coala(self):
        with prepare_file(["#fixme"], None) as (lines, filename):
            bear = "LineCountBear"
            retval, output = execute_coala(
                             coala.main,
                            "coala", "-c", os.devnull,
                            "--settings", "files=" + re.escape(filename),
                            "bears=" + bear)
        self.assertIn("This file has 1 lines.",
                      output,
                      "The output should report count as 1 lines")
