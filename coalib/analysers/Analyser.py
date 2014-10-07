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
import sys
import traceback

from coalib.misc.StringConstants import StringConstants
from coalib.misc.i18n import _
from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.processes.Process import Process
from coalib.processes.communication.LogMessage import LogMessage
from coalib.settings.Settings import Settings


class Analyser(Process):
    """
    This is the base class for every analyser. If you want to write an analyser, inherit from this class and overwrite
    at least the run_analyser method. You can send debug/warning/error messages through the debug_msg(), warn_msg(),
    fail_msg() functions. These will send the appropriate messages so that they are outputted. Be aware that if you
    use fail_msg(), you are expected to also terminate the analyser run-through immediately.

    If you need some setup or teardown for your analyser, feel free to overwrite the set_up() and tear_down() functions.
    They will be invoked before/after every run_analyser invocation.

    Settings are available at all times through self.settings. You can access the translation database with the self._()
    function, it will be routed to the usual gettext _(). Be aware that the strings you use are not necessarily in the
    database, especially if your analyser is not shipped with coala. Feel free to use your own translation database in
    this case or consider make your analyser available to the coala project.
    """
    def __init__(self,
                 settings,
                 message_queue,
                 TIMEOUT=0):
        if not isinstance(settings, Settings):
            raise TypeError("settings has to be of type Settings.")
        if not hasattr(message_queue, "put") and message_queue is not None:
            raise TypeError("message_queue has to be a Queue or None.")

        self.settings = settings
        self.message_queue = message_queue
        self.TIMEOUT = TIMEOUT

    @staticmethod
    def _(msg):
        return _(msg)

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def debug_msg(self, *args, delimiter=' '):
        self.__send_msg(LOG_LEVEL.DEBUG, delimiter, *args)

    def warn_msg(self, *args, delimiter=' '):
        self.__send_msg(LOG_LEVEL.WARNING, delimiter, *args)

    def fail_msg(self, *args, delimiter=' '):
        self.__send_msg(LOG_LEVEL.ERROR, delimiter, *args)

    def __send_msg(self, log_level, delimiter, *args):
        if self.message_queue is None:
            return

        if len(args) == 0:
            return

        msg = ""
        for i in range(len(args) - 1):
            msg += str(args[i]) + str(delimiter)
        msg += str(args[-1])

        self.message_queue.put(LogMessage(log_level, msg), timeout=self.TIMEOUT)

    def run_analyser(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        try:
            self.debug_msg(_("Setting up analyser..."))
            self.set_up()
            self.debug_msg(_("Running analyser..."))
            retval = self.run_analyser(*args, **kwargs)
            self.debug_msg(_("Tearing down analyser..."))
            self.tear_down()

            return retval
        except:
            exception = sys.exc_info()
            self.debug_msg(_("Unknown failure in worker process.\n"
                             "Exception: {}\nTraceback:\n{}").format(str(exception[0]),
                                                                     traceback.extract_tb(exception[2])))
            self.warn_msg(_("An unknown failure occurred and an analyzer run is aborted."),
                          StringConstants.THIS_IS_A_BUG)

    @staticmethod
    def kind():
        """
        :return: The kind of the analyser
        """
        raise NotImplementedError

    @staticmethod
    def get_needed_settings():
        """
        This method has to determine which settings are needed by this analyser. The user will be prompted for needed
        settings that are not available in the settings file so don't include settings where a default value would do.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        return {}
