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
import re
from coalib.misc.StringConstants import StringConstants


class StringConverter:
    """
    Converts strings to other things as needed. If you need a conversion for string that is not implemented here
    consider adding it so everyone gets something out of it.

    Planned conversions to add: (TODOs)
    - __path__() creates an absolute path for a string
    """
    def __init__(self, value, strip_whitespaces=True, list_delimiters=[",", ";"]):
        if not isinstance(list_delimiters, list) and not isinstance(list_delimiters, str):
            raise TypeError
        if not isinstance(strip_whitespaces, bool):
            raise TypeError

        self.__strip_whitespaces = strip_whitespaces
        self.__set_value_delims(list_delimiters)

        self.__prepare_string(value)

    def __set_value_delims(self, val):
        self.__list_delimiters = val
        if len(self.__list_delimiters) == 0:
            self.__delim_regex = ""
            return

        self.__delim_regex = "("
        for i in range(len(val) - 1):
            self.__delim_regex += re.escape(str(val[i])) + "|"
        self.__delim_regex += re.escape(str(val[-1])) + ")"

    def __str__(self):
        return self.__value

    def __bool__(self):
        if self.__value.lower() in StringConstants.TRUE_STRINGS:
            return True
        if self.__value.lower() in StringConstants.FALSE_STRINGS:
            return False
        raise ValueError

    def __len__(self):
        return len(self.__value)

    def __int__(self):
        return int(self.__value)

    def __iter__(self):
        return iter(self.__list)

    def __prepare_string(self, val):
        self.__value = str(val)
        list = re.split(self.__delim_regex, self.__value)

        if self.__strip_whitespaces:
            self.__value = self.__value.strip()
            for i in range(len(list)):
                list[i] = list[i].strip()

        self.__list = []
        for elem in list:
            if not elem in self.__list_delimiters and not elem == "":
                self.__list.append(elem)
