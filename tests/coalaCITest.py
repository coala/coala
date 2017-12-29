import os
import sys
import unittest

from coalib import coala, coala_ci
from coala_utils.ContextManagers import prepare_file
from tests.TestUtilities import bear_test_module, execute_coala


class coalaCITest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_log(self, debug=False):
        retval, stdout, stderr = execute_coala(
            coala_ci.main, 'coala-ci', '--help', debug=debug)
        self.assertIn('usage: coala', stdout)
        self.assertIn('Use of `coala-ci` executable is deprecated', stderr)
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
             ".*\\[ERROR\\].*Requested coafile '.*' does not exist")
        self.assertNotEqual(retval, 0,
                            'coala must return nonzero when errors occured')

        retval, stdout, stderr = execute_coala(
            coala.main, 'coala', '-c', 'nonex',
            '--show-bears', '--filter-by-language', 'Python')
        self.assertNotIn(
             stderr,
             "Requested coafile '.coafile' does not exist")

        retval, stdout, stderr = execute_coala(
            coala.main, 'coala', '-c', 'nonex', '--show-bears')
        self.assertIn(
             stderr,
             "Requested coafile '.coafile' does not exist")

    def test_nonexistent_debug(self):
        self.test_nonexistent(debug=True)

    def test_find_no_issues(self, debug=False):
        with bear_test_module(), \
                prepare_file(['#include <a>'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--non-interactive',
                                                   '-c', os.devnull,
                                                   '-f', filename,
                                                   '-b',
                                                   'SpaceConsistencyTestBear',
                                                   '--settings',
                                                   'use_spaces=True',
                                                   debug=debug)
            self.assertEqual('Executing section cli...\n', stdout)
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
                                                   '-f', filename,
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
                '-f', filename,
                '-b', 'SpaceConsistencyTestBear',
                '--settings', 'use_spaces=True',
                debug=debug)
            self.assertIn('Line contains ', stdout)  # Result message is shown
            self.assertIn("Applied 'ShowPatchAction'", stderr)
            self.assertEqual(retval, 5,
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

    def test_limit_files_affirmative(self):
        sample_text = '\t#include <a>'
        with open('match.cpp', 'w') as match, \
                open('noMatch.cpp', 'w') as no_match:
            match.write(sample_text)
            no_match.write(sample_text)
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '--non-interactive',
                '-c', os.devnull,
                '--limit-files', 'match*',
                '-f', 'match.cpp', 'noMatch.cpp',
                '-b', 'SpaceConsistencyTestBear',
                '--settings', 'use_spaces=True')
            os.remove('match.cpp')
            os.remove('noMatch.cpp')
            self.assertIn('match.cpp', stdout)
            self.assertNotIn('noMatch.cpp', stdout)
            self.assertIn("Applied 'ShowPatchAction'", stderr)
            self.assertEqual(retval, 5,
                             'coala must return exitcode 5 when it '
                             'autofixes the code.')

    def test_limit_files_negative(self):
        with bear_test_module(), \
                prepare_file(['\t#include <a>'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '--non-interactive',
                '-c', os.devnull,
                '--limit-files', 'some_pattern',
                '-f', filename,
                '-b', 'SpaceConsistencyTestBear',
                '--settings', 'use_spaces=True',)
            self.assertEqual('Executing section cli...\n', stdout)
            self.assertFalse(stderr)
            self.assertEqual(retval, 0,
                             'coala must return zero when successful')
