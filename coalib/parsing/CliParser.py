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
import re
import sys
from collections import OrderedDict
from coalib.parsing.Parser import Parser
from coalib.parsing.LineParser import LineParser
from coalib.settings.Setting import Setting
from coalib.settings.Settings import Settings
from coalib.parsing.DefaultArgParser import default_arg_parser


class CliParser(Parser):
    def __init__(self,
                 arg_parser=default_arg_parser,
                 key_value_delimiters=['=', ':'],
                 comment_seperators=['#', '//'],
                 key_delimiters=[',', ' '],
                 section_name_surroundings={}):
        Parser.__init__(self)

        self._arg_parser = arg_parser
        self.line_parser = LineParser(key_value_delimiters,
                                      comment_seperators,
                                      key_delimiters,
                                      section_name_surroundings)

        self.sections = OrderedDict(default=Settings('default'))

    def parse(self, arg_list=None, origin=os.getcwd()):
        """
        Parses the input and adds the new data to the existing

        :param arg_list: list of args. If not passed, sys.args will be parsed
        :param origin: directory to be used for absolute path of settings
        :return a non empty string containing an error message on failure
        """
        if arg_list is None:
            arg_list = sys.argv
        line_list = []

        for arg in arg_list:
            if re.search('[^\\\\]=', arg):  # find unescaped '='
                arg_list.remove(arg)  # arg_list contains ['-c', 'val1', 'val2' '-s', 'val1'] etc.
                line_list.append(arg)  # line_list contains ['section.key=value', 'key=value'] etc.

        self._parse_args(arg_list, origin)
        self._parse_lines(line_list, origin)

    def _parse_args(self, arg_list, origin):
        arg_dict = vars(self._arg_parser.parse_args(arg_list))

        for arg_key, arg_value in arg_dict.items():
            if isinstance(arg_value, list):
                arg_value = ",".join([str(val) for val in arg_value])  # [1,2,3] => "1,2,3"
            else:
                arg_value = str(arg_value)

            self.sections['default'].append(Setting(arg_key, arg_value, origin))

    def _parse_lines(self, line_list, origin):
        for line in line_list:
            section_name = 'default'
            first_period_position = line.find('.')
            first_equals_position = line.find('=')
            if 0 < first_period_position < first_equals_position:
                section_name = line[:first_period_position]
                line = line[first_period_position+1:]

            futile_section_name, keys, value, futile_comment = self.line_parser.parse(line)

            for key in keys:
                if not section_name in self.sections:
                    self.sections[section_name] = Settings(section_name)
                self.sections[section_name].append(Setting(key, value, origin))

    def reparse(self, arg_list=None):
        """
        Deletes existent data before parsing the input

        :param arg_list: list of args. If not passed, sys.args will be parsed
        :return a non empty string containing an error message on failure
        """
        self.sections = OrderedDict(default=Settings('default'))
        return self.parse(arg_list)

    def export_to_settings(self):
        """
        :return a dict of Settings objects representing the currently parsed arguments
        """
        return self.sections

