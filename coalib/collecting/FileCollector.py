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
import re

from coalib.collecting.Collector import Collector
from coalib.output.LogPrinter import LogPrinter
from coalib.misc.StringConstants import StringConstants
from coalib.output.ConsolePrinter import ConsolePrinter
from coalib.settings.Section import Section
from coalib.settings.Setting import path_list


class FileCollector(Collector):
    def __init__(self,
                 files=[],
                 regex="",
                 flat_dirs=[],
                 rec_dirs=[],
                 allowed_types=None,
                 ignored_files=[],
                 ignored_dirs=[],
                 log_printer=ConsolePrinter()):
        """
        :param files: Absolute path to files that will always be collected if accessible
        :param regex: Regex to match with files to collect
        :param flat_dirs: list of strings: directories from which files should be collected, excluding sub directories
        :param rec_dirs: list of strings: directories from which files should be collected, including sub
                               directories
        :param allowed_types: list of strings: file types that should be collected. The default value of None will
                              result in all file types being collected.
        :param ignored_files: list of strings: files that should be ignored.
        :param ignored_dirs: list of strings: directories that should be ignored.
        :param log_printer: LogPrinter to handle logging
        """
        if not isinstance(log_printer, LogPrinter):
            raise TypeError("log_printer should be an instance of LogPrinter")
        if not isinstance(files, list):
            raise TypeError("files should be of type list")
        if not isinstance(regex, str):
            raise TypeError("regex should be of type string")
        if not isinstance(flat_dirs, list):
            raise TypeError("flat_dirs should be of type list")
        if not isinstance(rec_dirs, list):
            raise TypeError("rec_dirs should be of type list")
        if not (isinstance(allowed_types, list) or allowed_types is None):
            raise TypeError("allowed should be of type list or None")
        if not isinstance(ignored_files, list):
            raise TypeError("ignored should be of type list")
        if not isinstance(ignored_dirs, list):
            raise TypeError("ignored should be of type list")

        Collector.__init__(self)
        self.log_printer = log_printer

        self._regex = self.prepare_regex(regex)

        self._prelim_files = [os.path.abspath(a_file) for a_file in files]
        self._prelim_flat_dirs = [os.path.abspath(f_dir) for f_dir in flat_dirs]
        self._prelim_rec_dirs = [os.path.abspath(r_dir) for r_dir in rec_dirs]
        self.unfolded = False

        self._files = []
        self._flat_dirs = []
        self._rec_dirs = []

        if allowed_types is not None:
            self._allowed_types = [t.lower().lstrip('.') for t in allowed_types]
        else:
            self._allowed_types = None
        self._ignored_files = [os.path.abspath(path) for path in ignored_files]
        self._ignored_dirs = [os.path.abspath(path) for path in ignored_dirs]

    @classmethod
    def from_section(cls, section):
        if not isinstance(section, Section):
            raise TypeError("section should be of type Section.")

        return cls(files=path_list(section["files"]),
                   flat_dirs=path_list(section["flat_dirs"]),
                   rec_dirs=path_list(section["rec_dirs"]),
                   ignored_dirs=path_list(section["ignored_dirs"]),
                   allowed_types=[],
                   log_printer=section.log_printer)

    @staticmethod
    def prepare_regex(regex):
        if regex.endswith("$"):
            return regex

        return regex + "$"

    def _is_target(self, file_path):
        """
        :param file_path: absolute path to a file
        :return: Bool value to determine if the file should be collected

        This method assumes that the given path lies in a directory that should be collected. However it will check if
        the path is a subpath of an ignored directory.
        """
        for ignored_path in self._ignored_files:
            if file_path.startswith(ignored_path):
                return False

        if self._regex != "$" and re.match(self._regex, os.path.split(file_path)[1]):
            return True

        file_type = os.path.splitext(os.path.basename(file_path))[1].lower().lstrip('.')
        if self._allowed_types is None or file_type in self._allowed_types:
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
                    if not abs_sub_dir in self._ignored_dirs:
                        dir_list.extend(self._nonignored_dir_tree(abs_sub_dir))

            return dir_list

        except OSError:
            self.log_printer.warn(StringConstants.OBJ_NOT_ACCESSIBLE.format(directory))
            return []

    def _get_files_from_dir(self, directory):
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
            self.log_printer.warn(StringConstants.OBJ_NOT_ACCESSIBLE.format(directory))
            return []

        return file_list

    def _unfold_params(self):
        # remove allowed files that are not accessible
        # we do this every time because accessibility of files might change from one collect invocation to another
        self._files = []
        for a_file in self._prelim_files:
            if os.access(a_file, os.R_OK):
                self._files.append(a_file)
            else:
                self.log_printer.warn(StringConstants.OBJ_NOT_ACCESSIBLE.format(a_file))

        # this doesnt change, do this only once
        if not self.unfolded:
            # remove directories that are ignored
            flat_dirs = self._prelim_flat_dirs
            rec_dirs = self._prelim_rec_dirs

            for ignored_dir in self._ignored_dirs:
                for f_dir in flat_dirs:
                    if ignored_dir in f_dir:
                        flat_dirs.remove(f_dir)
                for r_dir in rec_dirs:
                    if ignored_dir in r_dir:
                        rec_dirs.remove(r_dir)

            self._flat_dirs = flat_dirs
            self._rec_dirs = rec_dirs

            self.unfolded = True

    def collect(self):
        """
        :return: list of absolute file paths to all collected files
        """
        self._unfold_params()

        all_dirs = self._flat_dirs
        for rec_dir in self._rec_dirs:
            all_dirs.extend(self._nonignored_dir_tree(rec_dir))

        files = self._files
        for a_dir in all_dirs:
            files.extend(self._get_files_from_dir(a_dir))

        self._items = files

        return files
