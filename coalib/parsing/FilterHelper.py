from coalib.output.printers.LogPrinter import LogPrinter

from coalib.parsing.InvalidFilterException import InvalidFilterException

from coalib.parsing.filters.LanguageFilter import language_filter
from coalib.parsing.filters.CanDetectFilter import can_detect_filter
from coalib.parsing.filters.CanFixFilter import can_fix_filter


class FilterHelper:
    available_filters = {'language': language_filter,
                         'can_detect': can_detect_filter,
                         'can_fix': can_fix_filter}

    @classmethod
    def get_all_filters_str(cls, sep=', '):
        return sep.join(sorted(cls.available_filters))

    @classmethod
    def is_valid_filter(cls, filter):
        return filter in cls.available_filters

    @classmethod
    def get_filtered_bears(cls, filter, args, all_bears=None):
        if all_bears is None:
            from coalib.settings.ConfigurationGathering import (
                get_all_bears)
            all_bears = get_all_bears(LogPrinter())
        if not cls.is_valid_filter(filter):
            raise InvalidFilterException('{!r} is an invalid filter. '
                                         'Available filters: {}'.format(
                                             filter, cls.get_all_filters_str()))
        if not args or len(args) == 0:
            return all_bears
        return cls.available_filters[filter](all_bears, args)
