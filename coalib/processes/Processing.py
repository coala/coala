from itertools import chain
import os
import platform
import queue
import subprocess

from coala_utils.string_processing.StringConverter import StringConverter
from coala_utils.FileUtils import detect_encoding

from coalib.collecting.Collectors import collect_files
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.processes.BearRunning import run
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.processes.LogPrinterThread import LogPrinterThread
from coalib.results.Result import Result
from coalib.results.result_actions.DoNothingAction import DoNothingAction
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.IgnoreResultAction import IgnoreResultAction
from coalib.results.result_actions.ShowAppliedPatchesAction \
    import ShowAppliedPatchesAction
from coalib.results.result_actions.PrintDebugMessageAction import (
    PrintDebugMessageAction)
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import glob_list
from coalib.parsing.Globbing import fnmatch


ACTIONS = [DoNothingAction,
           ApplyPatchAction,
           PrintDebugMessageAction,
           ShowPatchAction,
           IgnoreResultAction,
           ShowAppliedPatchesAction]


def get_cpu_count():
    # cpu_count is not implemented for some CPU architectures/OSes
    return os.cpu_count() or 2


def fill_queue(queue_fill, any_list):
    """
    Takes element from a list and populates a queue with those elements.

    :param queue_fill: The queue to be filled.
    :param any_list:   List containing the elements.
    """
    for elem in any_list:
        queue_fill.put(elem)


def get_running_processes(processes):
    return sum((1 if process.is_alive() else 0) for process in processes)


def create_process_group(command_array, **kwargs):
    if platform.system() == 'Windows':  # pragma posix: no cover
        proc = subprocess.Popen(
            command_array,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            **kwargs)
    else:  # pragma nt: no cover
        proc = subprocess.Popen(command_array,
                                preexec_fn=os.setsid,
                                **kwargs)
    return proc


def get_default_actions(section):
    """
    Parses the key ``default_actions`` in the given section.

    :param section:    The section where to parse from.
    :return:           A dict with the bearname as keys and their default
                       actions as values and another dict that contains bears
                       and invalid action names.
    """
    try:
        default_actions = dict(section['default_actions'])
    except IndexError:
        return {}, {}

    action_dict = {action.get_metadata().name: action for action in ACTIONS}
    invalid_action_set = default_actions.values() - action_dict.keys()
    invalid_actions = {}
    if len(invalid_action_set) != 0:
        invalid_actions = {
            bear: action
            for bear, action in default_actions.items()
            if action in invalid_action_set}
        for invalid in invalid_actions.keys():
            del default_actions[invalid]

    actions = {bearname: action_dict[action_name]
               for bearname, action_name in default_actions.items()}
    return actions, invalid_actions


def autoapply_actions(results,
                      file_dict,
                      file_diff_dict,
                      section,
                      log_printer):
    """
    Auto-applies actions like defined in the given section.

    :param results:        A list of results.
    :param file_dict:      A dictionary containing the name of files and its
                           contents.
    :param file_diff_dict: A dictionary that contains filenames as keys and
                           diff objects as values.
    :param section:        The section.
    :param log_printer:    A log printer instance to log messages on.
    :return:               A list of unprocessed results.
    """

    default_actions, invalid_actions = get_default_actions(section)
    no_autoapply_warn = bool(section.get('no_autoapply_warn', False))
    for bearname, actionname in invalid_actions.items():
        log_printer.warn('Selected default action {!r} for bear {!r} does '
                         'not exist. Ignoring action.'.format(actionname,
                                                              bearname))

    if len(default_actions) == 0:
        # There's nothing to auto-apply.
        return results

    not_processed_results = []
    for result in results:
        try:
            # Match full bear names deterministically, prioritized!
            action = default_actions[result.origin]
        except KeyError:
            for bear_glob in default_actions:
                if fnmatch(result.origin, bear_glob):
                    action = default_actions[bear_glob]
                    break
            else:
                not_processed_results.append(result)
                continue

        applicable = action.is_applicable(result, file_dict, file_diff_dict)
        if applicable is not True:
            if not no_autoapply_warn:
                log_printer.warn('{}: {}'.format(result.origin, applicable))
            not_processed_results.append(result)
            continue

        try:
            action().apply_from_section(result,
                                        file_dict,
                                        file_diff_dict,
                                        section)
            log_printer.info('Applied {!r} on {} from {!r}.'.format(
                action.get_metadata().name,
                result.location_repr(),
                result.origin))
        except Exception as ex:
            not_processed_results.append(result)
            log_printer.log_exception(
                'Failed to execute action {!r} with error: {}.'.format(
                    action.get_metadata().name, ex),
                ex)
            log_printer.debug('-> for result ' + repr(result) + '.')

    return not_processed_results


