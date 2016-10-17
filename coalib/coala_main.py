import os
import platform

import pip
from pyprint.ConsolePrinter import ConsolePrinter

from coalib import VERSION
from coalib.misc.Exceptions import get_exitcode
from coalib.output.Interactions import fail_acquire_settings
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.processes.Processing import execute_section, simplify_section_result
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.misc.Caching import FileCache
from coalib.misc.CachingUtilities import (
    settings_changed, update_settings_db, get_settings_hash)
from coalib.misc.Constants import configure_logging

do_nothing = lambda *args: True


def run_coala(log_printer=None,
              print_results=do_nothing,
              acquire_settings=fail_acquire_settings,
              print_section_beginning=do_nothing,
              nothing_done=do_nothing,
              autoapply=True,
              arg_parser=None,
              arg_list=None):
    """
    This is a main method that should be usable for almost all purposes and
    reduces executing coala to one function call.

    :param log_printer:             A LogPrinter object to use for logging.
    :param print_results:           A callback that takes a LogPrinter, a
                                    section, a list of results to be printed,
                                    the file dict and the mutable file diff
                                    dict.
    :param acquire_settings:        The method to use for requesting settings.
                                    It will get a parameter which is a
                                    dictionary with the settings name as key
                                    and a list containing a description in [0]
                                    and the names of the bears who need this
                                    setting in all following indexes.
    :param print_section_beginning: A callback that will be called with a
                                    section name string whenever analysis of a
                                    new section is started.
    :param nothing_done:            A callback that will be called with only a
                                    log printer that shall indicate that
                                    nothing was done.
    :param autoapply:               Set to False to autoapply nothing by
                                    default; this is overridable via any
                                    configuration file/CLI.
    :param arg_list:                The CLI argument list.
    :return:                        A dictionary containing a list of results
                                    for all analyzed sections as key.
    """
    configure_logging()

    log_printer = (
        LogPrinter(ConsolePrinter(), LOG_LEVEL.DEBUG) if log_printer is None
        else log_printer)

    exitcode = 0
    results = {}
    file_dicts = {}
    try:
        yielded_results = yielded_unfixed_results = False
        did_nothing = True
        sections, local_bears, global_bears, targets = gather_configuration(
            acquire_settings,
            log_printer,
            autoapply=autoapply,
            arg_parser=arg_parser,
            arg_list=arg_list)

        log_printer.debug("Platform {} -- Python {}, pip {}, coalib {}"
                          .format(platform.system(), platform.python_version(),
                                  pip.__version__, VERSION))

        config_file = os.path.abspath(str(sections["default"].get("config")))

        settings_hash = get_settings_hash(sections, targets)
        flush_cache = bool(sections["default"].get("flush_cache", False) or
                           settings_changed(log_printer, settings_hash))

        disable_caching = bool(sections["default"].get(
            "disable_caching", False))
        cache = None
        if not sections["default"].get("disable_caching", False):
            cache = FileCache(log_printer, os.getcwd(), flush_cache)

        for section_name, section in sections.items():
            if not section.is_enabled(targets):
                continue

            print_section_beginning(section)
            section_result = execute_section(
                section=section,
                global_bear_list=global_bears[section_name],
                local_bear_list=local_bears[section_name],
                print_results=print_results,
                cache=cache,
                log_printer=log_printer)
            yielded, yielded_unfixed, results[section_name] = (
                simplify_section_result(section_result))

            yielded_results = yielded_results or yielded
            yielded_unfixed_results = (
                yielded_unfixed_results or yielded_unfixed)
            did_nothing = False

            file_dicts[section_name] = section_result[3]

        update_settings_db(log_printer, settings_hash)
        if cache:
            cache.write()

        if did_nothing:
            nothing_done(log_printer)
        elif yielded_unfixed_results:
            exitcode = 1
        elif yielded_results:
            exitcode = 5
    except BaseException as exception:  # pylint: disable=broad-except
        exitcode = exitcode or get_exitcode(exception, log_printer)

    return results, exitcode, file_dicts
