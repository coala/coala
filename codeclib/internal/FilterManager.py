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
import re
import inspect
import sys
import importlib
import multiprocessing
from queue import Empty
from codeclib.fillib.results import ResultContainer
import webbrowser

class FilterManager:

    @staticmethod
    def get_sub_dirs(dir):
        """returns list of sub_dirs of a directory including that original directory

        :param dir: original directory
        :return:list of sub_dirs of a directory including that original directory
        """
        dir_list = [dir]
        try:
            for subdir in os.listdir(dir):
                if os.path.isdir(os.path.join(dir, subdir)):
                    dir_list.extend(FilterManager.get_sub_dirs(os.path.join(dir, subdir)))
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
        if setting.value and setting.value != ['None']:
            for item in setting.value:
                if item == os.path.abspath(item):
                    abspaths.append(item)
                else:
                    if setting.import_history == ['cmdline'] or setting.import_history == ['default']:
                        abspaths.append(os.path.join(os.getcwd(),item))
                    else:
                        abspaths.append(os.path.join(os.path.dirname(os.path.abspath(setting.import_history[-1])),item))
            return abspaths
        else:
            return[]

    @staticmethod
    def filter_process(settings, file_name_queue, global_filter_class_queue, local_filter_class_list, file_dict, result_queue):

        """This is the method that actually runs on the processes

        :param settings: Settings object
        :param file_name_queue: multiprocessing.queue of file names (so save memory...)
        :param global_filter_class_queue: multiprocessing.queue of global filter classes
        :param local_filter_class_list: list of local filter classes
        :param file_dict: dict of all files as {filename:file}, file as in file.readlines()
        :param result_queue: queue for results
        """
        something_to_do = True
        while something_to_do:
            try:  # run a local filter
                file_name = file_name_queue.get_nowait()
                file_results = ResultContainer.ResultContainer(file_name, settings, type='file')

                for filter_class in local_filter_class_list:
                    filter = filter_class(settings)
                    result_list = filter.run(file_name, file_dict[file_name])
                    for result in result_list:
                        file_results.add(result)
                result_queue.put(file_results)

            except Empty:
                try:  # run a global filter
                    filter_class = global_filter_class_queue.get_nowait()
                    filter = filter_class(settings)
                    filter_results = filter.run(file_dict)
                    result_queue.put(filter_results)

                except Empty:
                    # all tasks done
                    something_to_do = False
                    result_queue.put('DONE')

    @staticmethod
    def get_changes_answer(choices_number):
        assert(type(choices_number) == type(2))
        assert(choices_number > 0)
        while True:
            user_input = input("Please enter the numbers of changes to apply ('y'=all, 'n'=none, 'e'=edit manually): ")
            if user_input.lower().strip() in ['y']:
                return [i+1 for i in range(choices_number)]
            elif user_input.lower().strip() in ['n']:
                return []
            elif user_input.lower().strip() in ['e']:
                return ['EDIT']
            else:
                try:
                    choices_list=[]
                    user_input_list = re.sub(' +',' ',user_input.strip().replace(',',' ')).split(' ')
                    for item in user_input_list:
                        if item.isdigit():
                            assert(0 < int(item) <= choices_number)
                            choices_list.append(int(item))
                        else:
                            item_from, item_to = item.split('-')
                            assert(int(item_to) > int(item_from))
                            for i in range(int(item_from), int(item_to)+1):
                                assert(0 < i <= choices_number)
                                choices_list.append(i)
                    choices_list = list(set(choices_list))
                    return sorted(choices_list)
                except:
                    print("WARNING: incorrect input!")

    @staticmethod
    def do_change(line_result):
        try:
            line_list = []
            try:
                with open(line_result.filename, 'r') as file:
                    line_list = file.readlines()
            except:
                return False, "WARNING: Could not read {}".format(line_result.filename)

            try:
                assert(line_list[line_result.line_number-1] == line_result.original)
            except:
                return False, "WARNING: Line {} of {} is different than expected".format(line_result.line_number, line_result.filename)

            line_list[line_result.line_number-1] = line_result.replacement

            try:
                with open(line_result.filename, 'w') as file:
                    for i in range(len(line_list)):
                        file.write(line_list[i])
            except:
                return False, "WARNING: Changes could not be written to {}".format(line_result.filename)

            return True, "Succesfully changed line {} of {} to {}".format(line_result.line_number, line_result.filename, line_result.replacement)

        except:
            return False, "WARNING: Could not change line {} of {}".format(line_result.line_number, line_result.filename)

    @staticmethod
    def file_name_ends_in(file_name, ending):

        n = len(ending)
        ends_in = (file_name[-1*n:] == ending)

        return ends_in

    @staticmethod
    def show_whitespace(line_string, tab_width=4, color=None):
        result = str()
        for char in line_string:
            if char == ' ':
                if color:
                    result += color + '\u00B7' + '\033[0m'
                else:
                    result += '\u00B7'
            elif char == '\t':
                if color:
                    result += color + '\u2192' + '\033[0m'
                else:
                    result += '\u2192'
                while (len(result) % tab_width != 0):
                    result += ' '
            else:
                result += char

        return result

    def __init__(self, settings):
        self.settings = settings
        self.local_filters, self.global_filters = self.get_filters()
        self.targets = self.get_targets()

    def get_filter_directories(self):

        filter_dirs = []

        default_global_dir = os.path.abspath(os.path.join(
            os.path.split(inspect.getfile(inspect.currentframe()))[0],
            "../globalfilters")) #always codec/codeclib/globalfilters

        default_local_dir = os.path.abspath(os.path.join(
            os.path.split(inspect.getfile(inspect.currentframe()))[0],
            "../localfilters")) #always codec/codeclib/globalfilters

        filter_dirs.extend([default_global_dir, default_local_dir])

        included_filter_dirs = FilterManager.get_abspaths_from_setting(self.settings['includedfilterdirectories'])
        filter_dirs.extend(included_filter_dirs)

        for dir in filter_dirs:
            if not os.path.isdir(dir):
                filter_dirs.remove(dir)

        return filter_dirs


    def get_filters(self):

        local_filters = []
        global_filters = []

        filter_dirs = self.get_filter_directories()

        potential_filter_files = []
        for dir in filter_dirs:
            potential_filter_files.extend(FilterManager.get_dir_files(dir))

        filter_files = []

        # if regexfilters are specified:
        if self.settings['regexfilters'].value and self.settings['regexfilters'].value != ['None']:
            for file in potential_filter_files:
                for regex in self.settings['regexfilters'].value:
                    if re.search(regex, file):
                        filter_files.append(file)
            filter_files = list(set(filter_files))

        # if filters are specified:
        if self.settings['filters'].value and self.settings['filters'].value != ['None']:
            for file in potential_filter_files:
                for name in self.settings['filters'].value:
                    if name in [file, os.path.splitext(file)[0], os.path.basename(file), os.path.splitext(os.path.basename(file))[0]]:
                        filter_files.append(file)

        # neither regexfilters not filters are specified:
        if not (self.settings['regexfilters'].value and self.settings['regexfilters'].value != ['None']) \
                and not (self.settings['filters'].value and self.settings['filters'].value != ['None']):

            filter_files = potential_filter_files

        # if ignorefilters are specified:
        if self.settings['ignoredfilters'].value and self.settings['ignoredfilters'].value != ['None']:
            for file in filter_files:
                for name in self.settings['ignoredfilters'].value:
                    if name in [file, os.path.splitext(file)[0], os.path.basename(file), os.path.splitext(os.path.basename(file))[0]]:
                        filter_files.remove(file)
        filter_files = list(set(filter_files))

        # filter files are ready, let's import those suckers

        for dir in filter_dirs:
            if dir not in sys.path:
                sys.path.insert(0, dir)

        for file in filter_files:
            module_name = os.path.splitext(os.path.basename(file))[0]
            module = importlib.import_module(module_name)
            for name, object in inspect.getmembers(module):
                if hasattr(object, "kind"):
                    if object.kind() == 1:
                        local_filters.append(object)
                    elif object.kind() == 2:
                        global_filters.append(object)
                    else:
                        print("Warning: Module '{}' is of a weird .kind(): {}".format(name, object.kind()))
                        #TODO: proper warning

        return [local_filters, global_filters]

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
            rich_target_dirs.extend(FilterManager.get_sub_dirs(dir))

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

        if self.settings['targetfiletypes'].value and self.settings['targetfiletypes'].value != ['None']:
            if self.settings['ignoredfiletypes'].value and self.settings['ignoredfiletypes'].value != ['None']:

                for file_name in target_files:
                    for good_ending in self.settings['targetfiletypes'].value:
                        if FilterManager.file_name_ends_in(file_name, good_ending):
                            file_good = True
                            for bad_ending in self.settings['ignoredfiletypes'].value:
                                if FilterManager.file_name_ends_in(file_name, bad_ending):
                                    file_good = False
                            if file_good == True:
                                targets.append(file_name)
            else:
                for file_name in target_files:
                    for good_ending in self.settings['targetfiletypes'].value:
                        if FilterManager.file_name_ends_in(file_name, good_ending):
                            targets.append(file_name)
        else:
            if self.settings['ignoredfiletypes'].value and self.settings['ignoredfiletypes'].value != ['None']:
                for file_name in target_files:
                    file_good = True
                    for bad_ending in self.settings['ignoredfiletypes'].value:
                        if FilterManager.file_name_ends_in(file_name, bad_ending):
                            file_good = False
                    if file_good == True:
                        targets.append(file_name)
            else:
                targets = target_files


        return targets


    def get_needed_keys(self):

        filterclass_list = self.local_filters + self.global_filters
        needed_keys_dict_dict_list = []

        for filterclass in filterclass_list:
            filter_answer = {filterclass.__name__: filterclass.get_needed_settings()}
            try:
                assert(type(filter_answer[filterclass.__name__]) == type(dict()))
                needed_keys_dict_dict_list.append(filter_answer)
            except AssertionError:
                print("Warning: expected instance of type {} from {} for needed settings, got instance of type {}!"\
                      .format(type(dict()), filterclass.__name__, type(filter_answer[filterclass.__name__])))
        return needed_keys_dict_dict_list

    def run_processes(self):

        process_count = self.settings['jobcount'].to_int(index = 0)
        if process_count == 0:
            process_count = multiprocessing.cpu_count()
        ProcessManager = multiprocessing.Manager()

        file_dict = ProcessManager.dict()
        file_name_queue = ProcessManager.Queue()
        for file_name in self.targets:
            try:
                with open(file_name,'r') as file:
                    file_dict[file.name] = file.readlines()
                    file_name_queue.put(file.name)
            except:
                print("WARNING: can't open file:", file_name)
                #TODO: ince warning/log

        global_filter_class_queue = ProcessManager.Queue()
        for global_filter_class in self.global_filters:
            global_filter_class_queue.put(global_filter_class)

        local_filter_class_list = ProcessManager.list()
        for filter_class in self.local_filters:
            local_filter_class_list.append(filter_class)

        result_queue = ProcessManager.Queue()
        processes = []

        for i in range(process_count):
            processes.append(multiprocessing.Process(
                target=FilterManager.filter_process,
                args=(self.settings, file_name_queue, global_filter_class_queue, local_filter_class_list, file_dict, result_queue,)))
            processes[i].start()

        processes_done = 0
        while processes_done < process_count:
            try:
                result = result_queue.get(timeout = 0.3)
                if not result:
                    continue
                if result == 'DONE':
                    processes_done += 1
                else:
                    if self.settings['hidefinefiles'].to_bool(0):
                        if result: print(result)
                    else:
                        print(result)
                    self.process_changes(result)
            except Empty:
                pass

    def process_changes(self, result):
        possible_changes = result.get_replacement_line_results()
        actual_changes=[]

        if self.settings['applychanges'].value[0] == 'NO':
            return None
        elif self.settings['applychanges'].value[0] == 'ASK':
            if possible_changes:
                print("The following changes can be applied automagically:")
                for i in range(len(possible_changes)):
                    if result.type == 'file':
                        print("({}):\tline {}:".format(i+1, possible_changes[i].line_number))
                        print("\tfrom:\t{}".format(FilterManager.show_whitespace(possible_changes[i].original,
                              self.settings.get_int_setting('tabwidth'),
                              self.settings.get_color_setting('nonprintablecharscolor'))))
                        print("\tto:\t{}".format(FilterManager.show_whitespace(possible_changes[i].replacement,
                              self.settings.get_int_setting('tabwidth'),
                              self.settings.get_color_setting('nonprintablecharscolor'))))
                    else:
                        print("({}):\tline {} in file {}:".format(i+1, possible_changes[i].line_number, ResultContainer.ResultContainer.fixed_length(possible_changes[i].filename,60)))
                        print("\tfrom:\t{}".format(FilterManager.show_whitespace(possible_changes[i].original,
                              self.settings.get_int_setting('tabwidth'),
                              self.settings.get_color_setting('nonprintablecharscolor'))))
                        print("\tto:\t{}".format(FilterManager.show_whitespace(possible_changes[i].replacement,
                              self.settings.get_int_setting('tabwidth'),
                              self.settings.get_color_setting('nonprintablecharscolor'))))
                actual_changes = FilterManager.get_changes_answer(len(possible_changes))
                if actual_changes == ['EDIT']:
                    actual_changes = []

                    files_to_edit = []
                    for line_result in possible_changes:
                        files_to_edit.append(line_result.filename)
                    files_to_edit = set(files_to_edit)
                    for file in files_to_edit:
                        webbrowser.open(file)

        elif self.settings['applychanges'].value[0] == 'YES':
            actual_changes = [i for i in range(1, len(possible_changes)+1)]
        else:
            print("WARNING: settings['applychanges'].value[0] not in ('YES','NO','ASK'):", self.settings['applychanges'].value[0])

        # let's do it
        for i0 in reversed(range(len(possible_changes))):
            i1 = i0+1 # human_readable index
            if i1 in actual_changes:
                success, msg = FilterManager.do_change(possible_changes[i0])
                if not success:
                    print(msg)




