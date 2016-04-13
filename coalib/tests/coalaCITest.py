import os
import re
import sys
import unittest
from tempfile import NamedTemporaryFile, TemporaryDirectory

from pyprint.NullPrinter import NullPrinter

from coalib import coala_ci
from coalib.misc.ContextManagers import make_temp, prepare_file
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.Tagging import get_tag_path
from coalib.tests.TestUtilities import bear_test_module, execute_coala


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
            ".*\\[ERROR\\].*The requested coafile '.*' does not exist.\n")

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

    def test_fix_patchable_issues(self):
        with bear_test_module(), \
                prepare_file(["\t#include <a>"], None) as (lines, filename):
            retval, output = execute_coala(
                coala_ci.main, "coala-ci",
                "-c", os.devnull,
                "-f", re.escape(filename),
                "-b", "SpaceConsistencyTestBear",
                "--settings", "autoapply=true", "use_spaces=True",
                "default_actions=SpaceConsistencyTestBear:ApplyPatchAction")
            self.assertIn("Applied 'ApplyPatchAction'", output)
            self.assertEqual(retval, 5,
                             "coala-ci must return exitcode 5 when it "
                             "autofixes the code.")

    def test_tagging(self):
        with bear_test_module(), \
                prepare_file(["\t#include <a>"], None) as (lines, filename):
            log_printer = LogPrinter(NullPrinter())
            execute_coala(coala_ci.main, "coala-ci", "default",
                          "-c", self.coafile,
                          "-f", re.escape(filename),
                          "-b", "SpaceConsistencyTestBear",
                          "-S", "tag=test_tag")
            tag_path = get_tag_path("test_tag",
                                    self.unescaped_coafile,
                                    log_printer)
            self.assertTrue(os.path.exists(tag_path))
            execute_coala(coala_ci.main, "coala-ci", "default",
                          "-c", self.coafile,
                          "-f", re.escape(filename),
                          "-b", "SpaceConsistencyTestBear",
                          "-S", "dtag=test_tag")
            self.assertFalse(os.path.exists(tag_path))

    def test_fail_acquire_settings(self):
        with bear_test_module():
            retval, output = execute_coala(coala_ci.main, "coala-ci",
                                           "-b", 'SpaceConsistencyTestBear',
                                           '-c', os.devnull)
            self.assertIn("During execution, we found that some", output)

    def test_coala_delete_orig(self):
        with TemporaryDirectory() as tempdir,\
             NamedTemporaryFile(suffix='.orig',
                                dir=tempdir,
                                delete=False) as orig_file,\
             make_temp(suffix='.coafile', prefix='', dir=tempdir) as coafile,\
             make_temp(dir=tempdir) as unrelated_file:
            orig_file.close()
            execute_coala(coala_ci.main, "coala-ci",
                          "-c", re.escape(coafile))
            self.assertFalse(os.path.isfile(orig_file.name))
            self.assertTrue(os.path.isfile(unrelated_file))
