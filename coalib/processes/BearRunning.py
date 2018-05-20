import queue
import traceback

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear
from coalib.misc import Constants
from coalib.processes.communication.LogMessage import LOG_LEVEL, LogMessage
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.results.Result import Result


def send_msg(message_queue, timeout, log_level, *args, delimiter=' ', end=''):
    """
    Puts message into message queue for a LogPrinter to present to the user.

    :param message_queue: The queue to put the message into and which the
                          LogPrinter reads.
    :param timeout:       The queue blocks at most timeout seconds for a free
                          slot to execute the put operation on. After the
                          timeout it returns queue Full exception.
    :param log_level:     The log_level i.e Error,Debug or Warning.It is sent
                          to the LogPrinter depending on the message.
    :param args:          This includes the elements of the message.
    :param delimiter:     It is the value placed between each arg. By default
                          it is a ' '.
    :param end:           It is the value placed at the end of the message.
    """
    output = str(delimiter).join(str(arg) for arg in args) + str(end)
    message_queue.put(LogMessage(log_level, output),
                      timeout=timeout)


def validate_results(message_queue, timeout, result_list, name, args, kwargs):
    """
    Validates if the result_list passed to it contains valid set of results.
    That is the result_list must itself be a list and contain objects of the
    instance of Result object. If any irregularity is found a message is put in
    the message_queue to present the irregularity to the user. Each result_list
    belongs to an execution of a bear.

    :param message_queue: A queue that contains messages of type
                          errors/warnings/debug statements to be printed in the
                          Log.
    :param timeout:       The queue blocks at most timeout seconds for a free
                          slot to execute the put operation on. After the
                          timeout it returns queue Full exception.
    :param result_list:   The list of results to validate.
    :param name:          The name of the bear executed.
    :param args:          The args with which the bear was executed.
    :param kwargs:        The kwargs with which the bear was executed.
    :return:              Returns None if the result_list is invalid. Else it
                          returns the result_list itself.
    """
    if result_list is None:
        return None

    for result in result_list:
        if not isinstance(result, Result):
            send_msg(message_queue,
                     timeout,
                     LOG_LEVEL.ERROR,
                     'The results from the bear {bear} could only be '
                     'partially processed with arguments {arglist}, '
                     '{kwarglist}'
                     .format(bear=name, arglist=args, kwarglist=kwargs))
            send_msg(message_queue,
                     timeout,
                     LOG_LEVEL.DEBUG,
                     'One of the results in the list for the bear {bear} is '
                     'an instance of {ret} but it should be an instance of '
                     'Result'
                     .format(bear=name, ret=result.__class__))
            result_list.remove(result)

    return result_list


def run_bear(message_queue, timeout, bear_instance, *args, debug=False,
             **kwargs):
    """
    This method is responsible for executing the instance of a bear. It also
    reports or logs errors if any occur during the execution of that bear
    instance.

    :param message_queue: A queue that contains messages of type
                          errors/warnings/debug statements to be printed in the
                          Log.
    :param timeout:       The queue blocks at most timeout seconds for a free
                          slot to execute the put operation on. After the
                          timeout it returns queue Full exception.
    :param bear_instance: The instance of the bear to be executed.
    :param args:          The arguments that are to be passed to the bear.
    :param kwargs:        The keyword arguments that are to be passed to the
                          bear.
    :return:              Returns a valid list of objects of the type Result
                          if the bear executed successfully. None otherwise.
    """
    if kwargs.get('dependency_results', True) is None:
        del kwargs['dependency_results']

    name = bear_instance.name

    try:
        result_list = bear_instance.execute(*args, debug=debug, **kwargs)
    except (Exception, SystemExit) as exc:
        if debug and not isinstance(exc, SystemExit):
            raise

        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.ERROR,
                 'The bear {bear} failed to run with the arguments '
                 '{arglist}, {kwarglist}. Skipping bear...'
                 .format(bear=name, arglist=args, kwarglist=kwargs))
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.DEBUG,
                 'Traceback for error in bear {}:'.format(name),
                 traceback.format_exc(),
                 delimiter='\n')

        return None

    return validate_results(message_queue,
                            timeout,
                            result_list,
                            name,
                            args,
                            kwargs)


