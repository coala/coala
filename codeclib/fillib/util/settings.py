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
import argparse
import shutil


# noinspection PyUnreachableCode
class Settings(dict):
    def __init__(self, custom_arg_list=None):
        # derived from ordered Dict for cleaner configuration files
        # noinspection PyTypeChecker
        dict.__init__(self)

        # default Options dict
        default_conf = self.defaultOptions()

        # command line arguments dict
        cli_conf = self.parse_args(custom_arg_list)

        # configuration file options dict:
        if cli_conf['ConfigFile']:
            config_file_conf = self.read_conf(cli_conf['ConfigFile'][0])
        else:
            config_file_conf = self.read_conf(default_conf['ConfigFile'][0])

        # generally importance: cli_conf > config_file_conf > default_conf
        # default_conf has all keys and they are needed if not overwritten later
        for setting_name, setting_value in default_conf.items():
            self[setting_name] = setting_value

        # config_file_conf is supposed to be minimal and all values can be taken
        for setting_name, setting_value in config_file_conf.items():
            self[setting_name] = setting_value

        # cli_conf contains all settings, but only the ones that are not None should be taken
        for setting_name, setting_value in cli_conf.items():
            if setting_value:
                self[setting_name] = setting_value

        # save settings if arguments say so
        if self['Save']:
            self.save_conf()

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

                       'FileOkColor': ['bright red'],
                       'FileBadColor': ['bright green'],
                       'FilterColor': ['grey'],
                       'ErrorResultColor': ['red'],
                       'WarningResultColor': ['yellow'],
                       'InfoResultColor': ['normal'],
                       'DebugResultColor': ['cyan'],

                       'LogType': ['CONSOLE'],
                       'LogOutput': None,
                       'Verbosity': ['INFO'],

                       'ConfigFile': ['.codecfile'],
                       'Save': None,
                       'JobCount': None
                       }
        return defaultValues

    def read_conf(self, codecfile_path, history_list=None):

        """
        Reads config file and includes references config files
        :param codecfile_path: path to configuration file
        :param history_list; list of previously read config files to prevent infinite loops
        :returns: dictionary containing values from config files
        """

        # this cannot be the default argument because it is mutable and would prevent a second run...
        if not history_list: history_list = []

        # this is the dict that saves settings read from configfiles
        config_dict = {}

        # return none if codecfile_path does not point to a file:
        if not os.path.isfile(codecfile_path):
            return {}

        # return none if codecfile_path points to file that is contained in history_list already:
        if history_list and (codecfile_path in history_list):
            return {}

        # open file if possible
        with open(codecfile_path,'r') as codecfile:

            # check if config refers to other config file
            codecfile.seek(0)
            for line in codecfile:
                if line[:11].lower() == 'configfile=':
                    # line[11:] slices first 11 characters that are 'configfile='
                    # .split('#')[0] removes potential '#' and trailing comment
                    # .strip() removes whitespace from front and back
                    new_codecfile_path = line[11:].split('#')[0].strip()

                    #append codecfile_path to history_list so it can't be called again:
                    history_list.append(codecfile_path)

                    #populate config_dict with data from inner config:
                    config_dict = self.read_conf(new_codecfile_path, history_list)



            # overwrite config_dict with values of current configuration file:
            codecfile.seek(0)
            for line in codecfile:

                # ignore line if it only contains a comment:
                # ignore line if it does not contain a '='
                # ignore line if it does not contain a key before '='
                if (not line.strip()[0] == '#') and ('=' in line ) and (not line.strip()[0] == '='):

                    # key is left of '=' and lowercase in general and should not contain whitespace at the end.
                    key = line.split('=')[0].lower().strip()
                    # adjust capital letters for standard settings
                    if key == 'targetdirectories': key = 'TargetDirectories'
                    if key == 'ignoreddirectories': key = 'IgnoredDirectories'
                    if key == 'flatdirectories': key = 'FlatDirectories'
                    if key == 'targetfiletypes': key = 'TargetFileTypes'
                    if key == 'ignoredfiletypes': key = 'IgnoredFileTypes'
                    if key == 'filters': key = 'Filters'
                    if key == 'ignoredfilters': key = 'IgnoredFilters'
                    if key == 'regexfilters': key = 'RegexFilters'
                    if key == 'fileokcolor': key = 'FileOkColor'
                    if key == 'filebadcolor': key = 'FileBadColor'
                    if key == 'filtercolor': key = 'FilterColor'
                    if key == 'errorresultcolor': key = 'ErrorResultColor'
                    if key == 'warningresultcolor': key = 'WarningResultColor'
                    if key == 'inforesultcolor': key = 'InfoResultColor'
                    if key == 'debugresultcolor': key = 'DebugResultColor'
                    if key == 'logtype': key = 'LogType'
                    if key == 'logoutput': key = 'LogOutput'
                    if key == 'verbosity': key = 'Verbosity'
                    if key == 'configfile': key = 'ConfigFile'
                    if key == 'save': key = 'Save'
                    if key == 'jobcount': key = 'JobCount'

                    # Values:
                    # left of '\n', right of first '=', left of first '#', separated by ',',no whitespace at borders
                    value = line.split('\n')[0].split('=')[1].split('#')[0].split(',')

                    for i in range(len(value)):
                        value[i] = value[i].strip()

                        # make it an int if possible:
                        try:
                            value[i] = int(value[i])
                        except ValueError:
                            pass

                        # make it bool if possible:
                        try:
                            if value[i].lower() in ['y','yes','yeah','always','sure','definitely','yup','true']:
                                value[i] = True
                            elif value[i].lower in ['n','no','nope','never','nah','false']:
                                value[i] = False
                        except AttributeError:
                            pass

                        # actually pass changes back to the list:
                        value[value.index(value[i])]=value[i]

                    # key and value should now have the preferred format
                    # config_dict should now contain no values, values from included config files or from above
                    # they should be overwritten in any of these cases
                    config_dict[key] = value

            # all lines have been read. config_dict can be returned
            return config_dict

        # configuration file could not be read, probably because of missing permission or wrong file format
        #TODO: log warning!
        return {}  # this is indeed reachable...





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
        arg_parser.add_argument('-c', '--config', nargs=1, metavar='FILE', dest='ConfigFile',
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

        #make -s --save store arguments in a list or None as all parameters do:
        if arg_vars['Save']: arg_vars['Save'] = [arg_vars['Save']]

        return arg_vars

    def save_conf(self):

        # sane default, mind that in some cases the config will be written to another directory
        save_location = self['ConfigFile'][0]

        # In this case, the config file will be saved to a file different from the config file
        # therefore the config file will be copied to that location if it exists
        # the following routine is then always the same
        if not (self['Save'] == [True] or self['Save'] is None or self['Save'][0] == self['ConfigFile'][0]):
            try:
                shutil.copyfile(self['ConfigFile'][0],self['Save'][0]) # remember that self[*] contains lists
                save_location = self['Save'][0]
            except IOError:
                # Possible errors:
                # - there is no config file at self['ConfigFile']
                # - It is not permitted to read self['ConfigFile']
                # - It is not permitted to write self['save']
                # If self['save'] exists, it will be overwritten without raising this error!
                #TODO: find out what happened and log a warning?
                pass

        # the config should be minimal, none of these defaults should be written:
        default_settings = self.defaultOptions()

        # the config should be minimal, no setting should be written that is already defined through it
        current_conf_settings = self.read_conf(save_location)

        # list of settings that should be written to the config
        # keep them lowercase to find matches!
        settings_to_write = []

        #list of settings that should be deleted from the config (before new values are written)
        # keep them lowercase to find matches!
        settings_to_delete = []

        # make sure all settings get saved if not for one of the above reasons
        for setting, value in self.items():

            if setting in default_settings and self[setting] == default_settings[setting]:
                # setting is a default and should not be written
                # it should even be deleted from the config if it was spedified there
                settings_to_delete.append(setting.lower())

            elif setting in current_conf_settings and self[setting] == current_conf_settings[setting]:
                # setting is already specified as is
                pass
            else:
                if not setting == 'ConfigFile':
                    # configFile should never be overwritten because:
                    # in config files this is only useful to chain configs
                    # at runtime this is not useful
                    # current chains should be kept, though.
                    settings_to_write.append(setting.lower())
                    settings_to_delete.append(setting.lower()) # should be deleted and re-added to prevent contradictions

        # delete config settings that are not current settings:
        for setting, value in current_conf_settings.items():
            if setting not in self:
                settings_to_delete.append(setting.lower())

        # make new config
        new_config = ""
        try:
            with open(save_location,'r') as new_config_file:
                new_config = new_config_file.readlines()

        except FileNotFoundError:
            pass

        new_config = list(new_config) # it was immutable an immutable tuple, it's a list now

        with open(save_location,'w') as new_config_file:

            # this list saves which settings could actually be removed from the direct configuration file
            removed_settings = []
            # remove lines to be removed
            for line in new_config:
                if line.split('=')[0].lower().strip() in settings_to_delete:
                    new_config.remove(line)
                    removed_settings.append(line.split('=')[0].lower().strip())

            # settings that should be removed but were not, might be specified in a nested config
            # they should be overwritten in this one - even if the settings is considered default
            for setting in settings_to_delete:
                if setting not in removed_settings:
                    if setting not in settings_to_write:
                        settings_to_write.append(setting)

            # since self[*] expects settings to be capitalized appropriately, this ugly thing is needed:
            for i in range(len(settings_to_write)):
                if settings_to_write[i] == 'targetdirectories': settings_to_write[i] = 'TargetDirectories'
                if settings_to_write[i] == 'ignoreddirectories': settings_to_write[i] = 'IgnoredDirectories'
                if settings_to_write[i] == 'flatdirectories': settings_to_write[i] = 'FlatDirectories'
                if settings_to_write[i] == 'targetfiletypes': settings_to_write[i] = 'TargetFileTypes'
                if settings_to_write[i] == 'ignoredfiletypes': settings_to_write[i] = 'IgnoredFileTypes'
                if settings_to_write[i] == 'filters': settings_to_write[i] = 'Filters'
                if settings_to_write[i] == 'ignoredfilters': settings_to_write[i] = 'IgnoredFilters'
                if settings_to_write[i] == 'regexfilters': settings_to_write[i] = 'RegexFilters'
                if settings_to_write[i] == 'fileokcolor': settings_to_write[i] = 'FileOkColor'
                if settings_to_write[i] == 'filebadcolor': settings_to_write[i] = 'FileBadColor'
                if settings_to_write[i] == 'filtercolor': settings_to_write[i] = 'FilterColor'
                if settings_to_write[i] == 'errorresultcolor': settings_to_write[i] = 'ErrorResultColor'
                if settings_to_write[i] == 'warningresultcolor': settings_to_write[i] = 'WarningResultColor'
                if settings_to_write[i] == 'inforesultcolor': settings_to_write[i] = 'InfoResultColor'
                if settings_to_write[i] == 'debugresultcolor': settings_to_write[i] = 'DebugResultColor'
                if settings_to_write[i] == 'logtype': settings_to_write[i] = 'LogType'
                if settings_to_write[i] == 'logoutput': settings_to_write[i] = 'LogOutput'
                if settings_to_write[i] == 'verbosity': settings_to_write[i] = 'Verbosity'
                if settings_to_write[i] == 'configfile': settings_to_write[i] = 'ConfigFile'
                if settings_to_write[i] == 'save': settings_to_write[i] = 'Save'
                if settings_to_write[i] == 'jobcount': settings_to_write[i] = 'JobCount'

            # add lines to be written
            for setting in settings_to_write:

                # values segregated by comma without quotation marks and brackets
                value_string = ""
                if self[setting]:
                    for value in self[setting]:
                        if value_string: value_string += ','
                        value_string += str(value)
                else:
                    value_string = str(self[setting])
                # add lines in the needed format
                # '\n' is actually cross platform because file is opened in text mode
                new_config.append("{} = {}\n".format(setting, value_string))

            # let's finally write the config file:
            for line in new_config:
                new_config_file.write(line)

                #TODO: log successful save, catch failures?

    def fill_settings(self, key_list):

        # remove duplicates
        key_list = list(set(key_list))

        #only do this if there are keys in the list
        if key_list:

            # ask for and add settings, that are not present
            print("At least one filter needs settings that are not available!")
            print("Please enter the values for the following settings:")
            print("If you need several values for one settings, please separate then by commas")

            for key in key_list:
                if key not in self.keys():
                    # this key is not available
                    value_line = input("{}: ".format(key))
                    value = value_line.split(',')
                    for i in range(len(value)):
                        value[i] = value[i].strip()

                    self[key] = value

            # offer to save settings if saving is not set
            if not self['Save']:
                save_now = input("Do you want to save the settings now? (y/n)")
                if save_now.lower() in ['y', 'yes', 'yeah', 'always', 'sure', 'definitely', 'yup', 'true']:
                    self['Save'] = [True]

            if self['Save']:
                self.save_conf()


if __name__ == "__main__":
    settings=Settings()