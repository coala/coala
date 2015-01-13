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
import argparse
from collections import OrderedDict
import os
import sys

from coalib.parsing.LineParser import LineParser
from coalib.parsing.SectionParser import SectionParser
from coalib.settings.Setting import Setting
from coalib.settings.Section import Section
from coalib.parsing.DefaultArgParser import default_arg_parser


class CliParser(SectionParser):
    def __init__(self,
                 arg_parser=default_arg_parser,
                 key_value_delimiters=['=', ':'],
                 comment_seperators=[],
                 key_delimiters=[','],
                 section_override_delimiters=["."]):
        """
        CliParser parses arguments from the command line or a custom list of items that my look like this:
        ['-a', '-b', 'b1', 'b2', 'setting=value', 'section.setting=other_value', 'key1,section.key2=value2']
        :param arg_parser: Instance of ArgParser() that is used to parse none-setting arguments
        :param key_value_delimiters: delimiters to separate key and value in setting arguments
        :param comment_seperators: allowed prefixes for comments
        :param key_delimiters: delimiter to separate multiple keys of a setting argument
        :param section_override_delimiters: The delimiter to delimit the section from the key name
        (e.g. the '.' in section.key = value)
        """
        if not isinstance(arg_parser, argparse.ArgumentParser):
            raise TypeError("arg_parser must be an ArgumentParser")

        SectionParser.__init__(self)

        self._arg_parser = arg_parser
        self._line_parser = LineParser(key_value_delimiters,
                                       comment_seperators,
                                       key_delimiters,
                                       {},
                                       section_override_delimiters)

        self.__reset_sections()

    def __reset_sections(self):
        self.sections = OrderedDict(default=Section('default'))

    def _update_sections(self, section_name, key, value, origin):
        if key == '' or value is None:
            return

        if section_name == "" or section_name is None:
            section_name = "default"

        if not section_name in self.sections:
            self.sections[section_name] = Section(section_name)

        self.sections[section_name].append(Setting(key, str(value), origin))

    def parse(self, arg_list=sys.argv[1:], origin=os.getcwd()):
        """
        parses the input and adds the new data to the existing
        :param arg_list: list of arguments.
        :param origin: directory used to interpret relative paths given as argument
        :return: the settings dictionary
        """
        origin += os.path.sep
        arg_parse_list = []
        for arg in arg_list:
            section_stub, key_touples, value, comment_stub = self._line_parser.parse(arg)

            if key_touples:  # this argument is to be parsed by line_parser
                for key_touple in key_touples:
                    self._update_sections(section_name=key_touple[0], key=key_touple[1], value=value, origin=origin)
            else:  # this argument is to be parsed by arg_parser
                arg_parse_list.append(arg)

        arg_parse_dict = vars(self._arg_parser.parse_args(arg_parse_list))

        for arg_key, arg_value in arg_parse_dict.items():
            if isinstance(arg_value, list):
                arg_value = ",".join([str(val) for val in arg_value])  # [1,2,3] -> "1,2,3"
            self._update_sections("default", arg_key, arg_value, origin)

        return self.sections

    def reparse(self, arg_list=sys.argv[1:], origin=os.getcwd()):
        self.__reset_sections()

        return self.parse(arg_list, origin)

    def export_to_settings(self):
        return self.sections
