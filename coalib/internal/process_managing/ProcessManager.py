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
        assert(type(process) == Process)
        if job_count == 0:
            self.__job_count = multiprocessing.cpu_count()
        else:
            self.__job_count = job_count
        self.__process = process
        self.__processes = []

    def run(self):
        if self.__processes != []:
            return

        for i in range(self.__job_count):
            self.__processes.append(multiprocessing.Process(target=self.__process.run()))
            self.__processes[i].start()

    def num_active_processes(self):
        sum(int(process.exitcode == None) for process in self.__processes)

    def join(self):
        for p in self.__processes:
            p.join()
        self.__processes = []
