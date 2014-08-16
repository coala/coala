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
import os
from coalib.misc.i18n import _
from coalib.collecting.Collector import Collector
from coalib.output.LogPrinter import LogPrinter


class FileCollector(Collector):
    def __init__(self, log_printer, flat_dirs=None, rec_dirs=None, allowed=None, forbidden=None, ignored=None):
        """
        :param log_printer: LogPrinter to handel logging of debug, warning and error messages.
        :param flat_dirs: list of strings: directories from which files should be collected excluding sub directories.
        :param rec_dirs: list of strings: directories from which files should be collected including sub directories.
        :param allowed: list of strings: file types that should be collected. Default is all.
        :param forbidden: list of strings: file types that should not be collected. Default is none.
        :param ignored: list of strings: directories or files that should be ignored.
        """
        if flat_dirs is None:
            flat_dirs = []
        if rec_dirs is None:
            rec_dirs = []
        if allowed is None:
            allowed = []
        if forbidden is None:
            forbidden = []
        if ignored is None:
            ignored = []

        if not isinstance(log_printer, LogPrinter):
            raise(TypeError(_("log_printer should be an instance of LogPrinter")))
        if not isinstance(flat_dirs, list):
            raise(TypeError(_("flat_dirs should be of type list")))
        if not isinstance(rec_dirs, list):
            raise(TypeError(_("rec_dirs should be of type list")))
        if not isinstance(allowed, list):
            raise(TypeError(_("allowed should be of type list")))
        if not isinstance(forbidden, list):
            raise(TypeError(_("forbidden should be of type list")))
        if not isinstance(ignored, list):
            raise(TypeError(_("ignored should be of type list")))

        Collector.__init__(self)
        self.log_printer = log_printer
        self._flat_dirs = [os.path.abspath(f_dir) for f_dir in flat_dirs]
        self._rec_dirs = [os.path.abspath(r_dir) for r_dir in rec_dirs]
        self._allowed = allowed
        self._forbidden = forbidden
        self._ignored = [os.path.abspath(path) for path in ignored]

    def _is_target(self, file_name):
        """
        :param file_name: absolute path to a file
        :return: Bool value to determine if the file should be collected
        """
        if file_name in self._ignored:
            return False

        file_type = os.path.splitext(os.path.basename(file_name))[1]
        if file_type in self._allowed:
            return True
        elif (not self._allowed) and (file_type not in self._forbidden):
            return True
        else:
            return False

    def _dir_tree(self, directory):
        """
        :param directory: absolute path to a directory
        :return: list of absolute paths to this directory and all sub directories
        """
        dir_list = [directory]
        try:
            for sub_dir in os.listdir(directory):
                abs_sub_dir = os.path.join(directory, sub_dir)
                if os.path.isdir(abs_sub_dir):
                    if not abs_sub_dir in self._ignored:
                        dir_list.extend(self._dir_tree(abs_sub_dir))
            return dir_list
        except OSError:
            self.log_printer.warn(_("{} is not accessible and will be ignored!").format(directory))
            return []

    def _dir_files(self, directory):
        """
        :param directory: absolute path to a directory
        :return: list of absolute paths to all files in that directory
        """
        file_list = []
        try:
            for file in os.listdir(directory):
                abs_file = os.path.join(directory, file)
                if os.path.isfile(abs_file):
                    if self._is_target(abs_file):
                        file_list.append(abs_file)
        except OSError:
            self.log_printer.warn(_("{} is not accessible and will be ignored!").format(directory))
            return []

        return file_list

    def collect(self):
        """
        :return: list of absolute file paths to all collected files
        """
        all_dirs = self._flat_dirs
        for rec_dir in self._rec_dirs:
            all_dirs.extend(self._dir_tree(rec_dir))
        files = []
        for a_dir in all_dirs:
            files.extend(self._dir_files(a_dir))
        self._items = files

        return files
