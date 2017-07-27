from coalib.output.printers.LogPrinter import LogPrinter
from coalib.parsing.InvalidFilterException import InvalidFilterException


def get_all_filters_str(arg, sep=', '):
    return sep.join(sorted(arg.available_filters))


def is_valid_filter(arg, filter):
    return filter in arg.available_filters


def get_filtered_bears(arg, filter, args, all_bears=None):
    if all_bears is None:
        from coalib.settings.ConfigurationGathering import (
            get_all_bears)
        all_bears = get_all_bears(LogPrinter())
    if not arg.is_valid_filter(filter):
        raise InvalidFilterException('{!r} is an invalid filter. '
                                           'Available filters: {}'.format(
                                             filter, arg.get_all_filters_str()))
    if not args or len(args) == 0:
        return all_bears
    return cls.available_filters[filter](all_bears, args)
