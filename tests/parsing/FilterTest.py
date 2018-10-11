import unittest

from coalib import coala
from coalib.parsing.filters import available_filters
from tests.TestUtilities import (
    bear_test_module,
    execute_coala,
    TEST_BEARS_COUNT,
    C_BEARS_COUNT,
)
from tests.test_bears.TestBear import TestBear
from coalib.parsing.filters.decorators import typed_filter
from coalib.settings.Section import Section, Setting

# C bears plus 1 line holding the closing colour escape sequence.
C_BEARS_COUNT_OUTPUT = C_BEARS_COUNT + 1


class FilterTest(unittest.TestCase):

    def test_filter_by_language_c(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by', 'language', 'c')
            self.assertEqual(retval, 0)
            self.assertEqual(len(stdout.strip().splitlines()),
                             C_BEARS_COUNT_OUTPUT)

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

    def test_section_tags_filter_no_tags(self):
        filter = available_filters['section_tags']

        section = Section('sample')
        section.append(Setting('tags', 'save'))

        flag = filter(section, [])
        self.assertTrue(flag)

    def test_section_tags_filter_true(self):
        filter = available_filters['section_tags']

        section = Section('sample')
        section.append(Setting('tags', 'save'))

        test_bear = TestBear(section, None)
        flag = filter(test_bear, ['save'])
        self.assertTrue(flag)

    def test_section_tags_filter_false(self):
        filter = available_filters['section_tags']

        section = Section('sample')
        section.append(Setting('tags', 'save'))

        test_bear = TestBear(section, None)
        flag = filter(test_bear, ['change'])
        self.assertFalse(flag)


class FilterDecoratorsTest(unittest.TestCase):

    def test_typed_filter_single(self):
        @typed_filter('float')
        def sample_one(x):
            pass

        # Valid Invokes
        sample_one(5.5)
        sample_one(6.4)

        with self.assertRaises(NotImplementedError):
            sample_one([])

        with self.assertRaises(NotImplementedError):
            sample_one('sample')

    def test_typed_filter_multiple(self):
        @typed_filter(('int', 'list'))
        def sample_one(x, y, z):
            pass

        # Valid Invokes
        sample_one(5, 0, 0)
        sample_one(['a'], 0, 'a')

        with self.assertRaises(NotImplementedError):
            sample_one(6.2, 'a', 0)

        with self.assertRaises(NotImplementedError):
            sample_one('sample', 6, -8)

    def test_typed_filter_custom_msg(self):
        @typed_filter(('dict', 'set'), msg='random')
        def sample_func(x):
            pass

        with self.assertRaises(NotImplementedError) as context:
            sample_func(1.25)
        self.assertIn('random', str(context.exception))

        with self.assertRaises(NotImplementedError) as context:
            sample_func('sample')
        self.assertIn('random', str(context.exception))
