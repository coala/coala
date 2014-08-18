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
    def __init__(self, log_printer, flat_dirs=[], rec_dirs=[], allowed=None, forbidden=[], ignored=[]):
        """
        :param log_printer: LogPrinter to handle logging
        :param flat_dirs: list of strings: directories from which files should be collected, excluding sub directories
        :param rec_dirs: list of strings: directories from which files should be collected, including sub directories
        :param allowed: list of strings: file types that should be collected. The default value of None will result in
                        all file types being collected.
        :param forbidden: list of strings: file types that should not be collected. This overwrites allowed file types.
        :param ignored: list of strings: directories or files that should be ignored.
        """

        if not isinstance(log_printer, LogPrinter):
            raise(TypeError("log_printer should be an instance of LogPrinter"))
        if not isinstance(flat_dirs, list):
            raise(TypeError("flat_dirs should be of type list"))
        if not isinstance(rec_dirs, list):
            raise(TypeError("rec_dirs should be of type list"))
        if not (isinstance(allowed, list) or allowed is None):
            raise(TypeError("allowed should be of type list or None"))
        if not isinstance(forbidden, list):
            raise(TypeError("forbidden should be of type list"))
        if not isinstance(ignored, list):
            raise(TypeError("ignored should be of type list"))

        Collector.__init__(self)
        self.log_printer = log_printer
        self._flat_dirs = [os.path.abspath(f_dir) for f_dir in flat_dirs]
        self._rec_dirs = [os.path.abspath(r_dir) for r_dir in rec_dirs]
        self._allowed = allowed
        self._forbidden = forbidden
        self._ignored = [os.path.abspath(path) for path in ignored]

        for ignored_dir in self._ignored:
            for f_dir in self._flat_dirs:
                if ignored_dir in f_dir:
                    self._flat_dirs.remove(f_dir)
            for r_dir in self._rec_dirs:
                if ignored_dir in r_dir:
                    self._rec_dirs.remove(r_dir)

    def _is_target(self, file_path):
        """
        :param file_path: absolute path to a file
        :return: Bool value to determine if the file should be collected
        """
        for ignored_path in self._ignored:
            if ignored_path in file_path:
                return False

        file_type = os.path.splitext(os.path.basename(file_path))[1]
        if file_type in self._forbidden:
            return False
        elif self._allowed is None or file_type in self._allowed:
            return True
        else:
            return False

    def _nonignored_dir_tree(self, directory):
        """
        :param directory: absolute path to a directory
        :return: list of absolute paths of this directory and all subdirectories that are not ignored
        """
        dir_list = [directory]
        try:
            for sub_dir in os.listdir(directory):
                abs_sub_dir = os.path.join(directory, sub_dir)
                if os.path.isdir(abs_sub_dir):
                    if not abs_sub_dir in self._ignored:
                        dir_list.extend(self._nonignored_dir_tree(abs_sub_dir))

            return dir_list
        
        except OSError:
            self.log_printer.warn(_("{} is not accessible and will be ignored!").format(directory))
            return []

    def _dir_files(self, directory):
        """
        :param directory: absolute path to a directory
        :return: list of absolute paths to all target files in that directory
        """
        file_list = []
        try:
            for file in os.listdir(directory):
                abs_file = os.path.join(directory, file)
                if os.path.isfile(abs_file) and self._is_target(abs_file):
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
            all_dirs.extend(self._nonignored_dir_tree(rec_dir))
        files = []
        for a_dir in all_dirs:
            files.extend(self._dir_files(a_dir))
        self._items = files

        return files
