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

    def test_log(self, debug=False):
        retval, stdout, stderr = execute_coala(
            coala_ci.main, 'coala-ci', '--help', debug=debug)
        self.assertIn('usage: coala', stdout)
        self.assertIn('Use of `coala-ci` binary is deprecated', stderr)
        self.assertEqual(retval, 0,
                         'coala must return zero when successful')

    def test_log_debug(self):
        self.test_log(debug=True)

    def test_nonexistent(self, debug=False):
        retval, stdout, stderr = execute_coala(
            coala.main, 'coala', '--non-interactive', '-c', 'nonex', 'test')
        self.assertFalse(stdout)
        self.assertRegex(
            stderr,
            '.*\\[ERROR\\].+\n')
        self.assertNotEqual(retval, 0,
                            'coala must return nonzero when errors occured')

    def test_nonexistent_debug(self):
        self.test_nonexistent(debug=True)

    def test_find_no_issues(self, debug=False):
        with bear_test_module(), \
                prepare_file(['#include <a>'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--non-interactive',
                                                   '-c', os.devnull,
                                                   '-f', re.escape(filename),
                                                   '-b',
                                                   'SpaceConsistencyTestBear',
                                                   '--settings',
                                                   'use_spaces=True',
                                                   debug=debug)
            self.assertIn('', stdout)
            if not debug:
                self.assertFalse(stderr)
            else:
                # in debug mode, log_level is also set to DEBUG, causing
                # stderr output
                self.assertTrue(stderr)
            self.assertEqual(retval, 0,
                             'coala must return zero when successful')

    def test_find_no_issues_debug(self):
        self.test_find_no_issues(debug=True)

    def test_find_issues(self, debug=False):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--non-interactive',
                                                   '-c', os.devnull,
                                                   '-b', 'LineCountTestBear',
                                                   '-f', re.escape(filename),
                                                   debug=debug)
            self.assertIn('This file has 1 lines.',
                          stdout,
                          'The output should report count as 1 lines')
            self.assertIn('This result has no patch attached.', stderr)
            self.assertNotEqual(retval, 0,
                                'coala must return nonzero when errors occured')

    def test_find_issues_debug(self):
        self.test_find_issues(debug=True)

    def test_show_patch(self, debug=False):
        with bear_test_module(), \
             prepare_file(['\t#include <a>'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '--non-interactive',
                '-c', os.devnull,
                '-f', re.escape(filename),
                '-b', 'SpaceConsistencyTestBear',
                '--settings', 'use_spaces=True',
                debug=debug)
            self.assertIn('', stdout)  # Result message is shown
            self.assertIn('execute action', stderr)
            self.assertEqual(retval, 255,
                             'coala must return exitcode 5 when it '
                             'autofixes the code.')

    def test_show_patch_debug(self):
        self.test_show_patch(debug=True)

    def test_fail_acquire_settings(self, debug=False):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--non-interactive', '-b',
                                                   'SpaceConsistencyTestBear',
                                                   '-c', os.devnull,
                                                   debug=debug)
            self.assertFalse(stdout)
            self.assertIn('During execution, we found that some', stderr)
            self.assertNotEqual(retval, 0,
                                'coala was expected to return non-zero')

    def test_fail_acquire_settings_debug(self):
        with self.assertRaisesRegex(
                AssertionError,
                r'During execution, we found that some required settings '
                r'were not provided.'
        ):
            self.test_fail_acquire_settings(debug=True)
