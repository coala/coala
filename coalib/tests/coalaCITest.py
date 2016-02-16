import os
import re
import sys
import unittest
from tempfile import NamedTemporaryFile, TemporaryDirectory

from pyprint.NullPrinter import NullPrinter

from bears.c_languages.IndentBear import IndentBear
from bears.tests.BearTestHelper import generate_skip_decorator
from coalib import coala_ci
from coalib.misc.ContextManagers import make_temp, prepare_file
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.Tagging import get_tag_path
from coalib.tests.TestUtilities import execute_coala


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
        retval, output = execute_coala(
            coala_ci.main, "coala-ci", 'docs', '-c', self.coafile)
        self.assertRegex(output,
                         "(.*Unable to collect bears from.*PyLintBear.*)?",
                         "coala-ci output should be empty when running "
                         "over its own code.")
        self.assertEqual(retval,
                         0,
                         "coala-ci must return zero when running over its "
                         "own code.")

    def test_find_issues(self):
        with prepare_file(["#todo this is todo"], None) as (lines, filename):
            bear = "KeywordBear"
            retval, output = execute_coala(coala_ci.main, "coala-ci", "-c",
                                           os.devnull, "-S",
                                           "ci_keywords=#TODO",
                                           "cs_keywords=#todo",
                                           "bears=" + bear,
                                           "-f", re.escape(filename))
            self.assertIn("The line contains the keyword `#todo`.",
                          output, "coala-ci output should match the keyword\
                          #todo")
            self.assertNotEqual(retval,
                                0, "coala-ci must return nonzero when "
                                "matching `#todo` keyword")

    @generate_skip_decorator(IndentBear)
    def test_fix_patchable_issues(self):
        with prepare_file(["    #include <a>"], None) as (lines, filename):
            bear = "IndentBear"
            retval, output = execute_coala(
                coala_ci.main, "coala-ci", "-c", os.devnull, "--settings",
                "files=" + filename, "bears=" + bear, "autoapply=true",
                "default_actions=" + bear + ":ApplyPatchAction")
            self.assertEqual(retval,
                             5,
                             "coala-ci must return exitcode 5 when it "
                             "autofixes the code.")

    def test_tagging(self):
        log_printer = LogPrinter(NullPrinter())
        execute_coala(coala_ci.main, "coala-ci", 'docs',
                      "-S", "tag=test_tag", "-c", self.coafile)
        tag_path = get_tag_path("test_tag", self.unescaped_coafile, log_printer)
        self.assertTrue(os.path.exists(tag_path))
        execute_coala(coala_ci.main, "coala-ci", 'docs',
                      "-S", "dtag=test_tag", "-c", self.coafile)
        self.assertFalse(os.path.exists(tag_path))

    def test_fail_acquire_settings(self):
        retval, output = execute_coala(coala_ci.main,
                                       "coala-ci",
                                       "-b",
                                       'SpaceConsistencyBear',
                                       '-c',
                                       os.devnull)
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
