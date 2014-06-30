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
from codeclib.internal.process_managing.Process import Process


class FilterProcess(Process):
    def __init__(self, settings, file_name_queue, result_queue):
        """
        This is the object that actually runs on the processes

        :param settings: Settings object
        :param file_name_queue: multiprocessing.queue of file names to check
        :param result_queue: queue for results
        """
        Process.__init__(self)
        self.settings = settings
        # TODO

    def run(self):
        raise NotImplementedError

    def __run_local_filter(self, local_filter_class):
        raise NotImplementedError

    def __run_global_filter(self, global_filter_class):
        raise NotImplementedError
