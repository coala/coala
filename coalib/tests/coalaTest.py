import os
import re
import sys
import unittest

from coalib import coala
from coalib.misc.ContextManagers import prepare_file
from coalib.tests.test_bears.LineCountTestBear import (
    LineCountTestBear)
from coalib.tests.TestUtilities import execute_coala, bear_test_module


class coalaTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_coala(self):
        with bear_test_module(), \
                prepare_file(["#fixme"], None) as (lines, filename):
            retval, output = execute_coala(
                             coala.main,
                            "coala", "-c", os.devnull,
                            "-f", re.escape(filename),
                            "-b", "LineCountTestBear")
            self.assertIn("This file has 1 lines.",
                          output,
                          "The output should report count as 1 lines")

    def test_did_nothing(self):
        retval, output = execute_coala(coala.main, "coala", "-c", os.devnull,
                                       "-S", "default.enabled=false")
        self.assertEqual(retval, 0)
        self.assertIn("No existent section was targeted or enabled", output)

    def test_show_bears(self):
        with bear_test_module():
            retval, output = execute_coala(coala.main, "coala", "-A")
            self.assertEqual(retval, 0)

            lines = output.splitlines()
            bear_lines = sum(1 for line in lines if line.startswith(" * "))
            self.assertEqual(bear_lines, 2)

            retval, output = execute_coala(
                coala.main, "coala", "-B",
                "-b", "LineCountTestBear, SpaceConsistencyTestBear",
                "-c", os.devnull)
            self.assertEqual(retval, 0)
            self.assertIn(LineCountTestBear.run.__doc__.strip(), output)
