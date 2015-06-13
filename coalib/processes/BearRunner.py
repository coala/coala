import queue
import multiprocessing
import traceback

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear
from coalib.misc.StringConstants import StringConstants
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.processes.communication.LogMessage import LogMessage, LOG_LEVEL
from coalib.misc.i18n import _
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

    if not isinstance(result_list, list):
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.ERROR,
                 _("The results from the bear {bear} couldn't be processed "
                   "with arguments {arglist}, {kwarglist}.")
                 .format(bear=name, arglist=args, kwarglist=kwargs))
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.DEBUG,
                 _("The return value of the {bear} is an instance of {ret}"
                   " but should be an instance of list.")
                 .format(bear=name, ret=result_list.__class__))
        return None

    for result in result_list:
        if not isinstance(result, Result):
            send_msg(message_queue,
                     timeout,
                     LOG_LEVEL.ERROR,
                     _("The results from the bear {bear} could only be "
                       "partially processed with arguments {arglist}, "
                       "{kwarglist}")
                     .format(bear=name, arglist=args, kwarglist=kwargs))
            send_msg(message_queue,
                     timeout,
                     LOG_LEVEL.DEBUG,
                     _("One of the results in the list for the bear {bear} is "
                       "an instance of {ret} but it should be an instance of "
                       "Result")
                     .format(bear=name, ret=result.__class__))
            result_list.remove(result)

    return result_list


def run_bear(message_queue, timeout, bear_instance, *args, **kwargs):
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
                          if the bear executed succesfully. None otherwise.
    """
    if kwargs.get("dependency_results", True) is None:
        del kwargs["dependency_results"]

    name = bear_instance.__class__.__name__

    try:
        result_list = bear_instance.execute(*args,
                                            **kwargs)
    except:
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.ERROR,
                 _("The bear {bear} failed to run with the arguments "
                   "{arglist}, {kwarglist}. Skipping bear...")
                 .format(bear=name, arglist=args, kwarglist=kwargs))
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.DEBUG,
                 _("Traceback for error in bear {bear}:")
                 .format(bear=name),
                 traceback.format_exc(),
                 delimiter="\n")

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
    :return:                  Return none if their are no dependencies for the
                              bear. Else return a dictionary containing
                              dependency results.
    """
    deps = bear_instance.get_dependencies()
    if deps == []:
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
                   filename):
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
    if not isinstance(bear_instance, LocalBear) or \
            bear_instance.kind() != BEAR_KIND.LOCAL:
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.WARNING,
                 _("A given local bear ({}) is not valid. Leaving "
                   "it out...").format(bear_instance.__class__.__name__),
                 StringConstants.THIS_IS_A_BUG)

        return None

    kwargs = {"dependency_results":
                  get_local_dependency_results(local_result_list,
                                               bear_instance)}
    return run_bear(message_queue,
                    timeout,
                    bear_instance,
                    filename,
                    file_dict[filename],
                    **kwargs)


def run_global_bear(message_queue,
                    timeout,
                    global_bear_instance,
                    dependency_results):
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
    if not isinstance(global_bear_instance, GlobalBear) \
            or global_bear_instance.kind() != BEAR_KIND.GLOBAL:
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.WARNING,
                 _("A given global bear ({}) is not valid. Leaving it "
                   "out...")
                 .format(global_bear_instance.__class__.__name__),
                 StringConstants.THIS_IS_A_BUG)

        return None

    kwargs = {"dependency_results": dependency_results}
    return run_bear(message_queue,
                    timeout,
                    global_bear_instance,
                    **kwargs)


