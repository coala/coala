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
from multiprocessing.queues import Queue
from coalib.collecting.FileCollector import FileCollector
from coalib.output.ConsoleOutputter import ConsoleOutputter
from coalib.output.ConsolePrinter import ConsolePrinter
from coalib.processes.BearRunner import BearRunner
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.processes.Process import Process
from coalib.processes.ProcessSpawner import ProcessSpawner, get_cpu_count
from coalib.settings.Section import Section


class SectionExecutor(Process):
    def __init__(self, outputter=ConsoleOutputter(), log_printer=ConsolePrinter()):
        self.log_printer = log_printer
        self.outputter = outputter

    def run(self, section, global_bear_list, local_bear_list):
        if not isinstance(section, Section):
            raise TypeError("section has to be of type Section")

        global_bear_queue = Queue()
        for bear in global_bear_list:
            global_bear_queue.put(bear)

        filename_list = FileCollector.from_section(section, log_printer=self.log_printer).collect()

        filename_queue = Queue()
        file_dict = {}
        for filename in filename_list:
            filename_queue.put(filename)
            with open(filename, "r") as f:
                file_dict[filename] = f.readlines()

        local_result_queue = Queue()
        global_result_queue = Queue()
        message_queue = Queue()
        control_queue = Queue()

        bear_runner = BearRunner(file_name_queue=filename_queue,
                                 local_bear_list=local_bear_list,
                                 global_bear_queue=global_bear_queue,
                                 file_dict=file_dict,
                                 local_result_queue=local_result_queue,
                                 global_result_queue=global_result_queue,
                                 message_queue=message_queue,
                                 control_queue=control_queue)

        spawner = ProcessSpawner(bear_runner, int(section.get("job_count", get_cpu_count())))
        spawner.run()

        running = True
        while running:
            try:
                elem = control_queue.get(timeout=0.1)
                if elem == CONTROL_ELEMENT.LOCAL:
                    self.outputter.print_local_results(elem, file_dict)
                elif elem == CONTROL_ELEMENT.GLOBAL:
                    pass  # TODO Handle global result
                else:
                    running = spawner.num_active_processes() == 0
            except Queue.Empty:
                running = spawner.num_active_processes() == 0
