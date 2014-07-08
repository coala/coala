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
import os
from codeclib.internal.parsing.Parser import Parser
from codeclib.fillib.settings.Settings import Settings
from codeclib.fillib.misc.i18n import _


class CLIParser(Parser):
    @staticmethod
    def parse_args(custom_arg_list=None):
                        # arg_parser reads given arguments and presents help on wrong input
        arg_parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=__doc__)

        # -d sets parameter "TargetDirectories" => List of paths to files and/or directories to be (recursively) checked
        arg_parser.add_argument('-d', '--dirs', nargs='+', metavar='DIR', dest='TargetDirectories',
                                help=_('List of paths to files and/or directories to be (recursively) checked'))
        # -id sets parameter "IgnoredDirectories" => List of paths to files and/or directories to be ignored
        arg_parser.add_argument('-id', '--ignored-dirs', nargs='+', metavar='DIR', dest='IgnoredDirectories',
                                help=_('List of paths to files and/or directories to be ignored'))
        # -fd sets parameter "FlatDirectories" => List of paths to directories to be checked excluding sub-directories
        arg_parser.add_argument('-fd', '--flat-dirs', nargs='+', metavar='DIR', dest='FlatDirectories',
                                help=_('List of paths to directories to be checked excluding sub-directories'))
        # -t sets parameter "TargetFileTypes" => List of file endings of files to be checked
        arg_parser.add_argument('-t', '--types', nargs='+', metavar='TYPE', dest='TargetFileTypes',
                                help=_('List of file endings of files to be checked'))
        # -it sets parameter "IgnoredFileTypes" => List of file endings of files to be ignored
        arg_parser.add_argument('-it', '--ignored-types', nargs='+', metavar='TYPE', dest='IgnoredFileTypes',
                                help=_('List of file endings of files to be ignored'))
        # -i sets parameter IncludedFilterDirectories => additional filter sources
        arg_parser.add_argument('-i', '--include-filter-dirs', nargs='+', metavar='DIR',
                                dest='IncludedFilterDirectories', help=_('List of directories that contain filters'))
        # -f sets parameter "Filters" => Names of filters that should be used
        arg_parser.add_argument('-f', '--filters', nargs='+', metavar='FILE', dest='Filters',
                                help=_('Names of filters that should be used'))
        # -if sets parameter "IgnoredFilters" => Names of filters that should be ignored
        arg_parser.add_argument('-if', '--ignored-filters', nargs='+', metavar='FILE', dest='IgnoredFilters',
                                help=_('Names of filters that should be ignored'))
        # -rf sets parameter "RegexFilters" => List of regular expressions for matching filters to be used
        arg_parser.add_argument('-rf', '--regex-filters', nargs='+', metavar='REGEX', dest='RegexFilters',
                                help=_('List of regular expressions for matching filters to be used'))
        # -l sets parameter "LogType" => Enum (CONSOLE/TXT/HTML) to choose type of logging
        arg_parser.add_argument('-l', '--log', nargs=1, choices=['CONSOLE', 'TXT', 'HTML'], metavar='LEVEL',
                                dest='LogType', help=_('Enum (CONSOLE/TXT/HTML) to choose type of logging'))
        # -o sets parameter "LogOutput" => File path to where logging output should be saved
        arg_parser.add_argument('-o', '--output', nargs=1, metavar='FILE', dest='LogOutput',
                                help=_('File path to where logging output should be saved'))
        # -v sets parameter "Verbosity" => Enum (ERR/WARN/INFO/DEBUG) to choose level of verbosity
        arg_parser.add_argument('-v', '--verbose', nargs=1, choices=['ERR', 'WARN', 'INFO', 'DEBUG'], metavar='LEVEL',
                                dest='Verbosity', help=_('Enum (ERR/WARN/INFO/DEBUG) to choose level of verbosity'))
        # -c sets parameter "ConfigFile" => File path of configuration file to be used
        arg_parser.add_argument('-c', '--config', nargs=1, metavar='FILE', dest='ConfigFile',
                                help=_('File path of configuration file to be used'))
        # -s sets parameter "Save" => Filename of file to be saved to, defaults to config file
        arg_parser.add_argument('-s', '--save', nargs='?', const=True, metavar='FILE', dest='Save',
                                help=_('Filename of file to be saved to, defaults to config file'))
        # -j sets parameter "JobCount" => Number of processes to be allowed to run at once
        arg_parser.add_argument('-j', '--jobs', nargs=1, type=int, metavar='INT', dest='JobCount',
                                help=_('Number of processes to be allowed to run at once'))
        # -a sets parameter "ApplyChanges" => Set once to ask for or twice to apply changes
        arg_parser.add_argument('-a', '--apply-changes', nargs=1, choices=['YES', 'NO', 'ASK'], metavar='ENUM',
                                dest='ApplyChanges', help=_("Enum('YES','NO','ASK') to set whether to apply changes"))
        # -hf sets parameter "HideFineFiles" => Set to not show files that are ok
        arg_parser.add_argument('-hf', '--hide-fine-files', nargs=1, metavar='BOOL', dest='HideFineFiles',
                                help=_('Set to hide Files from results that do not produce filter output'))

        # arg_vars stores parsed arguments in form of a dictionary.
        # it reads custom_arg_string instead of sys.args if custom_arg_string is given.
        if custom_arg_list:
            arg_vars = vars(arg_parser.parse_args(custom_arg_list))
        else:
            arg_vars = vars(arg_parser.parse_args())

        #make arguments to list or None as all other parameters are:
        if arg_vars['Save']:
            arg_vars['Save'] = [arg_vars['Save']]

        return arg_vars

    @staticmethod
    def make_value_string(value_list):
        if value_list is None:
            return None
        value_string = ""
        for value in value_list:
            value_string += str(value) + ','
        value_string = value_string[:-1]
        return value_string

    def __init__(self):
        super().__init__()
        self.parsed_settings = Settings("CLIArgs")

    def parse(self, custom_arg_list=None):
        """
        :param custom_arg_list: the filename of the config file to read
        """
        arg_dict = CLIParser.parse_args(custom_arg_list)
        for key, value in arg_dict.items():
            value_string = CLIParser.make_value_string(value)
            if value_string:
                self.parsed_settings.append(key, value_string, os.getcwd())
        return ""

    def reparse(self, custom_arg_list=None):
        """
        :param custom_arg_list: the filename of the config file to read
        """
        self.parsed_settings = Settings("CLIArgs")
        return self.parse(custom_arg_list)

    def export_to_settings(self):
        """
        :return a list of Settings objects representing the current parsed things
        """
        return {"default": self.parsed_settings}

