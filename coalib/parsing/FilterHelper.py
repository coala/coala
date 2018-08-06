from coalib.parsing.InvalidFilterException import InvalidFilterException
from coalib.parsing.filters import available_filters
from coalib.parsing.DefaultArgParser import default_arg_parser


def is_valid_filter(filter):
    return filter in available_filters


def _filter_section_bears(bears, args, filter_name):
    filter_function = available_filters[filter_name]
    return {section:
            tuple(bear for bear in bears[section]
                  if filter_function(bear, args))
            for section in bears}


def apply_filter(filter_name, filter_args, all_bears=None):
    """
    Returns bears after filtering based on ``filter_args``. It returns
    all bears if nothing is present in ``filter_args``.

    :param filter_name:
        Name of the filter.
    :param filter_args:
        Arguments of the filter to be passed in.
        For example:
        ``['c', 'java']``
    :param all_bears:
        List of bears on which filter is to be applied.
        All the bears are loaded automatically by default.
    :return:
        Filtered bears based on a single filter.
    """
    if all_bears is None:
        from coalib.settings.ConfigurationGathering import (
            get_all_bears)
        all_bears = get_all_bears()
    if not is_valid_filter(filter_name):
        raise InvalidFilterException(filter_name)
    if not filter_args or len(filter_args) == 0:
        return all_bears

    filter_args = {arg.lower() for arg in filter_args}
    local_bears, global_bears = all_bears
    local_bears = _filter_section_bears(
        local_bears, filter_args, filter_name)
    global_bears = _filter_section_bears(
        global_bears, filter_args, filter_name)
    return local_bears, global_bears


def apply_filters(filters, bears=None, sections=None):
    """
    Returns bears or sections after filtering based on ``filters``.
    It returns intersection if more than one element is present in
    ``filters`` list. Either bears or sections need to be passed,
    if both or none are passed it defaults to use bears gathering
    and runs filter in bear filtering mode.

    :param filters:
        List of args based on ``bears`` has to be filtered. For example:
        ``[['language', 'c', 'java'], ['can_fix', 'syntax'],
        ['section_tags', 'save']]``
    :param bears:
        The bears to filter.
    :param sections:
        The sections to filter.
    :return:
        Filtered bears or sections.
    """
    items = bears
    applier = apply_filter
    if sections is not None:
        items = sections
        applier = _apply_section_filter

    for filter in filters:
        filter_name, *filter_args = filter
        items = applier(filter_name, filter_args, items)
    return items


def _apply_section_filter(filter_name, filter_args, all_sections):
    """
    Returns sections after filtering based on ``filter_args``. It
    returns all sections if nothing is present in ``filter_args``.

    :param filter_name:
        Name of the section filter.
    :param filter_args:
        Arguments to be passed to the filter. For example:
        ``['section_tags', ('save', 'change')]``
    :param all_sections:
        List of all sections on which filter is to be applied.
    :return:
        Filtered sections based on a single section filter.
    """
    if not is_valid_filter(filter_name):
        raise InvalidFilterException(filter_name)
    if not filter_args or len(filter_args) == 0:
        return all_sections

    filter_function = available_filters[filter_name]
    filtered_sections = []

    for section in all_sections:
        if filter_function(section, filter_args):
            filtered_sections += [section]

    return filtered_sections


def collect_filters(args, arg_list=None, arg_parser=None):
    """
    Collects all filters from based on cli arguments.

    :param args:
        Parsed CLI args using which the filters are to be collected.
    :param arg_list:
        The CLI argument list.
    :param arg_parser:
        Instance of ArgParser that is used to parse arg list.
    :return:
        List of filters in standard filter format, i.e
        ``[['filter_name', 'arg1', 'arg2']]``.
    """
    if args is None:
        arg_parser = default_arg_parser() if arg_parser is None else arg_parser
        args = arg_parser.parse_args(arg_list)

    return getattr(args, 'filter_by', None) or []
