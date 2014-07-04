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
from configparser import ConfigParser
from codeclib.fillib.settings.Settings import Settings
from codeclib.internal.parsing.Parser import Parser


class ConfParser(Parser):
    def __init__(self):
        self.parsed = False

    def parse(self, input_data):
        """
        :param input_data: the filename of the config file to read
        """
        raise NotImplementedError
        self.parsed = True

    def reparse(self, input_data):
        """
        :param input_data: the filename of the config file to read
        """
        raise NotImplementedError
        self.parsed = True

    def export_to_settings(self):
        assert self.parsed
        raise NotImplementedError

    def __parse_settings