def get_local_dependency_results(local_result_list, bear_instance):
    """
    This method gets all the results originating from the dependencies of a
    bear_instance. Each bear_instance may or may not have dependencies.

    :param local_result_list: The list of results out of which the dependency
                              results are picked.
    :param bear_instance:     The instance of a local bear to get the
                              dependencies from.
    :return:                  Return none if there are no dependencies for the
                              bear. Else return a dictionary containing
                              dependency results.
    """
    deps = bear_instance.BEAR_DEPS
    if not deps:
        return None

    dependency_results = {}
    dep_strings = []
    for dep in deps:
        dep_strings.append(dep.__name__)

    for result in local_result_list:
        if result.origin in dep_strings:
            results = dependency_results.get(result.origin, [])
            results.append(result)
            dependency_results[result.origin] = results

    return dependency_results


def run_local_bear(message_queue,
                   timeout,
                   local_result_list,
                   file_dict,
                   bear_instance,
                   filename,
                   debug=False,
                   debug_bears=False):
    """
    Runs an instance of a local bear. Checks if bear_instance is of type
    LocalBear and then passes it to the run_bear to execute.

    :param message_queue:     A queue that contains messages of type
                              errors/warnings/debug statements to be printed in
                              the Log.
    :param timeout:           The queue blocks at most timeout seconds for a
                              free slot to execute the put operation on. After
                              the timeout it returns queue Full exception.
    :param local_result_list: Its a list that stores the results of all local
                              bears.
    :param file_dict:         Dictionary containing contents of file.
    :param bear_instance:     Instance of LocalBear the run.
    :param filename:          Name of the file to run it on.
    :return:                  Returns a list of results generated by the passed
                              bear_instance.
    """
    if (not isinstance(bear_instance, LocalBear) or
            bear_instance.kind() != BEAR_KIND.LOCAL):
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.WARNING,
                 'A given local bear ({}) is not valid. Leaving '
                 'it out...'.format(bear_instance.__class__.__name__),
                 Constants.THIS_IS_A_BUG)

        return None

    kwargs = {'dependency_results':
              get_local_dependency_results(local_result_list,
                                           bear_instance),
              'debug': debug,
              'debug_bears':debug_bears}
    return run_bear(message_queue,
                    timeout,
                    bear_instance,
                    filename,
                    file_dict[filename],
                    **kwargs)


def run_global_bear(message_queue,
                    timeout,
                    global_bear_instance,
                    dependency_results,
                    debug=False,
                    debug_bears=False):
    """
    Runs an instance of a global bear. Checks if bear_instance is of type
    GlobalBear and then passes it to the run_bear to execute.

    :param message_queue:        A queue that contains messages of type
                                 errors/warnings/debug statements to be printed
                                 in the Log.
    :param timeout:              The queue blocks at most timeout seconds for a
                                 free slot to execute the put operation on.
                                 After the timeout it returns queue Full
                                 exception.
    :param global_bear_instance: Instance of GlobalBear to run.
    :param dependency_results:   The results of all the bears on which the
                                 instance of the passed bear to be run depends
                                 on.
    :return:                     Returns a list of results generated by the
                                 passed bear_instance.
    """
    if (not isinstance(global_bear_instance, GlobalBear)
            or global_bear_instance.kind() != BEAR_KIND.GLOBAL):
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.WARNING,
                 'A given global bear ({}) is not valid. Leaving it '
                 'out...'
                 .format(global_bear_instance.__class__.__name__),
                 Constants.THIS_IS_A_BUG)

        return None

    kwargs = {'dependency_results': dependency_results,
              'debug': debug,
              'debug_bears':debug_bears}
    return run_bear(message_queue,
                    timeout,
                    global_bear_instance,
                    **kwargs)


def run_local_bears_on_file(message_queue,
                            timeout,
                            file_dict,
                            local_bear_list,
                            local_result_dict,
                            control_queue,
                            filename,
                            debug=False,
                            debug_bears=False):
    """
    This method runs a list of local bears on one file.

    :param message_queue:     A queue that contains messages of type
                              errors/warnings/debug statements to be printed
                              in the Log.
    :param timeout:           The queue blocks at most timeout seconds for a
                              free slot to execute the put operation on. After
                              the timeout it returns queue Full exception.
    :param file_dict:         Dictionary that contains contents of files.
    :param local_bear_list:   List of local bears to run on file.
    :param local_result_dict: A Manager.dict that will be used to store local
                              bear results. A list of all local bear results
                              will be stored with the filename as key.
    :param control_queue:     If any result gets written to the result_dict a
                              tuple containing a CONTROL_ELEMENT (to indicate
                              what kind of event happened) and either a bear
                              name(for global results) or a file name to
                              indicate the result will be put to the queue.
    :param filename:          The name of file on which to run the bears.
    """
    if filename not in file_dict:
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.ERROR,
                 'An internal error occurred.',
                 Constants.THIS_IS_A_BUG)
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.DEBUG,
                 'The given file through the queue is not in the file '
                 'dictionary.')

        return

    local_result_list = []
    for bear_instance in local_bear_list:
        result = run_local_bear(message_queue,
                                timeout,
                                local_result_list,
                                file_dict,
                                bear_instance,
                                filename,
                                debug=debug,
                                debug_bears=debug_bears)
        if result is not None:
            local_result_list.extend(result)

    local_result_dict[filename] = local_result_list
    control_queue.put((CONTROL_ELEMENT.LOCAL, filename))


