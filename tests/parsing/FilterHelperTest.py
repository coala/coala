import unittest

from coalib.parsing.FilterHelper import (
    apply_filter,
    apply_filters,
    is_valid_filter,
    _filter_section_bears
)
from coalib.parsing.filters import available_filters
from coalib.parsing.InvalidFilterException import InvalidFilterException
from coalib.settings.ConfigurationGathering import get_all_bears
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.settings.Section import Section, Setting
from coalib.parsing.FilterHelper import (
    collect_filters, _apply_section_filter)


class MockObjMap:
    def __init__(self, **kargs):
        for k, v in kargs.items():
            setattr(self, k, v)


class FilterHelperTest(unittest.TestCase):

    def test_apply_filter_exception(self):
        with self.assertRaises(InvalidFilterException) as exp:
            apply_filter('unknown', ['args'])

        message = str(exp.exception)
        self.assertEqual("'unknown' is an invalid filter. Available filters: "
                         + ', '.join(sorted(available_filters)), message)

    def test_is_valid_filter_true(self):
        filter_result = is_valid_filter('can_detect')
        self.assertTrue(filter_result)

    def test_is_valid_filter_false(self):
        filter_result = is_valid_filter('wrong_filter')
        self.assertFalse(filter_result)

    def test_filter_section_bears(self):
        local_bears = get_all_bears()[0]
        filter_args = {'c', 'java'}
        result_for_filter_section = _filter_section_bears(
            local_bears, filter_args, 'language')
        self.assertIsNotNone(result_for_filter_section)

    def test_apply_filter(self):
        apply_filter_result = apply_filter('language', ['c', 'java'])
        self.assertIsNotNone(apply_filter_result)

    def test_apply_filters(self):
        apply_filters_result = apply_filters([('language', 'C', 'Python'),
                                              ('can_fix', 'syntax')])
        self.assertIsNotNone(apply_filters_result)

    def test_apply_filters(self):
        section_one = Section('apply')
        section_one.append(Setting('tags', 'save'))

        section_two = Section('filters')
        section_two.append(Setting('tags', 'change'))

        filtered = apply_filters([('section_tags', 'save')],
                                 sections=[section_one, section_two, ])

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, 'apply')

    def test_apply_section_filters(self):
        section_one = Section('apply')
        section_one.append(Setting('tags', 'save'))

        filtered = _apply_section_filter(
            'section_tags', [], [section_one])

        self.assertEqual(filtered, [section_one])

    def test_apply_section_filter_exception(self):
        with self.assertRaises(InvalidFilterException) as exp:
            _apply_section_filter('unknown', ['args'], [])

    def test_collect_filters_args(self):
        args = MockObjMap(filter_by=None)
        self.assertEqual(collect_filters(args), [])

        args = MockObjMap(filter_by=[['sample', 'arg0']])
        self.assertEqual(collect_filters(args), [['sample', 'arg0']])

    def test_collect_filters_arg_list_default_parser(self):
        collected = collect_filters(None, [])
        self.assertEqual(collected, [])

        collected = collect_filters(None, ['--filter-by', 'sample', 'arg'])
        self.assertEqual(collected, [['sample', 'arg']])

    def test_collect_filters_arg_list_custom_parser(self):
        collected = collect_filters(None, [], default_arg_parser())
        self.assertEqual(collected, [])

        collected = collect_filters(None,
                                    ['--filter-by', 'sample', 'arg'],
                                    default_arg_parser())
        self.assertEqual(collected, [['sample', 'arg']])
