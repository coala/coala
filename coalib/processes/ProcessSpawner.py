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

from coalib.processes.Process import Process


def get_cpu_count():
    try:
        return multiprocessing.cpu_count()
        # cpu_count is not implemented for some CPU architectures/OSes
    except NotImplementedError:  # pragma: no cover
        return 2


class ProcessSpawner:
    """
    Spawns job_count processes each running the run method of one instance of a class derived from Process.
    """

    def __init__(self, process, job_count=get_cpu_count()):
        """
        :param process: An instance of a class derived from Process to run
        :param job_count: Number of processes to run
        """
        if not isinstance(process, Process):
            raise TypeError("process needs to be an instance of a derivative of Process.")
        if not isinstance(job_count, int):
            raise TypeError("job_count needs to be an integer.")

        self.__job_count = job_count
        self.__process = process
        self.__processes = []

    def run(self, *args, **kwargs):
        """
        Starts the processes asynchronously. If you want a blocking invocation, use run_blocking.

        :param args: will be passed through to process.run
        :param kwargs: will be passed through to process.run
        """
        if self.__processes != []:
            raise RuntimeError("Processes are already running.")

        for i in range(self.__job_count):
            process = multiprocessing.Process(target=self.__process.run, args=args, kwargs=kwargs)
            process.start()
            self.__processes.append(process)

    def run_blocking(self, *args, **kwargs):
        """
        Runs the process.run method (blocking).

        :param args: will be passed through to process.run
        :param kwargs: will be passed through to process.run

        :return: an array with the exitcodes of the processes
        """
        self.run(*args, **kwargs)
        return self.join()

    def num_active_processes(self):
        """
        :return: the number of active processes
        """
        return sum(int(process.exitcode == None) for process in self.__processes)

    def join(self):
        """
        Waits until all processes end and returns an array of all exit codes.

        :return: an array with the exitcodes of the processes
        """
        exitcodes = []
        for p in self.__processes:
            p.join()
            exitcodes.append(p.exitcode)
        self.__processes = []
        return exitcodes
