import multiprocessing
import queue
import threading

from coalib.collecting.Collectors import collect_files
from coalib.collecting import Dependencies
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.processes.BearRunner import BearRunner
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.processes.Barrier import Barrier
from coalib.settings.Section import Section
from coalib.settings.Setting import path_list


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
        This is the Thread object that outputs all log messages it gets from its message_queue.
        """
        def __init__(self, message_queue, log_printer=ConsolePrinter()):
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
                 global_bear_list):
        if not isinstance(section, Section):
            raise TypeError("section has to be of type Section")
        if not isinstance(local_bear_list, list):
            raise TypeError("local_bear_list has to be of type list")
        if not isinstance(global_bear_list, list):
            raise TypeError("global_bear_list has to be of type list")

        self.section = section
        self.local_bear_list = Dependencies.resolve(local_bear_list)
        self.global_bear_list = Dependencies.resolve(global_bear_list)

    def run(self):
        filename_list = collect_files(path_list(self.section['files']))
        file_dict = self._get_file_dict(filename_list)

        manager = multiprocessing.Manager()
        global_bear_queue = multiprocessing.Queue()
        filename_queue = multiprocessing.Queue()
        local_result_dict = manager.dict()
        global_result_dict = manager.dict()
        message_queue = multiprocessing.Queue()
        control_queue = multiprocessing.Queue()

        self._instantiate_bears(file_dict, message_queue)

        running_processes = get_cpu_count()
        barrier = Barrier(parties=running_processes)

        bear_runner_args = {"file_name_queue": filename_queue,
                            "local_bear_list": self.local_bear_list,
                            "global_bear_list": self.global_bear_list,
                            "global_bear_queue": global_bear_queue,
                            "file_dict": file_dict,
                            "local_result_dict": local_result_dict,
                            "global_result_dict": global_result_dict,
                            "message_queue": message_queue,
                            "control_queue": control_queue,
                            "barrier": barrier,
                            "TIMEOUT": 0.1}
        processes = [BearRunner(**bear_runner_args) for i in range(running_processes)]
        logger_thread = self.LogPrinterThread(message_queue, self.section.log_printer)
        processes.append(logger_thread)  # Start and join the logger thread along with the BearRunner's

        self._fill_queue(filename_queue, filename_list)
        self._fill_queue(global_bear_queue, range(len(self.global_bear_list)))

        for runner in processes:
            runner.start()

        # One process is the logger thread
        while running_processes > 1:
            try:
                control_elem, index = control_queue.get(timeout=0.1)
                if control_elem == CONTROL_ELEMENT.LOCAL:
                    self.section.interactor.print_results(local_result_dict[index], file_dict)
                elif control_elem == CONTROL_ELEMENT.GLOBAL:
                    self.section.interactor.print_results(global_result_dict[index], file_dict)
                elif control_elem == CONTROL_ELEMENT.FINISHED:
                    running_processes = sum((1 if process.is_alive() else 0) for process in processes)
            except queue.Empty:
                running_processes = sum((1 if process.is_alive() else 0) for process in processes)

        logger_thread.running = False
        self.section.interactor.finalize(file_dict)

        for runner in processes:
            runner.join()

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

    @staticmethod
    def _fill_queue(_queue, any_list):
        for elem in any_list:
            _queue.put(elem)

    @staticmethod
    def _get_file_dict(filename_list):
        file_dict = {}
        for filename in filename_list:
            with open(filename, "r") as f:
                file_dict[filename] = f.readlines()

        return file_dict