def get_global_dependency_results(global_result_dict, bear_instance):
    """
    This method gets all the results originating from the dependencies of a
    bear_instance. Each bear_instance may or may not have dependencies.

    :param global_result_dict: The list of results out of which the dependency
                               results are picked.
    :return:                   None if bear has no dependencies, False if
                               dependencies are not met, the dependency dict
                               otherwise.
    """
    try:
        deps = bear_instance.BEAR_DEPS
        if not deps:
            return None
    except AttributeError:
        # When this occurs we have an invalid bear and a warning will be
        # emitted later.
        return None

    dependency_results = {}
    for dep in deps:
        depname = dep.__name__
        if depname not in global_result_dict:
            return False

        dependency_results[depname] = global_result_dict[depname]

    return dependency_results


def get_next_global_bear(timeout,
                         global_bear_queue,
                         global_bear_list,
                         global_result_dict):
    """
    Retrieves the next global bear.

    :param timeout:            The queue blocks at most timeout seconds for a
                               free slot to execute the put operation on. After
                               the timeout it returns queue Full exception.
    :param global_bear_queue:  queue (read, write) of indexes of global bear
                               instances in the global_bear_list.
    :param global_bear_list:   A list containing all global bears to be
                               executed.
    :param global_result_dict: A Manager.dict that will be used to store global
                               results. The list of results of one global bear
                               will be stored with the bear name as key.
    :return:                   (bear, bearname, dependency_results)
    """
    dependency_results = False

    while dependency_results is False:
        bear_id = global_bear_queue.get(timeout=timeout)
        bear = global_bear_list[bear_id]

        dependency_results = (
            get_global_dependency_results(global_result_dict, bear))
        if dependency_results is False:
            global_bear_queue.put(bear_id)

    return bear, dependency_results


def task_done(obj):
    """
    Invokes task_done if the given queue provides this operation. Otherwise
    passes silently.

    :param obj: Any object.
    """
    if hasattr(obj, 'task_done'):
        obj.task_done()


def run_local_bears(filename_queue,
                    message_queue,
                    timeout,
                    file_dict,
                    local_bear_list,
                    local_result_dict,
                    control_queue,
                    debug=False,
                    debug_bears=False):
    """
    Run local bears on all the files given.

    :param filename_queue:    queue (read) of file names to check with
                              local bears.
    :param message_queue:     A queue that contains messages of type
                              errors/warnings/debug statements to be printed
                              in the Log.
    :param timeout:           The queue blocks at most timeout seconds for a
                              free slot to execute the put operation on. After
                              the timeout it returns queue Full exception.
    :param file_dict:         Dictionary that contains contents of files.
    :param local_bear_list:   List of local bears to run.
    :param local_result_dict: A Manager.dict that will be used to store local
                              bear results. A list of all local bear results
                              will be stored with the filename as key.
    :param control_queue:     If any result gets written to the result_dict a
                              tuple containing a CONTROL_ELEMENT (to indicate
                              what kind of event happened) and either a bear
                              name(for global results) or a file name to
                              indicate the result will be put to the queue.
    """
    try:
        while True:
            filename = filename_queue.get(timeout=timeout)
            run_local_bears_on_file(message_queue,
                                    timeout,
                                    file_dict,
                                    local_bear_list,
                                    local_result_dict,
                                    control_queue,
                                    filename,
                                    debug=debug,
                                    debug_bears=debug_bears)
            task_done(filename_queue)
    except queue.Empty:
        return


