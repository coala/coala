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
from coalib.misc.i18n import _


class Settings:
    @staticmethod
    def __prepare_key(key):
        return str(key).lower().strip()
    """
    This class holds a set of settings.
    """
    def __init__(self, name, defaults=None):
        if defaults is not None and not isinstance(defaults, Settings):
            raise TypeError(_("defaults has to be a Settings object or None."))
        if defaults is self:
            raise ValueError(_("defaults may not be self for non-recursivity."))

        self.name = str(name)
        self.defaults = defaults
        self.contents = OrderedDict()

    def append(self, setting):
        if not isinstance(setting, Setting):
            raise TypeError

        # Setting asserts key != "" for us
        self.contents[self.__prepare_key(setting.key)] = setting

    def __iter__(self):
        joined = self.contents.copy()
        joined.update(self.defaults.contents)
        return iter(joined)

    def __getitem__(self, item):
        key = self.__prepare_key(item)
        if key == "":
            raise IndexError(_("Empty keys are invalid."))

        res = self.contents.get(key, None)
        if res is not None:
            return res

        if self.defaults is None:
            raise IndexError(_("Required index is unavailable."))

        return self.defaults[key]
