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


class ProcessManager:
    def __init__(self, settings, filenames, local_filter_classes, global_filter_classes):
        """
        :param settings: Settings object
        :param filenames: Filenames to check
        :param local_filter_classes: list of localfilter classes
        :param global_filter_classes: list of globalfilter classes
        """
        self.job_count = multiprocessing.cpu_count()
        # retrieve job_count from settings

    def run(self):
        raise NotImplementedError
