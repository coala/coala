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

import os
import inspect
import pkgutil
import argparse
import collections
import logging


class Settings(collections.OrderedDict):
    def __init__(self, custom_arg_list=None):
        # derived from ordered Dict for cleaner configuration files
        collections.OrderedDict.__init__(self)

        # TODO get settings:
        # 1. set defaults
        # 2. override with (earliest) conf
        # 3. override with confs up to latest
        # 4. override with cli args

    def defaultOptions(self):

        # dict of default values:
        defaultValues={'TargetDirectories': [os.getcwd()],
                       'IgnoredDirectories': None,
                       'FlatDirectories': None,
                       'TargetFileTypes': None,
                       'IgnoredFileTypes': ['.gitignore'],

                       'Filters': None,
                       'IgnoredFilters': None,
                       'RegexFilters': None,

                       'FileOkColor': 'bright red',
                       'FileBadColor': 'bright green',
                       'FilterColor': 'grey',
                       'ErrorResultColor': 'red',
                       'WarningResultColor': 'yellow',
                       'InfoResultColor': 'normal',
                       'DebugResultColor': 'cyan',

                       'LogType': 'CONSOLE',
                       'LogOutput': None,
                       'Verbosity': 'INFO',

                       'ConfigFile': '.codecfile',
                       'Save': None,
                       'JobCount': None
                       }
        return defaultValues

# WHILE THIS CAN BE TAKEN AS A STARTING POINT FOR LATER WORK, IT IS NOW OBSOLETE BECAUSE CONFIGPARSER WILL NOT BE USED!
#    def list_config_hierarchy(self, ccfile_path_list):
#        """Config files may refer to other config files which are included for values that don't differ from defaults
#        :param ccfile_path_list: list with already found config file paths
#        :returns: List of config files that refer to each other, highest priority file first
#        """
#        ccfile_path_list = ccfile_path_list
#        cfg_parser = configparser.ConfigParser()
#        cfg_parser.optionxform = str # this makes options case sensitive:
#
#        # let cfg_parser try to read last item of that list
#        # cfg_parser returns [] if it cannot read that file for any reason
#        if cfg_parser.read(ccfile_path_list[len(ccfile_path_list)]):
#            try:
#                # this will raise KeyError if either key or sub-key is not in the config:
#                next_config_path = cfg_parser['CODEC-SETTINGS']['ConfigLocation']
#
#                # the value can only be added to the list if it isn't None or already contained in the list:
#                if next_config_path and (next_config_path not in ccfile_path_list):
#                    ccfile_path_list.append(next_config_path)
#                    # recursive call looks for even further delegation of configs
#                    return self.list_config_hierarchy(ccfile_path_list)
#                else:
#                    # return list as is because 'ConfigLocation' had no value or to prevent infinite loop:
#                    return ccfile_path_list
#
#            except KeyError:
#                # another 'ConfigLocation' is not specified in this config, therefore the list can be returned as is
#                return ccfile_path_list
#        else:
#            # cfg_parser could not read this file, therefore the list must be returned without this item
#            return ccfile_path_list[:-1]


    def parse_conf(self, ccfile_path_list):

        pass

    def parse_args(self, custom_arg_list = None):
        """
        Parses command line arguments and configures help output.

        :param custom_arg_list: parse_args will parse this list instead of command line arguments, if specified
        :returns: parsed arguments in dictionary structure
        """
        # arg_parser reads given arguments and presents help on wrong input
        arg_parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=__doc__)

        # -d sets parameter "TargetDirectories" => List of paths to files and/or directories to be (recursively) checked
        arg_parser.add_argument('-d', '--dirs', nargs='+', metavar='DIR', dest='TargetDirectories',
                                help='List of paths to files and/or directories to be (recursively) checked')
        # -id sets parameter "IgnoredDirectories" => List of paths to files and/or directories to be ignored
        arg_parser.add_argument('-id', '--ignored-dirs', nargs='+', metavar='DIR', dest='IgnoredDirectories',
                                help='List of paths to files and/or directories to be ignored')
        # -fd sets parameter "FlatDirectories" => List of paths to directories to be checked excluding sub-directories
        arg_parser.add_argument('-fd', '--flat-dirs', nargs='+', metavar='DIR', dest='FlatDirectories',
                                help='List of paths to directories to be checked excluding sub-directories')
        # -t sets parameter "TargetFileTypes" => List of file endings of files to be checked
        arg_parser.add_argument('-t', '--types', nargs='+', metavar='TYPE', dest='TargetFileTypes',
                                help='List of file endings of files to be checked')
        # -it sets parameter "IgnoredFileTypes" => List of file endings of files to be ignored
        arg_parser.add_argument('-it', '--ignored-types', nargs='+', metavar='TYPE', dest='IgnoredFileTypes',
                                help='List of file endings of files to be ignored')
        # -f sets parameter "Filters" => Names of filters that should be used
        arg_parser.add_argument('-f', '--filters', nargs='+', metavar='FILE', dest='Filters',
                                help='Names of filters that should be used')
        # -if sets parameter "IgnoredFilters" => Names of filters that should be ignored
        arg_parser.add_argument('-if', '--ignored-filters', nargs='+', metavar='FILE', dest='IgnoredFilters',
                                help='Names of filters that should be ignored')
        # -rf sets parameter "RegexFilters" => List of regular expressions for matching filters to be used
        arg_parser.add_argument('-rf', '--regex-filters', nargs='+', metavar='REGEX', dest='RegexFilters',
                                help='List of regular expressions for matching filters to be used')
        # -l sets parameter "LogType" => Enum (CONSOLE/TXT/HTML) to choose type of logging
        arg_parser.add_argument('-l', '--log', nargs=1, choices=['CONSOLE', 'TXT', 'HTML'], metavar='LEVEL',
                                dest='LogType', help='Enum (CONSOLE/TXT/HTML) to choose type of logging')
        # -o sets parameter "LogOutput" => File path to where logging output should be saved
        arg_parser.add_argument('-o', '--output', nargs=1, metavar='FILE', dest='LogOutput',
                                help='File path to where logging output should be saved')
        # -v sets parameter "Verbosity" => Enum (ERR/WARN/INFO/DEBUG) to choose level of verbosity
        arg_parser.add_argument('-v', '--verbose', nargs=1, choices=['ERR', 'WARN', 'INFO', 'DEBUG'], metavar='LEVEL',
                                dest='Verbosity', help='Enum (ERR/WARN/INFO/DEBUG) to choose level of verbosity')
        # -c sets parameter "ConfigFile" => File path of configuration file to be used
        arg_parser.add_argument('-c', '--config', nargs='?', const=True, metavar='FILE', dest='ConfigFile',
                                help='File path of configuration file to be used')
        # -s sets parameter "Save" => Filename of file to be saved to, defaults to config file
        arg_parser.add_argument('-s', '--save', nargs='?', const=True, metavar='FILE', dest='Save',
                                help='Filename of file to be saved to, defaults to config file')
        # -j sets parameter "JobCount" => Number of processes to be allowed to run at once
        arg_parser.add_argument('-j', '--jobs', nargs=1, type=int, metavar='INT', dest='JobCount',
                                help='Number of processes to be allowed to run at once')

        # arg_vars stores parsed arguments in form of a dictionary.
        # it reads custom_arg_string instead of sys.args if custom_arg_string is given.
        if custom_arg_list:
            arg_vars = vars(arg_parser.parse_args(custom_arg_list))
        else:
            arg_vars = vars(arg_parser.parse_args())


        return arg_vars

    def save_conf(self, ccfile_path):
        pass


if __name__=="__main__":
    settings=Settings()