def run_global_bears(message_queue,
                     timeout,
                     global_bear_queue,
                     global_bear_list,
                     global_result_dict,
                     control_queue,
                     debug=False,
                     debug_bears=False):
    """
    Run all global bears.

    :param message_queue:      A queue that contains messages of type
                               errors/warnings/debug statements to be printed
                               in the Log.
    :param timeout:            The queue blocks at most timeout seconds for a
                               free slot to execute the put operation on. After
                               the timeout it returns queue Full exception.
    :param global_bear_queue:  queue (read, write) of indexes of global bear
                               instances in the global_bear_list.
    :param global_bear_list:   list of global bear instances
    :param global_result_dict: A Manager.dict that will be used to store global
                               results. The list of results of one global bear
                               will be stored with the bear name as key.
    :param control_queue:      If any result gets written to the result_dict a
                               tuple containing a CONTROL_ELEMENT (to indicate
                               what kind of event happened) and either a bear
                               name(for global results) or a file name to
                               indicate the result will be put to the queue.
    """
    try:
        while True:
            bear, dep_results = (
                get_next_global_bear(timeout,
                                     global_bear_queue,
                                     global_bear_list,
                                     global_result_dict))
            bearname = bear.__class__.__name__
            result = run_global_bear(message_queue, timeout, bear, dep_results,
                                     debug=debug,debug_bears=debug_bears)
            if result:
                global_result_dict[bearname] = result
                control_queue.put((CONTROL_ELEMENT.GLOBAL, bearname))
            else:
                global_result_dict[bearname] = None
            task_done(global_bear_queue)
    except queue.Empty:
        return


def run(file_name_queue,
        local_bear_list,
        global_bear_list,
        global_bear_queue,
        file_dict,
        local_result_dict,
        global_result_dict,
        message_queue,
        control_queue,
        timeout=0,
        debug=False,
        debug_bears = False):
    """
    This is the method that is actually runs by processes.

    If parameters type is 'queue (read)' this means it has to implement the
    get(timeout=TIMEOUT) method and it shall raise queue.Empty if the queue
    is empty up until the end of the timeout. If the queue has the
    (optional!) task_done() attribute, the run method will call it after
    processing each item.

    If parameters type is 'queue (write)' it shall implement the
    put(object, timeout=TIMEOUT) method.

    If the queues raise any exception not specified here the user will get
    an 'unknown error' message. So beware of that.

    :param file_name_queue:    queue (read) of file names to check with local
                               bears. Each invocation of the run method needs
                               one such queue which it checks with all the
                               local bears. The queue could be empty.
                               (Repeat until queue empty.)
    :param local_bear_list:    List of local bear instances.
    :param global_bear_list:   List of global bear instances.
    :param global_bear_queue:  queue (read, write) of indexes of global bear
                               instances in the global_bear_list.
    :param file_dict:          dict of all files as {filename:file}, file as in
                               file.readlines().
    :param local_result_dict:  A Manager.dict that will be used to store local
                               results. A list of all local results.
                               will be stored with the filename as key.
    :param global_result_dict: A Manager.dict that will be used to store global
                               results. The list of results of one global bear
                               will be stored with the bear name as key.
    :param message_queue:      queue (write) for debug/warning/error
                               messages (type LogMessage)
    :param control_queue:      queue (write). If any result gets written to the
                               result_dict a tuple containing a CONTROL_ELEMENT
                               (to indicate what kind of event happened) and
                               either a bear name (for global results) or a
                               file name to indicate the result will be put to
                               the queue. If the run method finished all its
                               local bears it will put
                               (CONTROL_ELEMENT.LOCAL_FINISHED, None) to the
                               queue, if it finished all global ones,
                               (CONTROL_ELEMENT.GLOBAL_FINISHED, None) will
                               be put there.
    :param timeout:            The queue blocks at most timeout seconds for a
                               free slot to execute the put operation on. After
                               the timeout it returns queue Full exception.
    """
    try:
        run_local_bears(file_name_queue,
                        message_queue,
                        timeout,
                        file_dict,
                        local_bear_list,
                        local_result_dict,
                        control_queue,
                        debug=debug,
                        debug_bears = debug_bears)
        control_queue.put((CONTROL_ELEMENT.LOCAL_FINISHED, None))

        run_global_bears(message_queue,
                         timeout,
                         global_bear_queue,
                         global_bear_list,
                         global_result_dict,
                         control_queue,
                         debug=debug,
                         debug_bears = debug_bears)
        control_queue.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))
    except (OSError, KeyboardInterrupt):  # pragma: no cover
        if debug:
            raise