def check_result_ignore(result, ignore_ranges):
    """
    Determines if the result has to be ignored.

    Any result will be ignored if its origin matches any bear names and its
    SourceRange overlaps with the ignore range.

    Note that everything after a space in the origin will be cut away, so the
    user can ignore results with an origin like `CSecurityBear (buffer)` with
    just `# Ignore CSecurityBear`.

    :param result:        The result that needs to be checked.
    :param ignore_ranges: A list of tuples, each containing a list of lower
                          cased affected bearnames and a SourceRange to
                          ignore. If any of the bearname lists is empty, it
                          is considered an ignore range for all bears.
                          This may be a list of globbed bear wildcards.
    :return:              True if the result has to be ignored.
    """
    for bears, range in ignore_ranges:
        orig = result.origin.lower().split(' ')[0]
        if (result.overlaps(range) and
                (len(bears) == 0 or orig in bears or fnmatch(orig, bears))):
            return True

    return False


def print_result(results,
                 file_dict,
                 retval,
                 print_results,
                 section,
                 log_printer,
                 file_diff_dict,
                 ignore_ranges,
                 console_printer,
                 apply_single=False):
    """
    Takes the results produced by each bear and gives them to the print_results
    method to present to the user.

    :param results:        A list of results.
    :param file_dict:      A dictionary containing the name of files and its
                           contents.
    :param retval:         It is True if no results were yielded ever before.
                           If it is False this function will return False no
                           matter what happens. Else it depends on if this
                           invocation yields results.
    :param print_results:  A function that prints all given results appropriate
                           to the output medium.
    :param file_diff_dict: A dictionary that contains filenames as keys and
                           diff objects as values.
    :param ignore_ranges:  A list of SourceRanges. Results that affect code in
                           any of those ranges will be ignored.
    :param apply_single:   The action that should be applied for all results,
                           If it's not selected, has a value of False.
    :param console_printer: Object to print messages on the console.
    :return:               Returns False if any results were yielded. Else
                           True.
    """
    min_severity_str = str(section.get('min_severity', 'INFO')).upper()
    min_severity = RESULT_SEVERITY.str_dict.get(min_severity_str, 'INFO')
    results = list(filter(lambda result:
                          type(result) is Result and
                          result.severity >= min_severity and
                          not check_result_ignore(result, ignore_ranges),
                          results))

    patched_results = autoapply_actions(results,
                                        file_dict,
                                        file_diff_dict,
                                        section,
                                        log_printer)

    print_results(log_printer,
                  section,
                  patched_results,
                  file_dict,
                  file_diff_dict,
                  console_printer,
                  apply_single)
    return retval or len(results) > 0, patched_results


def get_file_dict(filename_list, log_printer, allow_raw_files=False):
    """
    Reads all files into a dictionary.

    :param filename_list:   List of names of paths to files to get contents of.
    :param log_printer:     The logger which logs errors.
    :param allow_raw_files: Allow the usage of raw files (non text files),
                            disabled by default
    :return:                Reads the content of each file into a dictionary
                            with filenames as keys.
    """
    file_dict = {}
    for filename in filename_list:
        try:
            with open(filename, 'r',
                      encoding=detect_encoding(filename)) as _file:
                file_dict[filename] = tuple(_file.readlines())
        except UnicodeDecodeError:
            if allow_raw_files:
                file_dict[filename] = None
                continue
            log_printer.warn("Failed to read file '{}'. It seems to contain "
                             'non-unicode characters. Leaving it '
                             'out.'.format(filename))
        except OSError as exception:
            log_printer.log_exception("Failed to read file '{}' because of "
                                      'an unknown error. Leaving it '
                                      'out.'.format(filename),
                                      exception,
                                      log_level=LOG_LEVEL.WARNING)

    log_printer.debug('Files that will be checked:\n' +
                      '\n'.join(file_dict.keys()))
    return file_dict


