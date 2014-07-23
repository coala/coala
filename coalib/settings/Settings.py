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
    def __init__(self, name, defaults=None):
        if defaults is not None and not isinstance(defaults, Settings):
            raise TypeError

        self.name = str(name)
        self.defaults = defaults
        self.contents = OrderedDict()

    def append(self, setting):
        if not isinstance(setting, Setting):
            raise TypeError

        self.contents[setting.key.lower()] = setting
