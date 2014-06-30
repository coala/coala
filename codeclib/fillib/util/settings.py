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
import shutil
from codeclib.fillib.util.setting import Setting

import os
import argparse


class Settings(OrderedDict):
    @staticmethod
    def __make_value(original):
        stripped = original.strip()

        lst = stripped.split(',')
        if len(lst) > 1:
            new_list = []
            for elem in lst:
                new_list.append(Settings.__make_value(elem)[0])
            return new_list

        return [stripped]

    def __init__(self, auto_load=True):
        OrderedDict.__init__(self)

        self.defaults = OrderedDict()

        self.__get_default_settings()
        cmdargs = Settings.__parse_cmdline_args()

        if cmdargs.get('ConfigFile', None) != None and os.path.isfile(cmdargs.get('ConfigFile', [None])[0]):
            self.origin_file = cmdargs.get('ConfigFile', None)
        else:
            self.origin_file = self.defaults['configfile'].value[0]

        self.__import_file(self.origin_file)
        self.__import_dict(cmdargs)

    def save_if_necessary(self):
        paths = self.get('save', Setting('', '')).value
        for path in paths:
            if path is not None and not 'None':
                if path == True:
                    self.save_to_file(self.origin_file)
                else:
                    self.save_to_file(path)

    def __import_dict(self, dictionary):
        for key, value in dictionary.items():
            if value is not None:
                self.__import_setting(key, Setting(key, value, ['cmdline']))

    def __capitalize_key(self, key):
        if key.lower() in self.defaults:
            return self.defaults.get(key.lower()).key

        return key

    def __import_file(self, path, import_history=None):
        if import_history is None:
            import_history = []
        # prevent loops
        if path in import_history:
            # TODO log warning about circular dependency
            return
        import_history.append(path)

        if not os.path.isfile(path):
            # TODO log warning notafile
            return

        comments = []
        with open(path, 'r') as lines:
            for line in lines:
                comments = self.__parse_line(line, comments, import_history)

        if  comments != []:
            # add empty comment-only object
            self.__import_setting('comment', Setting('', '', import_history, comments))

    def save_to_file(self, path):
        if os.path.isfile(path):
            # create backup file
            shutil.copy2(path, path+'~')
        with open(path, 'w') as config_file:
            for setting in self.values():
                imp = self.__setting_is_implicit(setting)
                if imp == True:
                    continue

                lines = imp.generate_lines()
                for line in lines:
                    config_file.write(line+'\n')

    def ensure_settings_available(self, keys_dict_dict_list):
        # keys_dict_dict_list is a list, entries are {filter_name:{setting:help_text}}
        for key_dict_dict in keys_dict_dict_list:
            # since we save Setting objects, get() does not return None if it's set to None!

            for filter_name, key_dict in key_dict_dict.items():
                if key_dict:
                    for setting, help_text in key_dict.items():
                        if self.get(setting.lower()) is None:
                            print("Please enter the value of the setting '{}' (needed by {})".format(setting, filter_name))
                            user_input = input("{}: ".format(help_text))
                            self.__parse_line(setting + "=" + user_input, '', ['cmdline'])

