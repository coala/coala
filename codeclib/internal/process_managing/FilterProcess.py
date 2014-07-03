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
import sys
import traceback
from codeclib.fillib.filters.FilterBase import FILTER_KIND
from codeclib.internal.process_managing.Process import Process
from codeclib.internal.process_managing.ResultContainer import ResultContainer


# dummy until translations are working
def _(val):
    return val


class FilterProcess(Process):
    def __init__(self,
                 settings,
                 file_name_queue,
                 local_filter_list,
                 global_filter_queue,
                 file_dict,
                 result_queue,
                 debug_queue,
                 warning_queue,
                 error_queue):
        """
        This is the object that actually runs on the processes

        :param settings: Settings object
        :param file_name_queue: multiprocessing.queue of file names to check with local filters
        :param local_filter_list: list of local filter instances
        :param global_filter_queue: multiprocessing.queue of global filter instances
        :param file_dict: dict of all files as {filename:file}, file as in file.readlines()
        :param result_queue: queue for results
        :param debug_queue: for debug messages
        :param warning_queue: for warnings
        :param error_queue: for errors
        """
        Process.__init__(self)
        self.settings = settings

        self.file_name_queue = file_name_queue
        self.local_filter_list = local_filter_list
        self.global_filter_queue = global_filter_queue

        self.file_dict = file_dict

        self.result_queue = result_queue
        self.debug_queue = debug_queue
        self.warning_queue = warning_queue
        self.error_queue = error_queue

        self.TIMEOUT = 0.2

    def run(self):
        """
        1. Takes filenames from the queue and runs all local filters on them.
        2. Takes global filters from the queue and runs them on all files
        :return:
        """
        try:
            self.__run_on_elems_until_queue_empty(self.file_name_queue, self.__run_local_filters)
            self.__run_on_elems_until_queue_empty(self.global_filter_queue, self.__run_global_filter)
        except:
            exception = sys.exc_info()
            self.__debug("Unknown failure in worker process.\n"
                         "Exception: {}\nTraceback:\n{}".format(str(exception[0]), traceback.extract_tb(exception[2])))
            self.__warn(_("An unknown failure occurred and a process is aborted. "
                          "Please contact developers for assistance and try out starting codec with -j1."))


    def __run_on_elems_until_queue_empty(self, q, function):
        """
        Runs function on queue elements until queue is empty
        :param q: the queue
        :param function: the function to apply on each element
        """
        try:
            while True:
                elem = q.get(timeout=self.TIMEOUT)
                try:
                    function(elem)
                except:
                    self.__debug(_("Failed to handle queue element {}. If you are testing filters, make sure they"
                                   " inherit from GlobalFilter or LocalFilter and don't"
                                   " overwrite the kind() method.").format(elem))
                    self.__err(_("Failed to handle queue element {}.").format(elem))
                finally:
                    q.task_done()
        except queue.Empty:
            self.__debug(_("Queue timeout reached. Assuming no tasks are left."))

    def __run_local_filters(self, filename):
        for filter_instance in self.local_filter_list:
            self.__run_local_filter(filter_instance, filename)

    def __run_local_filter(self, filter_instance, filename):
        assert filter_instance.kind() == FILTER_KIND.LOCAL
        try:
            results = filter_instance.run(filename, self.file_dict[filename])
        except:
            exception = sys.exc_info()
            filter_name = filter_instance.__class__.__name__
            msg = _("Local filter {} raised an exception of type {}. If you are the writer of this filter, "
                    "please catch all exceptions. If not and this error keeps occurring you might want to get "
                    "in contact with the writer of this filter.").format(filter_name, str(exception[0]))
            self.__debug(msg)
            self.__warn(_("Filter {} failed to run.").format(filter_name))

        contained_results = ResultContainer()
        for result in results:
            contained_results.append(result)

        self.result_queue.put(contained_results)

    def __run_global_filter(self, global_filter_instance):
        raise NotImplementedError

    def __warn(self, message):
        self.warning_queue.put(message, timeout=self.TIMEOUT)

    def __err(self, message):
        self.error_queue.put(message, timeout=self.TIMEOUT)

    def __debug(self, message):
        self.debug_queue.put(message, timeout=self.TIMEOUT)
