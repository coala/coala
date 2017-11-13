import unittest

from coalib import coala
from coalib.parsing.FilterHelper import (
    available_filters, InvalidFilterException)
from tests.TestUtilities import (
    bear_test_module,
    execute_coala,
    TEST_BEARS_COUNT,
)


class FilterTest(unittest.TestCase):

    def test_filter_by_language_c(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by', 'language', 'c')
            self.assertEqual(retval, 0)
            # 1 bear plus 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()), 2)

    def test_filter_by_language_java_can_fix_syntax(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B',
                '--filter-by', 'language', 'java',
                '--filter-by', 'can_fix', 'syntax')
            self.assertEqual(retval, 0)
            # 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()), 1)
            self.assertIn('No bears to show.', stdout)

    def test_filter_by_language_java_can_detect_formatting(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B',
                '--filter-by', 'language', 'java',
                '--filter-by', 'can_detect', 'formatting')
            self.assertEqual(retval, 0)
            # 1 bear plus 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()), 2)

    def test_filter_bylanguage_java_can_detect_syntax(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B',
                '--filter-by-language', 'java',
                '--filter-by', 'can_detect', 'formatting')
            self.assertEqual(retval, 0)
            # 1 bear plus 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()), 2)

    def test_filter_by_can_detect_syntax(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by',
                'can_detect', 'syntax')
            self.assertEqual(retval, 0)
            # 2 bears plus 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()), 3)

    def test_filter_by_can_detect_security(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by',
                'can_detect', 'security')
            self.assertEqual(retval, 0)
            # 1 bear plus 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()), 2)

    def test_filter_by_can_detect_spelling(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by',
                'can_detect', 'spelling')
            self.assertEqual(retval, 0)
            # 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()), 1)
            self.assertIn('No bears to show.', stdout)

    def test_filter_by_can_fix_syntax(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by',
                'can_fix', 'syntax')
            self.assertEqual(retval, 0)
            # 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()), 1)
            self.assertIn('No bears to show.', stdout)

    def test_filter_by_can_fix_redundancy(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by',
                'can_fix', 'redundancy')
            self.assertEqual(retval, 0)
            # 1 bear plus 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()), 2)

    def test_filter_by_unknown(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by', 'unknown', 'arg1')
            self.assertEqual(retval, 2)
            self.assertIn("'unknown' is an invalid filter. Available "
                          'filters: ' + ', '.join(sorted(available_filters)),
                          stdout)

    def test_filter_by_can_fix_null(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by', 'can_fix')
            self.assertEqual(retval, 0)
            # All bears plus 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()),
                             TEST_BEARS_COUNT + 1)

    def test_filter_by_can_detect_null(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by', 'can_detect')
            self.assertEqual(retval, 0)
            # All bear plus 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()),
                             TEST_BEARS_COUNT + 1)
