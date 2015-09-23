import os
import dbus.service

from coalib.settings.ConfigurationGathering import find_user_config
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.processes.Processing import execute_section
from coalib.parsing.Globbing import fnmatch
from coalib.settings.Setting import path_list
from coalib.results.HiddenResult import HiddenResult
from coalib.output.printers.ListLogPrinter import ListLogPrinter
from coalib.output.Interactions import fail_acquire_settings
from coalib.misc.Exceptions import get_exitcode


class DbusDocument(dbus.service.Object):
    interface = "org.coala_analyzer.v1"

    def __init__(self, doc_id, path=""):
        """
        Creates a new dbus object-path for every document that a
        DbusApplication wants coala to analyze. It stores the information
        (path) of the document and the config file to use when analyzing the
        given document.

        :param doc_id: An id for the document.
        :param path:   The path to the document.
        """
        dbus.service.Object.__init__(self)

        self.config_file = ""
        self.path = path
        self.doc_id = doc_id

    @dbus.service.method(interface,
                         in_signature="",
                         out_signature="s")
    def FindConfigFile(self):
        """
        This method uses the path of the document to identify a user config
        file for it

        :return: The config file path
        """
        if self.path == "":
            return ""

        self.config_file = find_user_config(self.path)
        return self.config_file

    @dbus.service.method(interface,
                         in_signature="s",
                         out_signature="s")
    def SetConfigFile(self, config_file):
        """
        This method sets the config file to use. It has to be an absolute path,
        as otherwise it is difficult to find it.

        :param config_file: The path fo the config file to use. This has to be
                            an absolute path
        :return:            The config path which has been used
        """
        self.config_file = config_file
        return self.config_file

    @dbus.service.method(interface,
                         in_signature="",
                         out_signature="s")
    def GetConfigFile(self):
        """
        This method gets the config file which is being used

        :return: The config path which is being used
        """
        return self.config_file

    # Signature explanation:
    # s -> string
    # b -> boolean
    # i -> integer (32bit)
    # a -> array (list of tuple in python)
    # () -> structure (or tuple in python)
    # a{ss} -> dictionary with string keys and string values
    @dbus.service.method(interface,
                         in_signature="",
                         out_signature="(iaa{ss}a(sbaa{ss}))")
    def Analyze(self):
        """
        This method analyzes the document and sends back the result

        :return: The output is a list with an element for each section.
                 It contains:
                 - The name of the section
                 - Boolean which is true if all bears in the section executed
                   successfully
                 - List of results where each result is a list which contains:
                   (str)origin, (str)message, (str)file, (str)line_nr,
                   (str)severity
        """
        retval = []
        if self.path == "" or self.config_file == "":
            return retval

        args = ["--config=" + self.config_file]

        log_printer = ListLogPrinter()
        exitcode = 0
        try:
            yielded_results = False
            (sections,
             local_bears,
             global_bears,
             targets) = gather_configuration(fail_acquire_settings,
                                             log_printer,
                                             arg_list=args)

            for section_name in sections:
                section = sections[section_name]

                if not section.is_enabled(targets):
                    continue

                if any([fnmatch(self.path, file_pattern)
                        for file_pattern in path_list(section["files"])]):

                    section["files"].value = self.path
                    section_result = execute_section(
                        section=section,
                        global_bear_list=global_bears[section_name],
                        local_bear_list=local_bears[section_name],
                        print_results=lambda *args: True,
                        log_printer=log_printer)
                    yielded_results = yielded_results or section_result[0]

                    retval.append(
                        DbusDocument.results_to_dbus_struct(section_result,
                                                            section_name))

            if yielded_results:
                exitcode = 1
        except BaseException as exception:  # pylint: disable=broad-except
            exitcode = exitcode or get_exitcode(exception, log_printer)

        logs = [log.to_string_dict() for log in log_printer.logs]
        return (exitcode, logs, retval)

    @staticmethod
    def results_to_dbus_struct(section_result, section_name):
        """
        Converts the result tuple given by execute_section() - which has
        dictionaries and classes inside it - into a purely array based format
        as dbus protocol only allows arrays.

        :param section_result: The result tuple given by execute_section()
                               for a section
        :param section_name:   The name of the section
        :return:               The result for a section in the form of an
                               array which is sendable through dbus.
        """
        results_for_section = []
        for i in range(1, 3):  # Loop over bear types - local, global

            # Loop over every file affected for local bears
            # and every bear for global bears
            for key, value in section_result[i].items():

                # Loop over every result for a file
                results_for_section += [result.to_string_dict()
                    for result in filter(
                        lambda x: not isinstance(x, HiddenResult),
                        value)]

        return [section_name, section_result[0], results_for_section]

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        if new_path:
            new_path = os.path.abspath(os.path.expanduser(new_path))
        self._path = new_path
