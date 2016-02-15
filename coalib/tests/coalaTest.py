import os
import re
import sys
import unittest

from bears.general.LineCountBear import LineCountBear
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

    def test_did_nothing(self):
        retval, output = execute_coala(coala.main, "coala", "-c", os.devnull,
                                       "-S", "default.enabled=false")
        self.assertEqual(retval, 0)
        self.assertIn("No existent section was targeted or enabled", output)

    def test_show_bears(self):
        retval, output = execute_coala(coala.main, "coala", "-A")
        self.assertEqual(retval, 0)
        bear_lines = [i.startswith(" * ") for i in output.split()]
        self.assertGreater(len(bear_lines), 0)

        retval, output = execute_coala(coala.main, "coala", "-B",
                                       "-b", "LineCountBear",
                                       "-c", os.devnull)
        self.assertEqual(retval, 0)
        self.assertIn(LineCountBear.run.__doc__.strip(), output)
