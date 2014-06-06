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

import multiprocessing
import os
import re


class FilterManager:

    @staticmethod
    def sub_dirs(dir):
        """returns list of sub_dirs of a directory including that original directory

        :param dir: original directory
        :return:list of sub_dirs of a directory including that original directory
        """
        dir_list = [dir]
        try:
            for subdir in os.listdir(dir):
                if os.path.isdir(os.path.join(dir, subdir)):
                    dir_list.extend(FilterManager.sub_dirs(os.path.join(dir, subdir)))
        except PermissionError:
            print("{} is not accessible and will be ignored!".format(dir))
            return None
        return dir_list

    @staticmethod
    def get_dir_files(dir):
        """lists absolute paths to all files from a directory

        :param dir: directrory to list files from
        :return: List of files of that directory
        """
        file_list = []
        for file in os.listdir(dir):
            try:
                if os.path.isfile(os.path.join(dir, file)):
                    file_list.append(os.path.join(dir, file))
            except PermissionError:
                print("{} is not accessible and will be ignored!".format(file))
                return None
        return file_list

    @staticmethod
    def get_abspaths_from_setting(setting):
        abspaths = []
        if setting.value and setting.value != [None]:
            for item in setting.value:
                if item == os.path.abspath(item):
                    abspaths.append(item)
                else:
                    if setting.import_history == ['cmdline'] or setting.import_history == ['default']:
                        abspaths.append(os.path.join(os.getcwd(),item))
                    else:
                        abspaths.append(os.path.join(setting.import_history[-1], item))
            return abspaths
        else:
            return[]

    def __init__(self, settings):
        self.settings = settings
        self.global_filters = self.get_filters(None) # GlobalBase
        self.local_filters = self.get_filters(None) # LocalBase
        self.targets = self.get_targets()
        #TODO Process management
        pass


    def get_filters(self, base_class):
        #TODO
        pass

    def get_targets(self):

        target_dirs = []
        target_files = []
        blacklist = FilterManager.get_abspaths_from_setting(self.settings['ignoreddirectories'])
        target_directories = FilterManager.get_abspaths_from_setting(self.settings['targetdirectories'])
        flat_directories = FilterManager.get_abspaths_from_setting(self.settings['flatdirectories'])


        for item in target_directories:
            if os.path.isfile(item) and item not in blacklist:
                target_files.append(item)
            elif os.path.isdir(item) and item not in blacklist:
                target_dirs.append(item)

        rich_target_dirs = []
        for dir in target_dirs:
            rich_target_dirs.extend(FilterManager.sub_dirs(dir))

        for item in flat_directories:
            if os.path.isfile(item) and item not in blacklist:
                target_files.append(item)
            elif os.path.isdir(item) and item not in blacklist:
                rich_target_dirs.append(item)

        for dir in rich_target_dirs:
            files = FilterManager.get_dir_files(dir)
            if files:
                for file in files:
                    if file not in blacklist:
                        target_files.append(file)

        # at this point we have all files together and need to sort.
        targets = []
        if self.settings['targetfiletypes'].value and self.settings['targetfiletypes'].value != [None]:
            if self.settings['ignoredfiletypes'].value and self.settings['ignoredfiletypes'].value != [None]:
                for file_name in target_files:
                    for good_ending in self.settings['targetfiletypes'].value:
                        for bad_ending in self.settings['ignoredfiletypes'].value:
                            if re.search(good_ending + '$', file_name) and not re.search(bad_ending + '$', file_name):
                                targets.append(file_name)
            else:
                for file_name in target_files:
                    for good_ending in self.settings['targetfiletypes'].value:
                        if re.search(good_ending + '$', file_name):
                            targets.append(file_name)
        else:
            if self.settings['ignoredfiletypes'].value and self.settings['ignoredfiletypes'].value != [None]:
                for file_name in target_files:
                    for bad_ending in self.settings['ignoredfiletypes'].value:
                        if not re.search(bad_ending + '$', file_name):
                            targets.append(file_name)
            else:
                targets = target_files

        #print(targets)
        return targets


    def get_needed_keys(self):
        #TODO
        return []

    def run_processes(self):
        #TODO
        pass