class BearRunner(multiprocessing.Process):
    def __init__(self,
                 file_name_queue,
                 local_bear_list,
                 global_bear_list,
                 global_bear_queue,
                 file_dict,
                 local_result_dict,
                 global_result_dict,
                 message_queue,
                 control_queue,
                 TIMEOUT=0):
        """
        This is the object that actually runs on the processes

        If parameters type is 'queue (read)' this means it has to implement the
        get(timeout=TIMEOUT) method and it shall raise queue.Empty if the queue
        is empty up until the end of the timeout. If the queue has the
        (optional!) task_done() attribute, BearRunner will call it after
        processing each item.

        If parameters type is 'queue (write)' it shall implement the
        put(object, timeout=TIMEOUT) method.

        If the queues raise any exception not specified here the user will get
        an 'unknown error' message. So beware of that.

        :param file_name_queue:    queue (read) of file names to check with
                                   local bears. Every BearRunner takes one of
                                   those and checks it with all local bears.
                                   (Repeat until queue empty.)
        :param local_bear_list:    list of local bear instances
        :param global_bear_list:   list of global bear instances
        :param global_bear_queue:  queue (read, write) of indexes of global
                                   bear instances in the global_bear_list
        :param file_dict:          dict of all files as {filename:file}, file
                                   as in file.readlines()
        :param local_result_dict:  A Manager.dict that will be used to store
                                   local results. A list of all local results
                                   will be stored with the filename as key.
        :param global_result_dict: A Manager.dict that will be used to store
                                   global results. The list of results of one
                                   global bear will be stored with the bear
                                   name as key.
        :param message_queue:      queue (write) for debug/warning/error
                                   messages (type LogMessage)
        :param control_queue:      queue (write). If any result gets written to
                                   the result_dict a tuple containing a
                                   CONTROL_ELEMENT (to indicate what kind of
                                   event happened) and either a bear name
                                   (for global results) or a file name to
                                   indicate the result will be put to the
                                   queue. If this BearRunner finished all its
                                   local bears it will put
                                   (CONTROL_ELEMENT.LOCAL_FINISHED, None) to
                                   the queue, if it finished all global ones,
                                   (CONTROL_ELEMENT.GLOBAL_FINISHED, None) will
                                   be put there.
        :param TIMEOUT:            in seconds for all queue actions
        """
        multiprocessing.Process.__init__(self)

        self.filename_queue = file_name_queue
        self.local_bear_list = local_bear_list
        self.global_bear_queue = global_bear_queue
        self.global_bear_list = global_bear_list

        self.file_dict = file_dict

        self.local_result_dict = local_result_dict
        self.global_result_dict = global_result_dict
        self.message_queue = message_queue
        self.control_queue = control_queue

        self.TIMEOUT = TIMEOUT

        # Will be used to hold local results when they are not yet stored in
        # the result dict
        self._local_result_list = []

    def run(self):
        self.run_local_bears()
        self.control_queue.put((CONTROL_ELEMENT.LOCAL_FINISHED, None))

        self.run_global_bears()
        self.control_queue.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))

    def run_local_bears(self):
        try:
            while True:
                filename = self.filename_queue.get(timeout=self.TIMEOUT)
                self.run_local_bears_on_file(filename)
                if hasattr(self.filename_queue, "task_done"):
                    self.filename_queue.task_done()
        except queue.Empty:
            return

    def _get_global_dependency_results(self, bear_instance):
        """
        Retreives dependency results for a global bear.

        :return: None if bear has no dependencies, False if dependencies are
        not met, the dependency dict otherwise.
        """
        try:
            deps = bear_instance.get_dependencies()
            if deps == []:
                return None
        except AttributeError:
            # When this occurs we have an invalid bear and a warning will be
            # emitted later.
            return None

        dependency_results = {}
        for dep in deps:
            depname = dep.__name__
            if depname not in self.global_result_dict:
                return False

            dependency_results[depname] = self.global_result_dict[depname]

        return dependency_results

    def _get_next_global_bear(self):
        """
        Retrieves the next global bear.

        :return: (bear, bearname, dependency_results)
        """
        dependency_results = False

        while dependency_results is False:
            bear_id = self.global_bear_queue.get(timeout=self.TIMEOUT)
            bear = self.global_bear_list[bear_id]

            dependency_results = self._get_global_dependency_results(bear)
            if dependency_results is False:
                self.global_bear_queue.put(bear_id)

        return bear, bear.__class__.__name__, dependency_results

    def run_global_bears(self):
        try:
            while True:
                bear, bearname, dep_results = self._get_next_global_bear()
                result = run_global_bear(self.message_queue,
                                         self.TIMEOUT,
                                         bear,
                                         dep_results)
                if result:
                    self.global_result_dict[bearname] = result
                    self.control_queue.put((CONTROL_ELEMENT.GLOBAL,
                                            bearname))
                else:
                    self.global_result_dict[bearname] = None
                if hasattr(self.global_bear_queue, "task_done"):
                    self.global_bear_queue.task_done()
        except queue.Empty:
            return

    def run_local_bears_on_file(self, filename):
        if filename not in self.file_dict:
            send_msg(self.message_queue,
                     self.TIMEOUT,
                     LOG_LEVEL.ERROR,
                     _("An internal error occurred."),
                     StringConstants.THIS_IS_A_BUG)
            send_msg(self.message_queue,
                     self.TIMEOUT,
                     LOG_LEVEL.DEBUG,
                     _("The given file through the queue is not in the file "
                       "dictionary."))

            return

        self._local_result_list = []
        for bear_instance in self.local_bear_list:
            r = run_local_bear(self.message_queue,
                               self.TIMEOUT,
                               self._local_result_list,
                               self.file_dict,
                               bear_instance,
                               filename)
            if r is not None:
                self._local_result_list.extend(r)

        self.local_result_dict[filename] = self._local_result_list
        self.control_queue.put((CONTROL_ELEMENT.LOCAL, filename))
