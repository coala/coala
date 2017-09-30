import logging
import os
import platform

from coalib import VERSION
from coalib.misc.Exceptions import get_exitcode
from coalib.output.Interactions import fail_acquire_settings
from coalib.output.Logging import CounterHandler
from coalib.processes.Processing import execute_section, simplify_section_result
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.results.result_actions.DoNothingAction import DoNothingAction
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.IgnoreResultAction import IgnoreResultAction
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.results.result_actions.PrintAspectAction import PrintAspectAction
from coalib.results.result_actions.PrintMoreInfoAction import  \
    PrintMoreInfoAction
from coalib.results.result_actions.PrintDebugMessageAction import \
    PrintDebugMessageAction
from coalib.misc.Caching import FileCache
from coalib.misc.CachingUtilities import (
    settings_changed, update_settings_db, get_settings_hash)


def do_nothing(*args):
    return True


STR_ENTER_NUMBER = 'Enter number (Ctrl-{} to exit): '.format(
    'Z' if platform.system() == 'Windows' else 'D')


def provide_all_actions():
    return [DoNothingAction().get_metadata().desc,
            ShowPatchAction().get_metadata().desc,
            ApplyPatchAction().get_metadata().desc,
            IgnoreResultAction().get_metadata().desc,
            OpenEditorAction().get_metadata().desc,
            PrintAspectAction().get_metadata().desc,
            PrintDebugMessageAction().get_metadata().desc,
            PrintMoreInfoAction().get_metadata().desc]


def format_lines(lines, symbol='', line_nr=''):
    # type: (object, object, object) -> object
    def sym(x): return ']' if x is '[' else x
    return '\n'.join('{}{:>5}{} {}'.format(symbol, sym(symbol), line_nr, line)
                     for line in lines.rstrip('\n').split('\n'))


def run_coala(console_printer=None,
              log_printer=None,
              print_results=do_nothing,
              acquire_settings=fail_acquire_settings,
              print_section_beginning=do_nothing,
              nothing_done=do_nothing,
              autoapply=True,
              force_show_patch=False,
              arg_parser=None,
              arg_list=None,
              args=None,
              debug=False):
    """
    This is a main method that should be usable for almost all purposes and
    reduces executing coala to one function call.

    :param console_printer:         Object to print messages on the console.
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
    :param autoapply:               Set this to false to not autoapply any
                                    actions. If you set this to `False`,
                                    `force_show_patch` will be ignored.
    :param force_show_patch:        If set to True, a patch will be always
                                    shown. (Using ApplyPatchAction.)
    :param arg_parser:              Instance of ArgParser that is used to parse
                                    non-setting arguments.
    :param arg_list:                The CLI argument list.
    :param args:                    Alternative pre-parsed CLI arguments.
    :param debug:                   Run in debug mode, bypassing
                                    multiprocessing, and not catching any
                                    exceptions.
    :return:                        A dictionary containing a list of results
                                    for all analyzed sections as key.
    """
    all_actions_possible = provide_all_actions()
    apply_single = None
    if getattr(args, 'single_action', None) is not None:
        while True:
            for i, action in enumerate(all_actions_possible, 1):
                console_printer.print(format_lines('{}'.format(
                    action), symbol='['))

            line = format_lines(STR_ENTER_NUMBER, symbol='[')

            choice = input(line)

            if choice.isalpha():
                choice = choice.upper()
                choice = '(' + choice + ')'
                if choice == '(N)':
                    apply_single = 'Do (N)othing'
                    break
                for i, action in enumerate(all_actions_possible, 1):
                    if choice in action:
                        apply_single = action
                        break
                if apply_single:
                    break
                console_printer.print(format_lines(
                                    'Please enter a valid letter.',
                                    symbol='['))

        args.apply_patch = False

    exitcode = 0
    sections = {}
    results = {}
    file_dicts = {}
    try:
        yielded_results = yielded_unfixed_results = False
        did_nothing = True
        sections, local_bears, global_bears, targets = gather_configuration(
            acquire_settings,
            arg_parser=arg_parser,
            arg_list=arg_list,
            args=args)

        logging.debug('Platform {} -- Python {}, coalib {}'
                      .format(platform.system(), platform.python_version(),
                              VERSION))

        settings_hash = get_settings_hash(sections, targets)
        flush_cache = bool(sections['cli'].get('flush_cache', False) or
                           settings_changed(None, settings_hash))

        cache = None
        if not sections['cli'].get('disable_caching', False):
            cache = FileCache(None, os.getcwd(), flush_cache)

        for section_name, section in sections.items():
            if not section.is_enabled(targets):
                continue

            if not autoapply:
                section['default_actions'] = ''
            elif force_show_patch:
                section['default_actions'] = '*: ShowPatchAction'
                section['show_result_on_top'] = 'yeah'

            print_section_beginning(section)
            section_result = execute_section(
                section=section,
                global_bear_list=global_bears[section_name],
                local_bear_list=local_bears[section_name],
                print_results=print_results,
                cache=cache,
                log_printer=None,
                console_printer=console_printer,
                debug=debug or args and args.debug,
                apply_single=(apply_single
                              if apply_single is not None else
                              False))
            yielded, yielded_unfixed, results[section_name] = (
                simplify_section_result(section_result))

            yielded_results = yielded_results or yielded
            yielded_unfixed_results = (
                yielded_unfixed_results or yielded_unfixed)
            did_nothing = False

            file_dicts[section_name] = section_result[3]

        update_settings_db(None, settings_hash)
        if cache:
            cache.write()

        if CounterHandler.get_num_calls_for_level('ERROR') > 0:
            exitcode = 1
        elif did_nothing:
            nothing_done(None)
            exitcode = 2
        elif yielded_unfixed_results:
            exitcode = 1
        elif yielded_results:
            exitcode = 5
    except BaseException as exception:  # pylint: disable=broad-except
        if not isinstance(exception, SystemExit):
            if args and args.debug or (
                    sections and sections.get('cli', {}).get('debug', False)
            ):
                import ipdb
                with ipdb.launch_ipdb_on_exception():
                    raise

            if debug:
                raise

        exitcode = exitcode or get_exitcode(exception)

    return results, exitcode, file_dicts
