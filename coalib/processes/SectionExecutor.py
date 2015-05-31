import multiprocessing
import queue
import threading

from coalib.collecting.Collectors import collect_files
from coalib.collecting import Dependencies
from coalib.output.printers import LOG_LEVEL
from coalib.processes.BearRunner import BearRunner
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.results.HiddenResult import HiddenResult
from coalib.settings.Setting import path_list
from coalib.misc.i18n import _


def get_cpu_count():
    try:
        return multiprocessing.cpu_count()
    # cpu_count is not implemented for some CPU architectures/OSes
    except NotImplementedError:  # pragma: no cover
        return 2


class SectionExecutor:
    """
    The section executor does the following things:

    1. Prepare a BearRunner
      * Load files
      * Create queues
    2. Spawn up one or more BearRunner's
    3. Output results from the BearRunner's
    4. Join all processes
    """

    class LogPrinterThread(threading.Thread):
        """
        This is the Thread object that outputs all log messages it gets from
        its message_queue.
        """
        def __init__(self, message_queue, log_printer):
            threading.Thread.__init__(self)
            self.running = True
            self.message_queue = message_queue
            self.log_printer = log_printer

        def run(self):
            while self.running:
                try:
                    elem = self.message_queue.get(timeout=0.1)
                    self.log_printer.log_message(elem)
                except queue.Empty:
                    pass

    def __init__(self,
                 section,
                 local_bear_list,
                 global_bear_list,
                 interactor,
                 log_printer):
        self.section = section
        self.local_bear_list = Dependencies.resolve(local_bear_list)
        self.global_bear_list = Dependencies.resolve(global_bear_list)

        self.interactor = interactor
        self.log_printer = log_printer

    def run(self):
        """
        Executes the section with the given bears.

        :return: Tuple containing a bool (True if results were yielded, False
                 otherwise), a Manager.dict containing all local results
                 (filenames are key) and a Manager.dict containing all global
                 bear results (bear names are key).
        """
        running_processes = get_cpu_count()
        processes, arg_dict = self._instantiate_processes(running_processes)

        logger_thread = self.LogPrinterThread(arg_dict["message_queue"],
                                              self.log_printer)
        # Start and join the logger thread along with the BearRunner's
        processes.append(logger_thread)

        for runner in processes:
            runner.start()

        try:
            return (self._process_queues(processes,
                                         arg_dict["control_queue"],
                                         arg_dict["local_result_dict"],
                                         arg_dict["global_result_dict"],
                                         arg_dict["file_dict"]),
                    arg_dict["local_result_dict"],
                    arg_dict["global_result_dict"])
        finally:
            logger_thread.running = False

            for runner in processes:
                runner.join()

    @staticmethod
    def _get_running_processes(processes):
        return sum((1 if process.is_alive() else 0) for process in processes)

    def _process_queues(self,
                        processes,
                        control_queue,
                        local_result_dict,
                        global_result_dict,
                        file_dict):
        running_processes = self._get_running_processes(processes)
        retval = False
        # Number of processes working on local bears
        local_processes = len(processes)
        global_result_buffer = []

        # One process is the logger thread
        while local_processes > 1 and running_processes > 1:
            try:
                control_elem, index = control_queue.get(timeout=0.1)

                if control_elem == CONTROL_ELEMENT.LOCAL_FINISHED:
                    local_processes -= 1
                elif control_elem == CONTROL_ELEMENT.LOCAL:
                    assert local_processes != 0
                    retval = self._print_result(local_result_dict,
                                                file_dict,
                                                index,
                                                retval)
                elif control_elem == CONTROL_ELEMENT.GLOBAL:
                    global_result_buffer.append(index)
            except queue.Empty:
                running_processes = self._get_running_processes(processes)

        # Flush global result buffer
        for elem in global_result_buffer:
            retval = self._print_result(global_result_dict,
                                        file_dict,
                                        elem,
                                        retval)

        running_processes = self._get_running_processes(processes)
        # One process is the logger thread
        while running_processes > 1:
            try:
                control_elem, index = control_queue.get(timeout=0.1)

                if control_elem == CONTROL_ELEMENT.GLOBAL:
                    retval = self._print_result(global_result_dict,
                                                file_dict,
                                                index,
                                                retval)
                else:
                    assert control_elem == CONTROL_ELEMENT.GLOBAL_FINISHED
                    running_processes = self._get_running_processes(processes)

            except queue.Empty:
                running_processes = self._get_running_processes(processes)

        self.interactor.finalize(file_dict)
        return retval

    @staticmethod
    def _non_hidden_results(result_list):
        results = []
        for result in result_list:
            if not isinstance(result, HiddenResult):
                results.append(result)

        return results

    def _print_result(self, result_dict, file_dict, index, retval):
        results = self._non_hidden_results(result_dict[index])
        self.interactor.print_results(results, file_dict)

        return retval or len(results) > 0

    def _instantiate_bears(self, file_dict, message_queue):
        for i in range(len(self.local_bear_list)):
            self.local_bear_list[i] = self.local_bear_list[i](self.section,
                                                              message_queue,
                                                              TIMEOUT=0.1)
        for i in range(len(self.global_bear_list)):
            self.global_bear_list[i] = self.global_bear_list[i](file_dict,
                                                                self.section,
                                                                message_queue,
                                                                TIMEOUT=0.1)

    def _instantiate_processes(self, job_count):
        filename_list = collect_files(path_list(self.section.get('files',
                                                                 "")),
                                      self.log_printer)
        file_dict = self._get_file_dict(filename_list)

        manager = multiprocessing.Manager()
        global_bear_queue = multiprocessing.Queue()
        filename_queue = multiprocessing.Queue()
        local_result_dict = manager.dict()
        global_result_dict = manager.dict()
        message_queue = multiprocessing.Queue()
        control_queue = multiprocessing.Queue()

        bear_runner_args = {"file_name_queue": filename_queue,
                            "local_bear_list": self.local_bear_list,
                            "global_bear_list": self.global_bear_list,
                            "global_bear_queue": global_bear_queue,
                            "file_dict": file_dict,
                            "local_result_dict": local_result_dict,
                            "global_result_dict": global_result_dict,
                            "message_queue": message_queue,
                            "control_queue": control_queue,
                            "TIMEOUT": 0.1}

        self._instantiate_bears(file_dict,
                                message_queue)
        self._fill_queue(filename_queue, file_dict.keys())
        self._fill_queue(global_bear_queue, range(len(self.global_bear_list)))

        return ([BearRunner(**bear_runner_args) for i in range(job_count)],
                bear_runner_args)

    @staticmethod
    def _fill_queue(_queue, any_list):
        for elem in any_list:
            _queue.put(elem)

    def _get_file_dict(self, filename_list):
        file_dict = {}
        for filename in filename_list:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    file_dict[filename] = f.readlines()
            except UnicodeDecodeError:
                self.log_printer.warn(_("Failed to read file '{}'. It seems "
                                        "to contain non-unicode characters. "
                                        "Leaving it out.".format(filename)))
            except Exception as exception:  # pragma: no cover
                self.log_printer.log_exception(_("Failed to read file '{}' "
                                                 "because of an unknown "
                                                 "error. Leaving it "
                                                 "out.").format(filename),
                                               exception,
                                               log_level=LOG_LEVEL.WARNING)

        return file_dict
