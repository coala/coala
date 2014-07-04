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
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from collections import OrderedDict
from codeclib.fillib.settings.Setting import Setting


class Settings:
    def __init__(self, name):
        self.name = name
        self.contents = OrderedDict()

    def import_section(self, config_parser, origin, section_name=None):
        if section_name is not None:
            self.name = section_name

        section = config_parser[self.name]
        for key in section:
            self.contents[key] = Setting(key, section[key], origin)
