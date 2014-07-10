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
from coalib.internal.process_managing.Process import Process


class ProcessManager:
    def __init__(self, process, job_count=0):
        """
        :param process: the process to run
        :param job_count: if 0 take cpu count
        """
        assert(isinstance(process, Process))
        if job_count == 0:
            try:
                self.__job_count = multiprocessing.cpu_count()
            except NotImplementedError:
                self.__job_count = 1
        else:
            self.__job_count = job_count
        self.__process = process
        self.__processes = []

    def run(self):
        if self.__processes != []:
            return

        for i in range(self.__job_count):
            self.__processes.append(multiprocessing.Process(target=self.__process.run))
            self.__processes[i].start()

    def num_active_processes(self):
        sum(int(process.exitcode == None) for process in self.__processes)

    def join(self):
        """
        :return: an array with the exitcodes of the processes
        """
        exitcodes = []
        for p in self.__processes:
            p.join()
            exitcodes.append(p.exitcode)
        self.__processes = []
        return exitcodes
