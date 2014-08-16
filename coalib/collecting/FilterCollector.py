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
import importlib
import inspect
import os
import re
import sys
from coalib.misc.i18n import _
from coalib.collecting.FileCollector import FileCollector


class FilterCollector(FileCollector):
    def __init__(self, filter_kind, log_printer, filter_dirs, filter_names=None, ignored=None, regexs=None):
        """
        This collector stores filter classes (not instances) in self._items
        :param filter_kind: the KIND of filters to be collected
        :param log_printer: LogPrinter to handle logging of debug, warning and error messages
        :param filter_dirs: list of strings: directories from which filters should be collected
        :param filter_names: list of strings: names of filters that should be collected. Default is all.
        :param ignored: list of strings: names of filters that should not be collected. Default is none.
        :param regexs: list of strings: regexs that match filters to be collected.
        """
        if filter_names is None:
            filter_names = []
        if ignored is None:
            ignored = []
        if regexs is None:
            regexs = []

        if not isinstance(filter_names, list):
            raise TypeError("filter_names should be of type list")
        if not isinstance(ignored, list):
            raise TypeError("ignored should be of type list")
        if not isinstance(regexs, list):
            raise TypeError("regexs should be of type list")

        FileCollector.__init__(self,
                               log_printer,
                               flat_dirs=filter_dirs,
                               allowed=[".py"])

        self._filter_kind = filter_kind
        self._filter_names = filter_names
        self._ignored = ignored
        self._regexs = regexs

    def _is_target(self, file_path):
        """
        :param file_path: absolute path to a file
        :return: Bool value to determine if filters should be imported from this file
        """
        if not os.path.splitext(file_path)[1] in self._allowed:
            return False

        filter_name = os.path.splitext(os.path.basename(file_path))[0]
        named = filter_name in self._filter_names
        matched = sum(1 if re.match(regex, filter_name) else 0 for regex in self._regexs) > 0

        if filter_name in self._ignored:
            return False  # ignored

        if named or matched:
            return True  # specifically called
        elif self._filter_names or self._regexs:
            return False  # specific filters were called but not this one
        else:
            return True  # default

    def collect(self):
        """
        :return: list of classes (not instances) of all collected filters
        """
        for f_dir in self._flat_dirs:
            if f_dir not in sys.path:
                sys.path.insert(0, f_dir)

        files = FileCollector.collect(self)
        filters = []

        for file in files:
            module_name = os.path.splitext(os.path.basename(file))[0]
            module = importlib.import_module(module_name)
            for name, p_object in inspect.getmembers(module):
                if hasattr(p_object, "kind"):
                    if inspect.getfile(p_object) == file:
                        filter_kind = None
                        try:
                            filter_kind = p_object.kind()
                        except:
                            pass  # Filter base class
                        if filter_kind == self._filter_kind:
                            filters.append(p_object)

        self._items = filters
        return filters
