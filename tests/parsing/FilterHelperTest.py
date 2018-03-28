import unittest
from coalib.parsing.FilterHelper import apply_filter, apply_filters
from coalib.parsing.InvalidFilterException import InvalidFilterException


class FilterHelperTest(unittest.TestCase):

    def test_apply_filter(self):
        try:
            apply_filter('language', ['C', 'Python'])
            apply_filter('can_detect', ['Syntax', 'Formatting'])
            apply_filter('can_fix', ['Syntax', 'Formatting'])
        except:
            self.assertFalse(True)
        self.assertRaises(InvalidFilterException,
                          apply_filter, 'not supported', ['args'])

    def test_apply_filters(self):
        try:
            apply_filters([['language', 'C', 'Python'],
                           ['can_detect', 'Syntax', 'Formatting'],
                           ['can_fix', 'Syntax', 'Formatting']])
        except:
            self.assertFalse(True)
        self.assertRaises(InvalidFilterException, apply_filters,
                          [['language', 'C', 'Python'],
                           ['not_supported', 'args']])
