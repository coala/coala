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
        self.sections = OrderedDict(default=Section('Default'))

    def _update_sections(self, section_name, key, value, origin):
        if key == '' or value is None:
            return

        if section_name == "" or section_name is None:
            section_name = "default"

        if not section_name in self.sections:
            self.sections[section_name] = Section(section_name)

        self.sections[section_name].append(Setting(key, str(value), origin, from_cli=True))

    def parse(self, arg_list=sys.argv[1:], origin=os.getcwd()):
        """
        parses the input and adds the new data to the existing
        :param arg_list: list of arguments.
        :param origin: directory used to interpret relative paths given as argument
        :return: the settings dictionary
        """
        origin += os.path.sep
        for arg_key, arg_value in vars(self._arg_parser.parse_args(arg_list)).items():
            if arg_key == 'settings' and arg_value is not None:
                self._parse_custom_settings(arg_value, origin)
            else:
                if isinstance(arg_value, list):
                    arg_value = ",".join([str(val) for val in arg_value])  # [1,2,3] -> "1,2,3"

                self._update_sections("default", arg_key, arg_value, origin)

        return self.sections

    def _parse_custom_settings(self, custom_settings_list, origin):
        for setting_definition in custom_settings_list:
            section_stub, key_touples, value, comment_stub = self._line_parser.parse(setting_definition)
            for key_touple in key_touples:
                self._update_sections(section_name=key_touple[0], key=key_touple[1], value=value, origin=origin)

    def reparse(self, arg_list=sys.argv[1:], origin=os.getcwd()):
        self.__reset_sections()

        return self.parse(arg_list, origin)

    def export_to_settings(self):
        return self.sections
