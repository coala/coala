import os
import re
import sys
import unittest

from coalib import coala, coala_ci
from coala_utils.ContextManagers import prepare_file
from tests.TestUtilities import bear_test_module, execute_coala


class coalaCITest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv
        self.unescaped_coafile = os.path.abspath('./.coafile')
        self.coafile = re.escape(self.unescaped_coafile)

    def tearDown(self):
        sys.argv = self.old_argv

    def test_log(self):
        retval, stdout, stderr = execute_coala(
            coala_ci.main, 'coala-ci', '--help')
        self.assertIn('usage: coala', stdout)
        self.assertIn('Use of `coala-ci` binary is deprecated', stderr)

    def test_nonexistent(self):
        retval, stdout, stderr = execute_coala(
            coala.main, 'coala', '--non-interactive', '-c', 'nonex', 'test')
        self.assertFalse(stdout)
        self.assertRegex(
            stderr,
            ".*\\[ERROR\\].*The requested coafile '.*' does not exist. .+\n")

    def test_find_no_issues(self):
        with bear_test_module(), \
                prepare_file(['#include <a>'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--non-interactive',
                                                   '-c', os.devnull,
                                                   '-f', re.escape(filename),
                                                   '-b',
                                                   'SpaceConsistencyTestBear',
                                                   '--settings',
                                                   'use_spaces=True')
            self.assertIn('Executing section cli', stdout)
            self.assertFalse(stderr)
            self.assertEqual(retval, 0,
                             'coala-ci must return zero when successful')

    def test_find_issues(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--non-interactive',
                                                   '-c', os.devnull,
                                                   '-b', 'LineCountTestBear',
                                                   '-f', re.escape(filename))
            self.assertIn('This file has 1 lines.',
                          stdout,
                          'The output should report count as 1 lines')
            self.assertIn('This result has no patch attached.', stderr)
            self.assertNotEqual(retval, 0,
                                'coala-ci was expected to return non-zero')

    def test_show_patch(self):
        with bear_test_module(), \
             prepare_file(['\t#include <a>'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '--non-interactive',
                '-c', os.devnull,
                '-f', re.escape(filename),
                '-b', 'SpaceConsistencyTestBear',
                '--settings', 'use_spaces=True')
            self.assertIn('Line contains ', stdout)  # Result message is shown
            self.assertIn("Applied 'ShowPatchAction'", stderr)
            self.assertEqual(retval, 5,
                             'coala-ci must return exitcode 5 when it '
                             'autofixes the code.')

    def test_fail_acquire_settings(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--non-interactive', '-b',
                                                   'SpaceConsistencyTestBear',
                                                   '-c', os.devnull)
            self.assertFalse(stdout)
            self.assertIn('During execution, we found that some', stderr)
