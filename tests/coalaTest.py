import os
import re
import sys
import unittest
import unittest.mock
from pkg_resources import VersionConflict

from coalib import coala
from coalib.misc.ContextManagers import prepare_file
from tests.test_bears.LineCountTestBear import (
    LineCountTestBear)
from tests.TestUtilities import execute_coala, bear_test_module, raise_error


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
        retval, output = execute_coala(coala.main, "coala", "-A")
        self.assertEqual(retval, 0)
        lines = output.splitlines()
        bear_missing_lines = sum(1 for line in lines if "WARNING" in line)
        self.assertEqual(bear_missing_lines, 0)

        with bear_test_module():
            retval, output = execute_coala(coala.main, "coala", "-A")
            self.assertEqual(retval, 0)

            lines = output.splitlines()
            bear_lines = sum(1 for line in lines if line.startswith(" * "))
            self.assertEqual(bear_lines, 3)

            for line in lines:
                self.assertNotIn("WARNING", line)

            retval, output = execute_coala(
                coala.main, "coala", "-B",
                "-b", "LineCountTestBear, SpaceConsistencyTestBear",
                "-c", os.devnull)
            self.assertEqual(retval, 0)
            self.assertIn(LineCountTestBear.run.__doc__.strip(), output)

    @unittest.mock.patch('coalib.collecting.Collectors.icollect_bears')
    def test_version_conflict_in_collecting_bears(self, import_fn):
        with bear_test_module():
            import_fn.side_effect = (
                lambda *args, **kwargs: raise_error(VersionConflict,
                                                    "msg1", "msg2"))
            retval, output = execute_coala(coala.main, "coala", "-A")
            self.assertEqual(retval, 13)
            self.assertIn(("There is a conflict in the version of a "
                           "dependency you have installed"), output)
            self.assertIn("pip install msg2", output)  # Check recommendation

    @unittest.mock.patch('coalib.collecting.Collectors._import_bears')
    def test_unimportable_bear(self, import_fn):
        with bear_test_module():
            import_fn.side_effect = (
                lambda *args, **kwargs: raise_error(SyntaxError))
            retval, output = execute_coala(coala.main, "coala", "-A")
            self.assertEqual(retval, 0)
            self.assertIn("Unable to collect bears from", output)

            import_fn.side_effect = (
                lambda *args, **kwargs: raise_error(VersionConflict,
                                                    "msg1", "msg2"))
            retval, output = execute_coala(coala.main, "coala", "-A")
            # Note that bear version conflicts don't give exitcode=13,
            # they just give a warning with traceback in log_level debug.
            self.assertEqual(retval, 0)
            self.assertRegex(output,
                             "Unable to collect bears from .* because there "
                             "is a conflict with the version of a dependency "
                             "you have installed")
            self.assertIn("pip install msg2", output)  # Check recommendation
