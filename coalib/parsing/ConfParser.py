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
from coalib.parsing.Parser import Parser
from coalib.settings.Settings import Settings
from coalib.misc.i18n import _


class ConfParser(Parser):
    def __init__(self):
        # Declare it
        self.sections = None
        self.__init_sections()

    def parse(self, input_data, overwrite=False):
        """
        Parses the input and adds the new data to the existing

        :param input_data: filename
        :param overwrite: behaves like reparse if this is True
        :return a non empty string containing an error message on failure
        """
        try:
            f = open(input_data, "r", encoding='utf-8')
            lines = f.readlines()

            if overwrite:
                self.__init_sections()

            self.__parse_lines(lines)
        except FileNotFoundError:
            return _("Failed reading file. Please make sure to provide a file that is existent and "
                     "you have the permission to read it.")

    def reparse(self, input_data):
        """
        Parses the input and overwrites all existent data

        :param input_data: filename
        :return a non empty string containing an error message on failure
        """
        return self.parse(input_data, overwrite=True)

    def __parse_lines(self, lines):
        raise NotImplementedError

    def __init_sections(self):
        self.sections = OrderedDict()
        self.sections["default"] = Settings("Default")
