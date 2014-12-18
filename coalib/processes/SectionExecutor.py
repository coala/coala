"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import multiprocessing
import queue
from multiprocessing import Process
from coalib.collecting.FileCollector import FileCollector
from coalib.output.ConsoleOutputter import ConsoleOutputter, Outputter
from coalib.output.ConsolePrinter import ConsolePrinter, LogPrinter
from coalib.processes.BearRunner import BearRunner
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.settings.Section import Section


def get_cpu_count():
    try:
        return multiprocessing.cpu_count()
        # cpu_count is not implemented for some CPU architectures/OSes
    except NotImplementedError:  # pragma: no cover
        return 2


def run_bears(kwargs):
    r = BearRunner(**kwargs)
    r.run()


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
    def __init__(self,
                 section,
                 local_bear_list,
                 global_bear_list,
                 outputter=ConsoleOutputter(),
                 log_printer=ConsolePrinter()):
        if not isinstance(section, Section):
            raise TypeError("section has to be of type Section")
        if not isinstance(local_bear_list, list):
            raise TypeError("local_bear_list has to be of type list")
        if not isinstance(global_bear_list, list):
            raise TypeError("global_bear_list has to be of type list")
        if not isinstance(outputter, Outputter):
            raise TypeError("outputter has to be an Outputter")
        if not isinstance(log_printer, LogPrinter):
            raise TypeError("log_printer has to be a log_printer")

        self.section = section
        self.local_bear_list = local_bear_list
        self.global_bear_list = global_bear_list
        self.log_printer = log_printer
        self.outputter = outputter

    def run(self):
        filename_list = FileCollector.from_section(self.section, log_printer=self.log_printer).collect()
        file_dict = self._get_file_dict(filename_list)

        global_bear_queue = multiprocessing.Queue()
        filename_queue = multiprocessing.Queue()
        local_result_queue = multiprocessing.Queue()
        global_result_queue = multiprocessing.Queue()
        message_queue = multiprocessing.Queue()
        control_queue = multiprocessing.Queue()

        for i in range(len(self.local_bear_list)):
            self.local_bear_list[i] = self.local_bear_list[i](self.section, message_queue, TIMEOUT=0.1)
        for i in range(len(self.global_bear_list)):
            self.global_bear_list[i] = self.global_bear_list[i](file_dict, self.section, message_queue, TIMEOUT=0.1)

        bear_runner_args = {"file_name_queue": filename_queue,
                            "local_bear_list": self.local_bear_list,
                            "global_bear_queue": global_bear_queue,
                            "file_dict": file_dict,
                            "local_result_queue": local_result_queue,
                            "global_result_queue": global_result_queue,
                            "message_queue": message_queue,
                            "control_queue": control_queue,
                            "TIMEOUT": 0.1}
        bear_runners = [Process(target=run_bears, args=(bear_runner_args, )) for i in range(get_cpu_count())]

        self._fill_queue(filename_queue, filename_list)
        self._fill_queue(global_bear_queue, self.global_bear_list)

        for runner in bear_runners:
            runner.start()

        running = True
        while running:
            try:
                print("Waiting on control queue...")
                elem = control_queue.get(timeout=0.1)
                print("Got control element", elem)
                if elem == CONTROL_ELEMENT.LOCAL:
                    print("LOCAL RESULT")
                    self.outputter.print_results(local_result_queue.get(), file_dict)
                elif elem == CONTROL_ELEMENT.GLOBAL:
                    print("GLOBAL RESULT")
                    self.outputter.print_results(global_result_queue.get(), file_dict)
                else:
                    running = not all(process.exitcode is None for process in bear_runners)
            except queue.Empty:
                print("Got nothing on control queue")
                running = not all(process.exitcode is None for process in bear_runners)

        for runner in bear_runners:
            runner.join()

        print("joined")

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
