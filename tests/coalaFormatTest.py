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
        retval, output = execute_coala(
            coala_format.main, 'coala-format', '--help')
        self.assertIn('Use of `coala-format` binary is deprecated', output)

    def test_line_count(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, output = execute_coala(coala.main, 'coala', '--format',
                                           '-c', os.devnull,
                                           '-f', re.escape(filename),
                                           '-b', 'LineCountTestBear')
            self.assertRegex(output, r'message:This file has [0-9]+ lines.',
                             'coala-format output for line count should '
                             'not be empty')
            self.assertEqual(retval, 1,
                             'coala-format must return exitcode 1 when it '
                             'yields results')