def filter_raising_callables(it, exception, *args, debug=False, **kwargs):
    """
    Filters all callable items inside the given iterator that raise the
    given exceptions.

    :param it:        The iterator to filter.
    :param exception: The (tuple of) exception(s) to filter for.
    :param args:      Positional arguments to pass to the callable.
    :param kwargs:    Keyword arguments to pass to the callable.
    """
    for elem in it:
        try:
            yield elem(*args, **kwargs)
        except exception:
            if debug:
                raise


def instantiate_bears(section,
                      local_bear_list,
                      global_bear_list,
                      file_dict,
                      message_queue,
                      console_printer,
                      debug=False):
    """
    Instantiates each bear with the arguments it needs.

    :param section:          The section the bears belong to.
    :param local_bear_list:  List of local bear classes to instantiate.
    :param global_bear_list: List of global bear classes to instantiate.
    :param file_dict:        Dictionary containing filenames and their
                             contents.
    :param message_queue:    Queue responsible to maintain the messages
                             delivered by the bears.
    :param console_printer:  Object to print messages on the console.
    :return:                 The local and global bear instance lists.
    """
    local_bear_list = [bear
                       for bear in filter_raising_callables(
                           local_bear_list,
                           RuntimeError,
                           section,
                           message_queue,
                           timeout=0.1,
                           debug=debug)]

    global_bear_list = [bear
                        for bear in filter_raising_callables(
                            global_bear_list,
                            RuntimeError,
                            file_dict,
                            section,
                            message_queue,
                            timeout=0.1,
                            debug=debug)]

    return local_bear_list, global_bear_list


def instantiate_processes(section,
                          local_bear_list,
                          global_bear_list,
                          job_count,
                          cache,
                          log_printer,
                          console_printer,
                          debug=False,
                          use_raw_files=False):
    """
    Instantiate the number of processes that will run bears which will be
    responsible for running bears in a multiprocessing environment.

    :param section:          The section the bears belong to.
    :param local_bear_list:  List of local bears belonging to the section.
    :param global_bear_list: List of global bears belonging to the section.
    :param job_count:        Max number of processes to create.
    :param cache:            An instance of ``misc.Caching.FileCache`` to use as
                             a file cache buffer.
    :param log_printer:      The log printer to warn to.
    :param console_printer:  Object to print messages on the console.
    :param debug:            Bypass multiprocessing and activate debug mode
                             for bears, not catching any exceptions on running
                             them.
    :param use_raw_files:    Allow the usage of raw files (non text files)
    :return:                 A tuple containing a list of processes,
                             and the arguments passed to each process which are
                             the same for each object.
    """
    filename_list = collect_files(
        glob_list(section.get('files', '')),
        log_printer,
        ignored_file_paths=glob_list(section.get('ignore', '')),
        limit_file_paths=glob_list(section.get('limit_files', '')),
        section_name=section.name)

    # This stores all matched files irrespective of whether coala is run
    # only on changed files or not. Global bears require all the files
    complete_filename_list = filename_list
    complete_file_dict = get_file_dict(complete_filename_list, log_printer,
                                       use_raw_files)

    if debug:
        from . import DebugProcessing as processing
    else:
        import multiprocessing as processing
    manager = processing.Manager()
    global_bear_queue = processing.Queue()
    filename_queue = processing.Queue()
    local_result_dict = manager.dict()
    global_result_dict = manager.dict()
    message_queue = processing.Queue()
    control_queue = processing.Queue()

    loaded_local_bears_count = len(local_bear_list)
    local_bear_list[:], global_bear_list[:] = instantiate_bears(
        section,
        local_bear_list,
        global_bear_list,
        complete_file_dict,
        message_queue,
        console_printer=console_printer,
        debug=debug)
    loaded_valid_local_bears_count = len(local_bear_list)
    # Note: the complete file dict is given as the file dict to bears and
    # the whole project is accessible to every bear. However, local bears are
    # run only for the changed files if caching is enabled.

    # Start tracking all the files
    if cache and (loaded_valid_local_bears_count == loaded_local_bears_count
                  and not use_raw_files):
        cache.track_files(set(complete_filename_list))
        changed_files = cache.get_uncached_files(
            set(filename_list)) if cache else filename_list

        # If caching is enabled then the local bears should process only the
        # changed files.
        log_printer.debug("coala is run only on changed files, bears' log "
                          'messages from previous runs may not appear. You may '
                          'use the `--flush-cache` flag to see them.')
        filename_list = changed_files

    # Note: the complete file dict is given as the file dict to bears and
    # the whole project is accessible to every bear. However, local bears are
    # run only for the changed files if caching is enabled.
    file_dict = {filename: complete_file_dict[filename]
                 for filename in filename_list
                 if filename in complete_file_dict}

    bear_runner_args = {'file_name_queue': filename_queue,
                        'local_bear_list': local_bear_list,
                        'global_bear_list': global_bear_list,
                        'global_bear_queue': global_bear_queue,
                        'file_dict': file_dict,
                        'local_result_dict': local_result_dict,
                        'global_result_dict': global_result_dict,
                        'message_queue': message_queue,
                        'control_queue': control_queue,
                        'timeout': 0.1,
                        'debug': debug}

    fill_queue(filename_queue, file_dict.keys())
    fill_queue(global_bear_queue, range(len(global_bear_list)))

    return ([processing.Process(target=run, kwargs=bear_runner_args)
             for i in range(job_count)],
            bear_runner_args)


