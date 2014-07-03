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
import queue
from codeclib.fillib.filters.FilterBase import FILTER_KIND
from codeclib.internal.process_managing.Process import Process
from codeclib.internal.process_managing.ResultContainer import ResultContainer


class FilterProcess(Process):
    def __init__(self, settings, file_name_queue, local_filter_list, global_filter_queue, file_dict, result_queue):
        """
        This is the object that actually runs on the processes

        :param settings: Settings object
        :param file_name_queue: multiprocessing.queue of file names to check with local filters
        :param local_filter_list: list of local filter instances
        :param global_filter_queue: multiprocessing.queue of global filter instances
        :param file_dict: dict of all files as {filename:file}, file as in file.readlines()
        :param result_queue: queue for results
        """
        Process.__init__(self)
        self.settings = settings
        self.file_name_queue = file_name_queue
        self.local_filter_list = local_filter_list
        self.global_filter_queue = global_filter_queue
        self.file_dict = file_dict
        self.result_queue = result_queue

    def run(self):
        """
        1. Takes filenames from the queue and runs all local filters on them.
        2. Takes global filters from the queue and runs them on all files
        :return:
        """
        self.__run_on_elems_until_queue_empty(self.file_name_queue, self.__run_local_filters)
        self.__run_on_elems_until_queue_empty(self.global_filter_queue, self.__run_global_filter)

    def __run_on_elems_until_queue_empty(self, q, function):
        """
        Runs function on queue elements until queue is empty
        :param q: the queue
        :param function: the function to apply on each element
        """
        try:
            while True:
                elem = q.get_nowait()
                function(elem)
        except queue.Empty:
            return

    def __run_local_filters(self, filename):
        for filter_instance in self.local_filter_list:
            self.__run_local_filter(filter_instance, filename)

    def __run_filter(self, filter_instance, filename):
        assert filter_instance.kind() == FILTER_KIND.LOCAL
        results = filter_instance.run(filename, self.file_dict[filename])

        contained_results = ResultContainer()
        for result in results:
            contained_results.append(result)

        self.result_queue.put(contained_results)

    def __run_global_filter(self, global_filter_instance):
        raise NotImplementedError