#            if self.get(key_dict_dict[].lower(), None) is None:
#                print("Please enter the value for the setting {}.".format(key))
#                user_input = input("Value: ")
#                self.__parse_line(key + "=" + user_input, ['cmdline'])

    def __setting_is_implicit(self, setting):
        # write setting only if its import_history is [origin_file] AND
        # a) it is non-default
        # b) it is default and overrides a non-default setting with len(import_history) > 1 which does not
        #    get overwritten by a default setting with len(import_history) > 1
        # Since every command is non-default they don't need extra handling.
        if setting.import_history != [self.origin_file] and setting.import_history != ['cmdline']:
            return True

        if setting.import_history == ['cmdline'] and setting.key.lower() == 'save':
            if setting.overrides is None:
                return True
            else:
                return self.__setting_is_implicit(setting.overrides)

        if setting.key.lower() == "save" and setting.value == [False]:
            return True

        if setting.value != self.defaults.get(setting.key.lower(), Setting('', '')).value:
            return setting

        # it is a default value now

        if self.__overrides_non_default(setting):
            return setting
        return True

    def __overrides_non_default(self, setting):
        if setting.overrides == None:
            return False

        if setting.overrides.import_history == [self.origin_file]:
            return self.__overrides_non_default(setting.overrides)

        return setting.overrides.value != self.defaults[setting.key.lower()].value

    def __parse_line(self, line, comments, import_history=None):
        if import_history is None:
            import_history = []

        line = line.strip()
        if not line:
            comments.append('')
            return comments

        trailing_comment = ''
        if line.find('#') >= 0:
            trailing_comment = line[line.find('#')+1:].strip()

        # handle comments - TODO allow \# as non-comment
        line = line.split('#')[0].strip()
        # TODO allow \=!
        parts = line.split('=')
        if (len(parts) == 1):
            comments.append(trailing_comment)
            return comments

        if (len(parts) != 2):
            # TODO log a warning
            comments.append(trailing_comment)
            return comments

        key = parts[0].strip()
        val = Setting(self.__capitalize_key(key),
                      Settings.__make_value(parts[1]),
                      import_history,
                      comments,
                      trailing_comment,
                      self.get(key.lower(), None)
        )
        
        self.__import_setting(key, val)

        return []
    
    def __import_setting(self, key, val):

        # commands may be there more than one time, use some other virtual keys
        if self.__execute_command(val) or key.lower().strip() == 'comment':
            while key.lower() in self:
                key += ' '

        if val.overrides is None:
            val.overrides = self.get(key.lower(), None)

        # make sure the new value is at the end
        if key.lower() in self:
            del self[key.lower()]

        self[key.lower()] = val

    def __import_command(self, command):
        if command.value == None:
            return True
        for config_path in command.value:
            self.__import_file(config_path, command.import_history)
        return True

    def __execute_command(self, command):
        if command.key.lower() == 'import':
            return self.__import_command(command)

        return False

    def get_bool_setting(self, name, default=None):
        res = self.get(name.lower(), None)
        if res is None:
            return default
        return res.to_bool()[0]


    def get_int_setting(self, name, default=None):
        res = self.get(name.lower(), None)
        if res is None:
            return default
        return res.to_int()[0]


    def get_color_setting(self, name, default=None):
        res = self.get(name.lower(), None)
        if res is None:
            return default
        return res.to_color_code()[0]

    def get_string_setting(self, name, default=None):
        res = self.get(name.lower(), None)
        if res is None:
            return default
        return str(res[0])

    def __get_default_settings(self):
        # default settings
        defaultValues = OrderedDict([
            ('TargetDirectories', os.getcwd()),
            ('IgnoredDirectories', ".git"),
            ('FlatDirectories', "None"),
            ('TargetFileTypes', "None"),
            ('IgnoredFileTypes', '.gitignore,~'),

            ('IncludedFilterDirectories', 'None'),
            ('Filters', "None"),
            ('IgnoredFilters', "None"),
            ('RegexFilters', "None"),

            ('FileOkColor', 'bright green'),
            ('FileBadColor', 'bright red'),
            ('FilterColor', 'dark gray'),
            ('ErrorResultColor', 'red'),
            ('WarningResultColor', 'yellow'),
            ('InfoResultColor', 'normal'),
            ('DebugResultColor', 'cyan'),
            ('NormalColor', 'normal'),
            ('NonPrintableCharsColor', 'dark gray'),

            ('TabWidth', '4'),

            ('LogType', 'CONSOLE'),
            ('LogOutput', 'None'),
            ('Verbosity', 'INFO'),
            ('HideFineFiles', "False"),
            ('ConfigFile', '.codecfile'),
            ('Save', 'None'),
            ('ApplyChanges', 'ASK'),
            ('JobCount', 'None')
        ])
        for key, value in defaultValues.items():
            self.defaults[key.lower()] = Setting(key, Settings.__make_value(value), ['default'])
            self.__import_setting(key, Setting(key, Settings.__make_value(value), ['default']))

    @staticmethod
    def __parse_cmdline_args(custom_arg_list=None):
        """
        Parses command line arguments and configures help output.

        :param custom_arg_list: parse_args will parse this list instead of command line arguments, if specified
        :returns: a dictionary with the cmdline values
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
        # -i sets parameter IncludedFilterDirectories => additional filter sources
        arg_parser.add_argument('-i', '--include-filter-dirs', nargs='+', metavar='DIR', dest='IncludedFilterDirectories',
                                help='List of directories that contain filters')
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
        arg_parser.add_argument('-c', '--config', nargs=1, metavar='FILE', dest='ConfigFile',
                                help='File path of configuration file to be used')
        # -s sets parameter "Save" => Filename of file to be saved to, defaults to config file
        arg_parser.add_argument('-s', '--save', nargs='?', const=True, metavar='FILE', dest='Save',
                                help='Filename of file to be saved to, defaults to config file')
        # -j sets parameter "JobCount" => Number of processes to be allowed to run at once
        arg_parser.add_argument('-j', '--jobs', nargs=1, type=int, metavar='INT', dest='JobCount',
                                help='Number of processes to be allowed to run at once')
        # -a sets parameter "ApplyChanges" => Set once to ask for or twice to apply changes
        arg_parser.add_argument('-a', '--apply-changes', nargs=1, choices=['YES','NO','ASK'], metavar='ENUM',
                                dest='ApplyChanges', help="Enum('YES','NO','ASK') to set whether to apply changes")
        # -hf sets parameter "HideFineFiles" => Set to not show files that are ok
        arg_parser.add_argument('-hf', '--hide-fine-files', nargs=1, metavar='BOOL', dest='HideFineFiles',
                                help='Set to hide Files from results that do not produce filter output')

        # arg_vars stores parsed arguments in form of a dictionary.
        # it reads custom_arg_string instead of sys.args if custom_arg_string is given.
        if custom_arg_list:
            arg_vars = vars(arg_parser.parse_args(custom_arg_list))
        else:
            arg_vars = vars(arg_parser.parse_args())

        #make arguments to list or None as all other parameters are:
        if arg_vars['Save']: arg_vars['Save'] = [arg_vars['Save']]

        return arg_vars
if __name__ == "__main__":
    settings=Settings()
