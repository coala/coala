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

from coalib.misc.StringConverter import StringConverter


def path(obj, *args, **kwargs):
    return obj.__path__(*args, **kwargs)

def path_list(obj, *args, **kwargs):
    return obj.__path_list__(*args, **kwargs)


class Setting(StringConverter):
    def __init__(self, key, value, origin="", strip_whitespaces=True, list_delimiters=[",", ";"]):
        """
        Initializes a new Setting,

        :param key: The key of the Setting
        :param value: The value, if you apply conversions to this object these will be applied to this value.
        :param origin: The originating file. This will be used for path conversions and the last part will be stripped
        of. If you want to specify a directory as origin be sure to end it with a directory seperator.
        :param strip_whitespaces: Whether to strip whitespaces from the value or not
        :param list_delimiters: Delimiters for list conversion
        :return:
        """
        StringConverter.__init__(self, value, strip_whitespaces=strip_whitespaces, list_delimiters=list_delimiters)
        self.key = key
        self.origin = str(origin)

    def __path__(self, origin=None):
        """
        Determines the path of this setting.

        Note: You can also use this function on strings, in that case the origin argument will be taken in every case.

        :param origin: the origin file to take if no origin is specified for the given setting. If you want to provide
        a directory, make sure it ends with a directory seperator.
        :return: An absolute path.
        """
        strrep = str(self).strip()
        if os.path.isabs(strrep):
            return strrep

        if hasattr(self, "origin") and self.origin != "":
            origin = self.origin

        if origin is None:
            raise ValueError("Cannot determine path without origin.")

        return os.path.join(os.path.dirname(origin), strrep)

    def __path_list__(self):
        listrep = list(self)

        for i in range(len(listrep)):
            listrep[i] = Setting.__path__(listrep[i], self.origin)

        return listrep

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        newkey = str(key)
        if newkey == "":
            raise ValueError("An empty key is not allowed for a setting.")

        self._key = newkey
