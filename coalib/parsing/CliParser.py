import argparse
from collections import OrderedDict
import os
import sys

from coalib.parsing.LineParser import LineParser
from coalib.settings.Section import Section, append_to_sections
from coalib.parsing.DefaultArgParser import default_arg_parser


class CliParser:
    def __init__(self,
                 arg_parser=default_arg_parser,
                 key_value_delimiters=['=', ':'],
                 comment_seperators=[],
                 key_delimiters=[','],
                 section_override_delimiters=["."]):
        """
        CliParser parses arguments from the command line or a custom list of
        items that my look like this:
        ['-p', 'q', 'r', '-s', 'setting=value', 'section.setting=other_value']

        :param arg_parser:                  Instance of ArgParser() that is
                                            used to parse none-setting
                                            arguments
        :param key_value_delimiters:        delimiters to separate key and
                                            value in setting arguments
        :param comment_seperators:          allowed prefixes for comments
        :param key_delimiters:              delimiter to separate multiple keys
                                            of a setting argument
        :param section_override_delimiters: The delimiter to delimit the
                                            section from the key name
                                            (e.g. the '.' in sect.key = value)
        """
        if not isinstance(arg_parser, argparse.ArgumentParser):
            raise TypeError("arg_parser must be an ArgumentParser")

        self._arg_parser = arg_parser
        self._line_parser = LineParser(key_value_delimiters,
                                       comment_seperators,
                                       key_delimiters,
                                       {},
                                       section_override_delimiters)

        self.sections = OrderedDict(default=Section('Default'))

    def parse(self, arg_list=sys.argv[1:], origin=os.getcwd()):
        """
        parses the input and adds the new data to the existing

        :param arg_list: list of arguments.
        :param origin:   directory used to interpret relative paths given as
                         argument
        :return:         the settings dictionary
        """
        origin += os.path.sep
        for arg_key, arg_value in sorted(
                vars(self._arg_parser.parse_args(arg_list)).items()):
            if arg_key == 'settings' and arg_value is not None:
                self._parse_custom_settings(arg_value, origin)
            else:
                if isinstance(arg_value, list):
                    arg_value = ",".join([str(val) for val in arg_value])

                append_to_sections(self.sections,
                                   arg_key,
                                   arg_value,
                                   origin,
                                   from_cli=True)

        return self.sections

    def _parse_custom_settings(self, custom_settings_list, origin):
        for setting_definition in custom_settings_list:
            section_stub, key_touples, value, comment_stub =\
                self._line_parser.parse(setting_definition)
            for key_touple in key_touples:
                append_to_sections(self.sections,
                                   key=key_touple[1],
                                   value=value,
                                   origin=origin,
                                   section_name=key_touple[0],
                                   from_cli=True)
