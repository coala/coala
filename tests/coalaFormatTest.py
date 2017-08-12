import os
import re
import sys
import unittest

from coalib import coala, coala_format
from coala_utils.ContextManagers import prepare_file
from tests.TestUtilities import bear_test_module, execute_coala


class coalaFormatTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_deprecation_log(self):
        retval, stdout, stderr = execute_coala(
            coala_format.main, 'coala-format', '--help')
        self.assertIn('Use of `coala-format` executable is deprecated', stderr)
        self.assertIn('usage: coala', stdout)

    def test_line_count(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--format', '-c',
                                                   os.devnull, '-f',
                                                   re.escape(filename),
                                                   '-b', 'LineCountTestBear')
            self.assertRegex(stdout, r'message:This file has [0-9]+ lines.',
                             'coala-format output for line count should '
                             'not be empty')
            self.assertEqual(retval, 1,
                             'coala-format must return exitcode 1 when it '
                             'yields results')
            self.assertFalse(stderr)

    def test_format_ci_combination(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(coala.main, 'coala',
                                                   '--format', '--ci', '-c',
                                                   os.devnull, '-f',
                                                   re.escape(filename),
                                                   '-b', 'LineCountTestBear')
            self.assertRegex(stdout, r'message:This file has [0-9]+ lines.',
                             'coala --format --ci output for line count should '
                             'not be empty')
            self.assertEqual(retval, 1,
                             'coala --format --ci must return exitcode 1 when '
                             'it yields results')
            self.assertFalse(stderr)

    def test_format_show_bears(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by', 'language',
                'java', '-I', '--format')
        self.assertEqual(retval, 0)
        self.assertFalse(stderr)
        self.assertRegex(stdout, 'name:.*:can_detect:.*:can_fix:.*:'
                                 'description:.*')
