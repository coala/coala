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
                 barrier,
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

        :param file_name_queue: queue (read) of file names to check with local
        bears. Every BearRunner takes one of those and checks it with all local
        bears. (Repeat until queue empty.)
        :param local_bear_list: list of local bear instances
        :param global_bear_list: list of global bear instances
        :param global_bear_queue: queue (read, write) of indexes of global bear
        instances in the global_bear_list
        :param file_dict: dict of all files as {filename:file}, file as in
        file.readlines()
        :param local_result_dict: A Manager.dict that will be used to store
        local results. A list of all local results will be stored with the
        filename as key.
        :param global_result_dict: A Manager.dict that will be used to store
        global results. The list of results of one global bear will be stored
        with the bear name as key.
        :param message_queue: queue (write) for debug/warning/error messages
        (type LogMessage)
        :param control_queue: queue (write). If any result gets written to the
        result_dict a tuple containing a
        CONTROL_ELEMENT (to indicate what kind of event happened) and either a
        filter name (for global results) or a
        file name to indicate the result will be put to the queue. If this
        BearRunner finished all its tasks it will put
        (CONTROL_ELEMENT.FINISHED, None) to the queue.
        :param barrier: a thing that has a wait() method. This will be invoked
        after running the local bears and may serve as a barrier to avoid
        getting global results before local ones are processed.
        :param TIMEOUT: in seconds for all queue actions
        """
        if not isinstance(local_bear_list, list):
            raise TypeError("local_bear_list should be a list")
        if not isinstance(file_dict, dict):
            raise TypeError("file_dict should be a dict")
        if not hasattr(file_name_queue, "get"):
            raise TypeError("file_name_queue should be a queue like thing "
                            "(reading possible via 'get', raises queue.Empty "
                            "if empty)")
        if not isinstance(global_bear_list, list):
            raise TypeError("global_bear_list should be a list")
        if not hasattr(global_bear_queue, "get") or \
                not hasattr(global_bear_queue, "put"):
            raise TypeError("global_bear_queue should be a queue like thing "
                            "(reading possible via 'get', raises queue.Empty "
                            "if empty, writing possible via 'put')")
        if not isinstance(local_result_dict,
                          multiprocessing.managers.DictProxy):
            raise TypeError("local_result_dict should be a "
                            "multiprocessing.managers.DictProxy")
        if not isinstance(global_result_dict,
                          multiprocessing.managers.DictProxy):
            raise TypeError("global_result_dict should be a "
                            "multiprocessing.managers.DictProxy")
        if not hasattr(message_queue, "put"):
            raise TypeError("message_queue should be a queue like thing "
                            "(writing possible via 'put')")
        if not hasattr(control_queue, "put"):
            raise TypeError("control_queue should be a queue like thing "
                            "(writing possible via 'put')")
        if not hasattr(barrier, "wait"):
            raise TypeError("barrier should be a barrier like thing ('wait' "
                            "method should be available)")

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
        self.barrier = barrier

        self.TIMEOUT = TIMEOUT

        # Will be used to hold local results when they are not yet stored in
        # the result dict
        self._local_result_list = []

    def warn(self, *args, delimiter=' ', end=''):
        self.__send_msg(LOG_LEVEL.WARNING, *args, delimiter=delimiter, end=end)

    def err(self, *args, delimiter=' ', end=''):
        self.__send_msg(LOG_LEVEL.ERROR, *args, delimiter=delimiter, end=end)

    def debug(self, *args, delimiter=' ', end=''):
        self.__send_msg(LOG_LEVEL.DEBUG, *args, delimiter=delimiter, end=end)

    def run(self):
        self.run_local_bears()
        self.barrier.wait()
        self.run_global_bears()

        self.control_queue.put((CONTROL_ELEMENT.FINISHED, None))

    def run_local_bears(self):
        try:
            while True:
                filename = self.filename_queue.get(timeout=self.TIMEOUT)
                self.__run_local_bears(filename)
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
                result = self.__run_global_bear(bear, dep_results)
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

    def __send_msg(self, log_level, *args, delimiter=' ', end=''):
        output = str(delimiter).join(str(arg) for arg in args) + str(end)
        self.message_queue.put(LogMessage(log_level, output),
                               timeout=self.TIMEOUT)

    def __run_local_bears(self, filename):
        if filename not in self.file_dict:
            self.err(_("An internal error occurred."),
                     StringConstants.THIS_IS_A_BUG)
            self.debug(_("The given file through the queue is not in the "
                         "file dictionary."))

            return

        self._local_result_list = []
        for bear_instance in self.local_bear_list:
            r = self.__run_local_bear(bear_instance, filename)
            if r is not None:
                self._local_result_list.extend(r)

        self.local_result_dict[filename] = self._local_result_list
        self.control_queue.put((CONTROL_ELEMENT.LOCAL, filename))

    def _get_local_dependency_results(self, bear_instance):
        deps = bear_instance.get_dependencies()
        if deps == []:
            return None

        dependency_results = {}
        dep_strings = []
        for dep in deps:
            dep_strings.append(dep.__name__)

        for result in self._local_result_list:
            if result.origin in dep_strings:
                results = dependency_results.get(result.origin, [])
                results.append(result)
                dependency_results[result.origin] = results

        return dependency_results

    def __run_local_bear(self, bear_instance, filename):
        if not isinstance(bear_instance, LocalBear) or \
                bear_instance.kind() != BEAR_KIND.LOCAL:
            self.warn(_("A given local bear ({}) is not valid. "
                        "Leaving it out...")
                      .format(bear_instance.__class__.__name__),
                      StringConstants.THIS_IS_A_BUG)

            return None

        dependency_results = self._get_local_dependency_results(bear_instance)
        kwargs = {}
        # Only pass dependency results to bears who want it
        if dependency_results is not None:
            kwargs["dependency_results"] = dependency_results

        return self._run_bear(bear_instance,
                              filename,
                              self.file_dict[filename],
                              **kwargs)

    def __run_global_bear(self, global_bear_instance, dependency_results):
        if not isinstance(global_bear_instance, GlobalBear) \
                or global_bear_instance.kind() != BEAR_KIND.GLOBAL:
            self.warn(_("A given global bear ({}) is not valid. "
                        "Leaving it out...")
                      .format(global_bear_instance.__class__.__name__),
                      StringConstants.THIS_IS_A_BUG)

            return None

        kwargs = {}
        # Only pass dependency results to bears who want it
        if dependency_results is not None:
            kwargs["dependency_results"] = dependency_results

        return self._run_bear(global_bear_instance, **kwargs)

    def _run_bear(self, bear_instance, *args, **kwargs):
        try:
            return bear_instance.run(*args,
                                     **kwargs)
        except:
            name = bear_instance.__class__.__name__
            self.err(_("The bear {bear} failed to run with the arguments "
                       "{arglist}, {kwarglist}. Skipping bear...")
                     .format(bear=name, arglist=args, kwarglist=kwargs))
            self.debug(_("Traceback for error in bear {bear}:")
                       .format(bear=name),
                       traceback.format_exc(),
                       delimiter="\n")

            return None
