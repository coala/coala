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
from coalib.misc.StringConstants import StringConstants


class StringConverter:
    """
    Converts strings to other things as needed. If you need a conversion for string that is not implemented here
    consider adding it so everyone gets something out of it.

    Planned conversions to add: (TODOs)
    - __path__() creates an absolute path for a string
    """
    def __init__(self, value, strip_whitespaces=True):
        self.__value = value
        self.strip_whitespaces = strip_whitespaces

        self.__prepare_string()

    def __str__(self):
        return self.__value

    def __bool__(self):
        if self.__value.lower() in StringConstants.TRUE_STRINGS:
            return True
        if self.__value.lower() in StringConstants.FALSE_STRINGS:
            return False
        raise AttributeError

    def __len__(self):
        return len(self.__value)

    def __int__(self):
        return int(self.__value)

    def __prepare_string(self):
        if self.strip_whitespaces:
            self.__value = self.__value.strip()