def get_ignore_scope(line, keyword):
    """
    Retrieves the bears that are to be ignored defined in the given line.

    :param line:    The line containing the ignore declaration.
    :param keyword: The keyword that was found. Everything after the rightmost
                    occurrence of it will be considered for the scope.
    :return:        A list of lower cased bearnames or an empty list (-> "all")
    """
    toignore = line[line.rfind(keyword) + len(keyword):]
    if toignore.startswith('all'):
        return []
    else:
        return list(StringConverter(toignore, list_delimiters=', '))


def yield_ignore_ranges(file_dict):
    """
    Yields tuples of affected bears and a SourceRange that shall be ignored for
    those.

    :param file_dict: The file dictionary.
    """
    for filename, file in file_dict.items():
        start = None
        bears = []
        stop_ignoring = False

        # Do not process raw files
        if file is None:
            continue

        for line_number, line in enumerate(file, start=1):
            # Before lowering all lines ever read, first look for the biggest
            # common substring, case sensitive: I*gnor*e, start i*gnor*ing,
            # N*oqa*.
            if 'gnor' in line or 'oqa' in line:
                line = line.lower()
                if 'start ignoring ' in line:
                    start = line_number
                    bears = get_ignore_scope(line, 'start ignoring ')
                elif 'stop ignoring' in line:
                    stop_ignoring = True
                    if start:
                        yield (bears,
                               SourceRange.from_values(
                                   filename,
                                   start,
                                   1,
                                   line_number,
                                   len(file[line_number-1])))

                else:
                    for ignore_stmt in ['ignore ', 'noqa ', 'noqa']:
                        if ignore_stmt in line:
                            end_line = min(line_number + 1, len(file))
                            yield (get_ignore_scope(line, ignore_stmt),
                                   SourceRange.from_values(
                                       filename,
                                       line_number, 1,
                                       end_line, len(file[end_line-1])))
                            break

        if stop_ignoring is False and start is not None:
            yield (bears,
                   SourceRange.from_values(filename,
                                           start,
                                           1,
                                           len(file),
                                           len(file[-1])))


def get_file_list(results):
    """
    Get the set of files that are affected in the given results.

    :param results: A list of results from which the list of files is to be
                    extracted.
    :return:        A set of file paths containing the mentioned list of
                    files.
    """
    return {code.file for result in results for code in result.affected_code}


