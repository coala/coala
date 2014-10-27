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
    """
    def __init__(self, value, strip_whitespaces=True, list_delimiters=[",", ";"]):
        if not isinstance(list_delimiters, list) and not isinstance(list_delimiters, str):
            raise TypeError("list_delimiters has to be a string or a list")
        if not isinstance(strip_whitespaces, bool):
            raise TypeError("strip_whitespaces has to be a bool parameter")

        self.__strip_whitespaces = strip_whitespaces
        self.__set_value_delims(list_delimiters)

        self.value = value
        self.__list = None
        self.__recreate_list = True

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
        return self.value

    def __bool__(self):
        if self.value.lower() in StringConstants.TRUE_STRINGS:
            return True
        if self.value.lower() in StringConstants.FALSE_STRINGS:
            return False
        raise ValueError

    def __len__(self):
        return len(self.value)

    def __int__(self):
        return int(self.value)

    def __iter__(self):
        self.__prepare_list()

        return iter(self.__list)

    def __prepare_list(self):
        if not self.__recreate_list:
            return

        list = re.split(self.__delim_regex, self.value)

        if self.__strip_whitespaces:
            for i in range(len(list)):
                list[i] = list[i].strip()

        self.__list = []
        for elem in list:
            if not elem in self.__list_delimiters and not elem == "":
                self.__list.append(elem)

        self.__recreate_list = False

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newval):
        self.__value = str(newval)
        if self.__strip_whitespaces:
            self.__value = self.__value.strip()

        self.__recreate_list = True

    def __eq__(self, other):
        return isinstance(other, StringConverter) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)
