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
import queue
import sys
from coalib.analysers.ANALYSER_KIND import ANALYSER_KIND
from coalib.analysers.GlobalAnalyzer import GlobalAnalyzer
from coalib.analysers.LocalAnalyzer import LocalAnalyzer
from coalib.misc.StringConstants import StringConstants
from coalib.processes.Process import Process
from coalib.processes.communication.LogMessage import LogMessage, LOG_LEVEL
from coalib.misc.i18n import _
from coalib.settings.Settings import Settings


class AnalyzerRunProcess(Process):
    def __init__(self,
                 file_name_queue,
                 local_analyzer_list,
                 global_analyzer_queue,
                 file_dict,
                 local_result_queue,
                 global_result_queue,
                 message_queue,
                 TIMEOUT=0):
        """
        This is the object that actually runs on the processes

        If parameters type is 'queue (read)' this means it has to implement the get(timeout=TIMEOUT) method and it shall
        raise queue.Empty if the queue is empty up until the end of the timeout. If the queue has the (optional!)
        task_done() attribute, AnalyzerRunProcess will call it after processing each item.

        If parameters type is 'queue (write)' it shall implement the put(object, timeout=TIMEOUT) method.

        If the queues raise any exception not specified here the user will get an 'unknown error' message. So beware of
        that.

        :param file_name_queue: queue (read) of file names to check with local analyzers. Every AnalyzerRunProcess takes
        one of those and checks it with all local analyzers. (Repeat until queue empty.)
        :param local_analyzer_list: list of local analyzer instances
        :param global_analyzer_queue: queue (read) of global analyzer instances
        :param file_dict: dict of all files as {filename:file}, file as in file.readlines()
        :param local_result_queue: queue (write) for results from local analyzers (one item holds results of all
        analyzers for one file, its a tuple with the filename first and then a dict with (analyzer_class_name:
        [result1, result2, ...]))
        :param global_result_queue: queue (write) for results from global analyzers (one item holds a tuple with the
        analyzer name first and then the results of one analyzer for all files)
        :param message_queue: queue (write) for debug/warning/error messages (type LogMessage)
        :param TIMEOUT: in seconds for all queue actions
        """
        if not isinstance(local_analyzer_list, list):
            raise TypeError("local_analyzer_list should be a list")
        if not isinstance(file_dict, dict):
            raise TypeError("file_dict should be a dict")
        if not hasattr(file_name_queue, "get"):
            raise TypeError("file_name_queue should be a queue like thing "
                            "(reading possible via 'get', raises queue.Empty if empty)")
        if not hasattr(global_analyzer_queue, "get"):
            raise TypeError("global_analyzer_queue should be a queue like thing "
                            "(reading possible via 'get', raises queue.Empty if empty)")
        if not hasattr(local_result_queue, "put"):
            raise TypeError("local_result_queue should be a queue like thing (writing possible via 'put')")
        if not hasattr(global_result_queue, "put"):
            raise TypeError("global_result_queue should be a queue like thing (writing possible via 'put')")
        if not hasattr(message_queue, "put"):
            raise TypeError("message_queue should be a queue like thing (writing possible via 'put')")

        Process.__init__(self)

        self.filename_queue = file_name_queue
        self.local_analyzer_list = local_analyzer_list
        self.global_analyzer_queue = global_analyzer_queue

        self.file_dict = file_dict

        self.local_result_queue = local_result_queue
        self.global_result_queue = global_result_queue
        self.message_queue = message_queue

        self.TIMEOUT = TIMEOUT

    def warn(self, *args, delimiter=' ', end=''):
        self.__send_msg(LOG_LEVEL.WARNING, *args, delimiter=delimiter, end=end)

    def err(self, *args, delimiter=' ', end=''):
        self.__send_msg(LOG_LEVEL.ERROR, *args, delimiter=delimiter, end=end)

    def debug(self, *args, delimiter=' ', end=''):
        self.__send_msg(LOG_LEVEL.DEBUG, *args, delimiter=delimiter, end=end)

    def run(self):
        self.run_local_analyzers()
        self.run_global_analyzers()

    def run_local_analyzers(self):
        try:
            while True:
                filename = self.filename_queue.get(timeout=self.TIMEOUT)
                try:
                    self.__run_local_analyzers(filename)
                except:  # pragma: no cover
                    self.err(_("An unknown error occurred while running local analyzers for the file {}. "
                               "Skipping file...".format(filename)), StringConstants.THIS_IS_A_BUG)
                finally:
                    if hasattr(self.filename_queue, "task_done"):
                        self.filename_queue.task_done()
        except queue.Empty:
            return

    def run_global_analyzers(self):
        try:
            while True:
                ga = self.global_analyzer_queue.get(timeout=self.TIMEOUT)
                try:
                    result = self.__run_global_analyzer(ga)
                    if result:
                        self.global_result_queue.put(result, timeout=self.TIMEOUT)
                except:  # pragma: no cover
                    self.err(_("An unknown error occurred while running global analyzer {}. "
                               "Skipping analyzer...").format(ga.__class__.__name__), StringConstants.THIS_IS_A_BUG)
                finally:
                    if hasattr(self.global_analyzer_queue, "task_done"):
                        self.global_analyzer_queue.task_done()
        except queue.Empty:
            return

    def __send_msg(self, log_level, *args, delimiter=' ', end=''):
        output = str(delimiter).join(str(arg) for arg in args) + str(end)
        self.message_queue.put(LogMessage(log_level, output), timeout=self.TIMEOUT)

    def __run_local_analyzers(self, filename):
        if filename not in self.file_dict:
            self.err(_("An internal error occurred."), StringConstants.THIS_IS_A_BUG)
            self.debug(_("The given file through the queue is not in the file dictionary."))

            return

        result_dict = {}
        for analyzer_instance in self.local_analyzer_list:
            r = self.__run_local_analyzer(analyzer_instance, filename)
            if r is not None:
                result_dict[analyzer_instance.__class__.__name__] = r

        self.local_result_queue.put((filename, result_dict), timeout=self.TIMEOUT)

    def __run_local_analyzer(self, analyzer_instance, filename):
        if not isinstance(analyzer_instance, LocalAnalyzer) or analyzer_instance.kind() != ANALYSER_KIND.LOCAL:
            self.warn(_("A given local analyzer ({}) is not valid. Leaving it out...")
                      .format(analyzer_instance.__class__.__name__), StringConstants.THIS_IS_A_BUG)

            return None

        return analyzer_instance.run(filename, self.file_dict[filename])

    def __run_global_analyzer(self, global_analyzer_instance):
        name = global_analyzer_instance.__class__.__name__
        if not isinstance(global_analyzer_instance, GlobalAnalyzer)\
           or global_analyzer_instance.kind() != ANALYSER_KIND.GLOBAL:
            self.warn(_("A given local analyzer ({}) is not valid. Leaving it out...")
                      .format(name), StringConstants.THIS_IS_A_BUG)

            return None

        return name, global_analyzer_instance.run()
