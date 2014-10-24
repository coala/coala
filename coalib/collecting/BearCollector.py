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
from coalib.collecting.FileCollector import FileCollector
from coalib.output.ConsolePrinter import ConsolePrinter


class BearCollector(FileCollector):
    def __init__(self,
                 bear_kinds,
                 bear_dirs,
                 bear_names=None,
                 ignored_bears=None,
                 regexs=None,
                 log_printer=ConsolePrinter()):
        """
        This collector stores bear classes (not instances) in self._items
        :param bear_kinds: the KINDs of bears to be collected
        :param bear_dirs: list of strings: directories from which bears should be collected
        :param bear_names: list of strings: names of bears that should be collected. Default is all.
        :param ignored_bears: list of strings: names of bears that should not be collected. Default is none.
        :param regexs: list of strings: regexs that match bears to be collected.
        :param log_printer: LogPrinter to handle logging of debug, warning and error messages
        """
        if bear_names is None:
            bear_names = []
        if ignored_bears is None:
            ignored_bears = []
        if regexs is None:
            regexs = []

        if not isinstance(bear_kinds, list):
            raise TypeError("bear_kinds should be of type list")
        if not isinstance(bear_names, list):
            raise TypeError("bear_names should be of type list")
        if not isinstance(ignored_bears, list):
            raise TypeError("ignored should be of type list")
        if not isinstance(regexs, list):
            raise TypeError("regexs should be of type list")

        FileCollector.__init__(self,
                               flat_dirs=bear_dirs,
                               allowed_types=["py"],
                               log_printer=log_printer)

        self._bear_kinds = bear_kinds
        self._bear_names = bear_names
        self._ignored_bears = ignored_bears
        self._regexs = regexs

    def _is_target(self, file_path):
        """
        :param file_path: absolute path to a file
        :return: Bool value to determine if bears should be imported from this file

        This method assumes that the given path lies in a directory that should be collected. However it will check if
        the path is a subpath of an ignored directory.
        """
        # type disallowed
        if not os.path.splitext(file_path)[1].lower().lstrip('.') in self._allowed_types:
            return False

        bear_name = os.path.splitext(os.path.basename(file_path))[0]

        # ignored bear
        if bear_name in self._ignored_bears:
            return False

        # explicitly included
        if bear_name in self._bear_names:
            return True

        # regex included
        if any(re.match(regex, bear_name) for regex in self._regexs):
            return True  # specifically called

        # dont include if not everything is to be included
        if self._bear_names or self._regexs:
            return False  # specific bears were called but not this one

        # include everything
        return True

    def collect(self):
        """
        :return: list of classes (not instances) of all collected bears
        """

        files = FileCollector.collect(self)  # needs to be upfront since it calls _unfold_params()
        bears = []

        for f_dir in self._flat_dirs:
            if f_dir not in sys.path:
                sys.path.insert(0, f_dir)

        for file in files:
            module_name = os.path.splitext(os.path.basename(file))[0]
            module = importlib.import_module(module_name)
            for name, p_object in inspect.getmembers(module):
                if hasattr(p_object, "kind"):
                    if inspect.getfile(p_object) == file:
                        bear_kind = None
                        try:
                            bear_kind = p_object.kind()
                        except:
                            pass  # Bear base class
                        if bear_kind in self._bear_kinds:
                            bears.append(p_object)

        self._items = bears
        return bears