def process_queues(processes,
                   control_queue,
                   local_result_dict,
                   global_result_dict,
                   file_dict,
                   print_results,
                   section,
                   cache,
                   log_printer,
                   console_printer,
                   debug=False,
                   apply_single=False):
    """
    Iterate the control queue and send the results received to the print_result
    method so that they can be presented to the user.

    :param processes:          List of processes which can be used to run
                               Bears.
    :param control_queue:      Containing control elements that indicate
                               whether there is a result available and which
                               bear it belongs to.
    :param local_result_dict:  Dictionary containing results respective to
                               local bears. It is modified by the processes
                               i.e. results are added to it by multiple
                               processes.
    :param global_result_dict: Dictionary containing results respective to
                               global bears. It is modified by the processes
                               i.e. results are added to it by multiple
                               processes.
    :param file_dict:          Dictionary containing file contents with
                               filename as keys.
    :param print_results:      Prints all given results appropriate to the
                               output medium.
    :param cache:              An instance of ``misc.Caching.FileCache`` to use
                               as a file cache buffer.
    :param debug:              Run in debug mode, expecting that no logger
                               thread is running.
    :param apply_single:       The action that should be applied for all
                               results. If it's not selected, has a value of
                               False.
    :return:                   Return True if all bears execute successfully and
                               Results were delivered to the user. Else False.
    """
    file_diff_dict = {}
    retval = False
    # Number of processes working on local/global bears. They are count down
    # when the last queue element of that process is processed which may be
    # *after* the process has ended!
    local_processes = len(processes)
    global_processes = len(processes)
    global_result_buffer = []
    result_files = set()
    ignore_ranges = list(yield_ignore_ranges(file_dict))

    # One process is the logger thread (if not in debug mode)
    while local_processes > (1 if not debug else 0):
        try:
            control_elem, index = control_queue.get(timeout=0.1)

            if control_elem == CONTROL_ELEMENT.LOCAL_FINISHED:
                local_processes -= 1
            elif control_elem == CONTROL_ELEMENT.GLOBAL_FINISHED:
                global_processes -= 1
            elif control_elem == CONTROL_ELEMENT.LOCAL:
                assert local_processes != 0
                result_files.update(get_file_list(local_result_dict[index]))
                retval, res = print_result(local_result_dict[index],
                                           file_dict,
                                           retval,
                                           print_results,
                                           section,
                                           log_printer,
                                           file_diff_dict,
                                           ignore_ranges,
                                           console_printer=console_printer,
                                           apply_single=apply_single
                                           )
                local_result_dict[index] = res
            else:
                assert control_elem == CONTROL_ELEMENT.GLOBAL
                global_result_buffer.append(index)
        except queue.Empty:
            if get_running_processes(processes) < 2:  # pragma: no cover
                # Recover silently, those branches are only
                # nondeterministically covered.
                break

    # Flush global result buffer
    for elem in global_result_buffer:
        result_files.update(get_file_list(global_result_dict[elem]))
        retval, res = print_result(global_result_dict[elem],
                                   file_dict,
                                   retval,
                                   print_results,
                                   section,
                                   log_printer,
                                   file_diff_dict,
                                   ignore_ranges,
                                   console_printer=console_printer,
                                   apply_single=apply_single)
        global_result_dict[elem] = res

    # One process is the logger thread
    while global_processes > 1:
        try:
            control_elem, index = control_queue.get(timeout=0.1)

            if control_elem == CONTROL_ELEMENT.GLOBAL:
                result_files.update(get_file_list(global_result_dict[index]))
                retval, res = print_result(global_result_dict[index],
                                           file_dict,
                                           retval,
                                           print_results,
                                           section,
                                           log_printer,
                                           file_diff_dict,
                                           ignore_ranges,
                                           console_printer,
                                           apply_single)
                global_result_dict[index] = res
            else:
                assert control_elem == CONTROL_ELEMENT.GLOBAL_FINISHED
                global_processes -= 1
        except queue.Empty:
            if get_running_processes(processes) < 2:  # pragma: no cover
                # Recover silently, those branches are only
                # nondeterministically covered.
                break

    if cache:
        cache.untrack_files(result_files)
    return retval


