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
from collections import OrderedDict

from coalib.settings.Setting import Setting


class Settings:
    """
    This class holds a set of settings.
    """

    @staticmethod
    def __prepare_key(key):
        return str(key).lower().strip()

    def __init__(self, name, defaults=None):
        if defaults is not None and not isinstance(defaults, Settings):
            raise TypeError("defaults has to be a Settings object or None.")
        if defaults is self:
            raise ValueError("defaults may not be self for non-recursivity.")

        self.name = str(name)
        self.defaults = defaults
        self.contents = OrderedDict()

    def append(self, setting, custom_key=None):
        if not isinstance(setting, Setting):
            raise TypeError
        if custom_key is None:
            key = self.__prepare_key(setting.key)
        else:
            key = self.__prepare_key(custom_key)

        # Setting asserts key != "" for us
        self.contents[key] = setting

    def _add_or_create_setting(self, setting, custom_key=None, allow_appending=True):
        if custom_key is None:
            key = setting.key
        else:
            key = custom_key

        if self.__contains__(key, ignore_defaults=True) and allow_appending:
            val = self[key]
            val.value = str(val.value) + "\n" + setting.value
        else:
            self.append(setting, custom_key=key)

    def __iter__(self, ignore_defaults=False):
        joined = self.contents.copy()
        if self.defaults is not None and not ignore_defaults:
            joined.update(self.defaults.contents)
        return iter(joined)

    def __contains__(self, item, ignore_defaults=False):
        try:
            self.__getitem__(item, ignore_defaults)
            return True
        except IndexError:
            return False

    def __getitem__(self, item, ignore_defaults=False):
        key = self.__prepare_key(item)
        if key == "":
            raise IndexError("Empty keys are invalid.")

        res = self.contents.get(key, None)
        if res is not None:
            return res

        if self.defaults is None or ignore_defaults:
            raise IndexError("Required index is unavailable.")

        return self.defaults[key]

    def __str__(self):
        return self.name + " {" + ", ".join(key + " : " + str(self.contents[key]) for key in self.contents) + "}"

    def get(self, key, default="", ignore_defaults=False):
        """
        Retrieves the item without raising an exception. If the item is not available an appropriate Setting will be
        generated from your provided default value.

        :param key: The key of the setting to return.
        :param default: The default value
        :param ignore_defaults: Whether or not to ignore the default settings.
        :return: The setting.
        """
        try:
            return self.__getitem__(key, ignore_defaults)
        except IndexError:
            return Setting(key, str(default))
