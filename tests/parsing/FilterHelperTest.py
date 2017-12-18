import unittest

from coalib import coala
from coalib.parsing.FilterHelper import (
    available_filters, InvalidFilterException)
from tests.TestUtilities import (
    bear_test_module,
    execute_coala,
    TEST_BEARS_COUNT,
)


class FilterHelperTest(unittest.TestCase):

    def test_filter_for_exception(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by', 'some_filter',
                'abc')
            self.assertRaises(InvalidFilterException)

    def test_filter_for_exception_with_multiple_filters(self):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '--filter-by', 'language',
                'C', '--filter-by', 'some_filter', 'abc')
            self.assertRaises(InvalidFilterException)
