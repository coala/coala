from coalib.parsing.InvalidFilterException import InvalidFilterException

from coalib.parsing.filters.LanguageFilter import language_filter
from coalib.parsing.filters.CanDetectFilter import can_detect_filter
from coalib.parsing.filters.CanFixFilter import can_fix_filter

available_filters = {'language': language_filter,
                     'can_detect': can_detect_filter,
                     'can_fix': can_fix_filter}


def is_valid_filter(filter):
    return filter in available_filters


def apply_filter(filter_name, filter_args, filter_function, all_bears=None):
    def filter_section_bears(bears, args):
        return {section:
                tuple(bear for bear in bears[section]
                      if filter_function(bear, args))
                for section in bears}

    def filter_wrapper(section_to_bears_dict, args):
        args = {arg.lower() for arg in args}
        local_bears, global_bears = section_to_bears_dict
        local_bears = filter_section_bears(local_bears, args)
        global_bears = filter_section_bears(global_bears, args)
        return local_bears, global_bears

    if all_bears is None:
        from coalib.settings.ConfigurationGathering import (
            get_all_bears)
        all_bears = get_all_bears()
    if not is_valid_filter(filter_name):
        raise InvalidFilterException('{!r} is an invalid filter. '
                                     'Available filters: {}'.format(
                                         filter_name,
                                         ', '.join(sorted(
                                             available_filters))))
    if not filter_args or len(filter_args) == 0:
        return all_bears
    return available_filters[filter_name](all_bears, filter_args),
    filter_wrapper


def apply_filters(filters, bears=None):
    """
    Returns bears after filtering based on ``filters``. It returns
    intersection of bears if more than one element is present in ``filters``
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
        bears = apply_filter(filter_name, filter_args, bears)
    return bears
