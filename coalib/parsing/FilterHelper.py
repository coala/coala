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
    def apply_filter(cls, filter_name, filter_args, all_bears=None):
        if all_bears is None:
            from coalib.settings.ConfigurationGathering import (
                get_all_bears)
            all_bears = get_all_bears(LogPrinter())
        if not cls.is_valid_filter(filter_name):
            raise InvalidFilterException('{!r} is an invalid filter. '
                                         'Available filters: {}'.format(
                                             filter_name,
                                             cls.get_all_filters_str()))
        if not filter_args or len(filter_args) == 0:
            return all_bears
        return cls.available_filters[filter_name](all_bears, filter_args)

    @classmethod
    def apply_filters(cls, filters, bears=None):
        """
        Returns bears after filtering based on ``args``. It returns
        intersection of bears if more than one element is present in ``args``
        list.

        :param filters:
            List of args based on ``bears`` has to be filtered.
            For example:
            ``[['language', 'c', 'java'], ['can_fix', 'syntax']]``
        :param bears:
            The bears to filter.
        :return:
            Filtered bears.
        """
        for filter in filters:
            filter_name, *filter_args = filter
            bears = cls.apply_filter(
                filter_name, filter_args, bears)
        return bears
