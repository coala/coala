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
import os
import re
import sys

from coalib.parsing.LineParser import LineParser
from coalib.parsing.Parser import Parser
from coalib.settings.Setting import Setting
from coalib.settings.Settings import Settings
from coalib.parsing import DefaultArgParser
from coalib.misc.i18n import _


class CliParser(Parser):
    @staticmethod
    def first_unescaped_position(char, char_string, escape_sequence='\\'):
        first_unescaped = -2
        escaped_chars = [-1]
        while first_unescaped < -1:
            start = max(escaped_chars) + 1
            char_position = char_string[start:].find(char)
            if not char_position == -1:
                char_position += start  # -1 or real position
            if char_position - len(escape_sequence) >= 0 and \
               char_string[char_position - len(escape_sequence):].find(escape_sequence) == 0:  # escaped
                escaped_chars.append(char_position)
            else:
                first_unescaped = char_position
        return first_unescaped

    def __init__(self,
                 arg_parser=DefaultArgParser.default_arg_parser,
                 key_value_delimiters=['=', ':'],
                 section_key_delimiters=['.']):
        """
        CliParser parses arguments from the command line or a custom list of items that my look like this:
        ['-a', '-b', 'b1', 'b2', 'setting=value', 'section.setting=other_value', 'key1,section.key2=value2']
        :param arg_parser: Instance of ArgParser() that is used to parse none-setting arguments
        :param key_value_delimiters: delimiter to separate key and value in setting arguments
        :param key_delimiters: delimiter to separate multiple keys of a setting argument
        """
        Parser.__init__(self)

        self.key_value_delimiters = key_value_delimiters
        self.section_key_delimiters = section_key_delimiters
        self._arg_parser = arg_parser
        self._line_parser = LineParser(key_value_delimiters=self.key_value_delimiters,
                                       section_name_surroundings={},
                                       section_override_delimiters=self.section_key_delimiters)

        self.__reset_sections()

    def __reset_sections(self):
        self.sections = OrderedDict(default=Settings('default'))

    def parse(self, arg_list=sys.argv, origin=os.getcwd()):
        """
        parses the input and adds the new data to the existing
        :param arg_list: list of arguments.
        :param origin: directory used to interpret relative paths given as argument
        :return: the settings dictionary
        """
        set_list = []
        for arg in reversed(arg_list):
            for kv_delim in self.key_value_delimiters:
                if self.first_unescaped_position(kv_delim, arg) > 0:
                    arg_list.remove(arg)  # arg_list contains things like ['-c', c_arg1, c_arg2, '-d']
                    set_list.append(arg)  # setting_list contains things like ['section.key=value']

        self._parse_args(arg_list, origin)
        self._parse_sets(set_list, origin)

        return self.sections
        #for section_name, section in self.sections.items():
        #    print('\033[1;31m'+section.name+'\033[0m')
        #    for key, value in section.contents.items():
        #        print(key, ':', value)



    def _parse_args(self, arg_list, origin):
        arg_dict = vars(self._arg_parser.parse_args(arg_list))
        for arg_key, arg_value in arg_dict.items():
            if isinstance(arg_value, list):
                arg_value = ",".join([str(val) for val in arg_value])  # [1,2,3] -> "1,2,3"
            else:
                arg_value = str(arg_value)
            self.sections['default'].append(Setting(arg_key, arg_value, origin))

    def _parse_sets(self, set_list, origin):
        for setting_string in set_list:

            invalid_section, key_touples, value, comment = self._line_parser.parse(setting_string)
            for section_override, key in key_touples:
                if section_override != "":
                    section_name = section_override
                else:
                    section_name = "default"

                if not section_name in self.sections:
                    self.sections[section_name] = Settings(section_name)
                self.sections[section_name].append(Setting(key, value, origin))


    def reparse(self, arg_list=sys.argv, origin=os.getcwd()):
        self.__reset_sections()
        return self.parse(arg_list, origin)

    def export_to_settings(self):
        return self.sections