def simplify_section_result(section_result):
    """
    Takes in a section's result from ``execute_section`` and simplifies it
    for easy usage in other functions.

    :param section_result: The result of a section which was executed.
    :return:               Tuple containing:
                            - bool - True if results were yielded
                            - bool - True if unfixed results were yielded
                            - list - Results from all bears (local and global)
    """
    section_yielded_result = section_result[0]
    results_for_section = []

    for value in chain(section_result[1].values(),
                       section_result[2].values()):
        if value is None:
            continue

        for result in value:
            results_for_section.append(result)
    section_yielded_unfixed_results = len(results_for_section) > 0

    return (section_yielded_result,
            section_yielded_unfixed_results,
            results_for_section)


def execute_section(section,
                    global_bear_list,
                    local_bear_list,
                    print_results,
                    cache,
                    log_printer,
                    console_printer,
                    debug=False,
                    apply_single=False):
    # type: (object, object, object, object, object, object, object, object,
    # object) -> object
    """
    Executes the section with the given bears.

    The execute_section method does the following things:

    1. Prepare a Process
       -  Load files
       -  Create queues
    2. Spawn up one or more Processes
    3. Output results from the Processes
    4. Join all processes

    :param section:          The section to execute.
    :param global_bear_list: List of global bears belonging to the section.
                             Dependencies are already resolved.
    :param local_bear_list:  List of local bears belonging to the section.
                             Dependencies are already resolved.
    :param print_results:    Prints all given results appropriate to the
                             output medium.
    :param cache:            An instance of ``misc.Caching.FileCache`` to use as
                             a file cache buffer.
    :param log_printer:      The log_printer to warn to.
    :param console_printer:  Object to print messages on the console.
    :param debug:            Bypass multiprocessing and run bears in debug mode,
                             not catching any exceptions.
    :param apply_single:     The action that should be applied for all results.
                             If it's not selected, has a value of False.
    :return:                 Tuple containing a bool (True if results were
                             yielded, False otherwise), a Manager.dict
                             containing all local results(filenames are key)
                             and a Manager.dict containing all global bear
                             results (bear names are key) as well as the
                             file dictionary.
    """
    if debug:
        running_processes = 1
    else:
        try:
            running_processes = int(section['jobs'])
        except ValueError:
            log_printer.warn("Unable to convert setting 'jobs' into a number. "
                             'Falling back to CPU count.')
            running_processes = get_cpu_count()
        except IndexError:
            running_processes = get_cpu_count()

    bears = global_bear_list + local_bear_list
    use_raw_files = set(bear.USE_RAW_FILES for bear in bears)

    if len(use_raw_files) > 1:
        log_printer.err("Bears that uses raw files can't be mixed with "
                        'Bears that uses text files. Please move the following '
                        'bears to their own section: ' +
                        ', '.join(bear.name for bear in bears
                                  if not bear.USE_RAW_FILES))
        return ((), {}, {}, {})

    # use_raw_files is expected to be only one object.
    # The if statement is to ensure this doesn't fail when
    # it's running on an empty run
    use_raw_files = use_raw_files.pop() if len(use_raw_files) > 0 else False

    processes, arg_dict = instantiate_processes(section,
                                                local_bear_list,
                                                global_bear_list,
                                                running_processes,
                                                cache,
                                                log_printer,
                                                console_printer=console_printer,
                                                debug=debug,
                                                use_raw_files=use_raw_files)

    logger_thread = LogPrinterThread(arg_dict['message_queue'],
                                     log_printer)
    # Start and join the logger thread along with the processes to run bears
    if not debug:
        # in debug mode the logging messages are directly processed by the
        # message_queue
        processes.append(logger_thread)

    for runner in processes:
        runner.start()

    try:
        return (process_queues(processes,
                               arg_dict['control_queue'],
                               arg_dict['local_result_dict'],
                               arg_dict['global_result_dict'],
                               arg_dict['file_dict'],
                               print_results,
                               section,
                               cache,
                               log_printer,
                               console_printer=console_printer,
                               debug=debug,
                               apply_single=apply_single),
                arg_dict['local_result_dict'],
                arg_dict['global_result_dict'],
                arg_dict['file_dict'])
    finally:
        if not debug:
            # in debug mode multiprocessing and logger_thread are disabled
            # ==> no need for following actions
            logger_thread.running = False

            for runner in processes:
                runner.join()
