from itertools import chain

from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.processes.Processing import execute_section
from coalib.results.HiddenResult import HiddenResult
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.misc.Exceptions import get_exitcode


do_nothing = lambda *args: True


def run_coala(log_printer=None,
              print_results=do_nothing,
              acquire_settings=do_nothing,
              print_section_beginning=do_nothing,
              nothing_done=do_nothing,
              show_bears=do_nothing):
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
    :param nothing_done:            A callback that will be called without
                                    parameters if nothing was done.
    :param show_bears:              A callback that will be called with first
                                    a list of local bears, second a list of
                                    global bears to output them.
    :return:                        A dictionary containing a list of results
                                    for all analyzed sections as key.
    """
    log_printer = log_printer or LogPrinter(ConsolePrinter())

    exitcode = 0
    results = None
    try:
        yielded_results = False
        did_nothing = True
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(acquire_settings, log_printer)

        if bool(sections["default"].get("show_bears", "False")):
            show_bears(local_bears,
                       global_bears)
            did_nothing = False
        else:
            results = {}
            for section_name in sections:
                section = sections[section_name]
                if not section.is_enabled(targets):
                    continue

                print_section_beginning(section)
                section_result = execute_section(
                    section=section,
                    global_bear_list=global_bears[section_name],
                    local_bear_list=local_bears[section_name],
                    print_results=print_results,
                    log_printer=log_printer)
                yielded_results = yielded_results or section_result[0]

                results_for_section = []
                for value in chain(section_result[1].values(),
                                   section_result[2].values()):
                    if value is None:
                        continue

                    for result in value:
                        if not isinstance(result, HiddenResult):
                            results_for_section.append(result)

                results[section_name] = results_for_section
                did_nothing = False

        if did_nothing:
            nothing_done()

        if yielded_results:
            exitcode = 1
    except BaseException as exception:  # pylint: disable=broad-except
        exitcode = exitcode or get_exitcode(exception, log_printer)

    return results, exitcode
