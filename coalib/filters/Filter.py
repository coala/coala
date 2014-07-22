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

from coalib.misc.i18n import _
from coalib.filters.FILTER_KIND import FILTER_KIND
from coalib.processes.Process import Process
from coalib.processes.communication.LOG_LEVEL import LOG_LEVEL
from coalib.processes.communication.LogMessage import LogMessage


class Filter(Process):
    """
    This is the base class for every filter. If you want to write a filter, inherit from this class and overwrite at
    least the run_filter method. You can send debug/warning/error messages through the debug_msg(), warn_msg(),
    fail_msg() functions. These will send the appropriate messages so that they are outputted. Be aware that if you
    use fail_msg(), you are expected to also terminate the filter run-through immediately.

    If you need some setup or teardown for your filter, feel free to overwrite the set_up() and tear_down() functions.
    They will be invoked before/after every run_filter invocation.

    Settings are available at all times through self.settings. You can access the translation database with the self._()
    function, it will be routed to the usual gettext _(). Be aware that the strings you use are not necessarily in the
    database, especially if your filter is not shipped with coala. Feel free to use your own translation database in
    this case or consider make your filter available to the coala project.
    """
    def __init__(self, settings,
                 message_queue,
                 TIMEOUT=0.2):
        self.settings = settings
        self.message_queue = message_queue
        self.TIMEOUT = TIMEOUT

    def _(self, msg):
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
        msg = ""
        for i in range(len(args) - 1):
            msg += str(args[i]) + str(delimiter)
        msg += str(args[-1])

        self.message_queue.put(LogMessage(log_level, msg), timeout=self.TIMEOUT)

    def run_filter(self):
        raise NotImplementedError

    def run(self):
        self.debug_msg(_("Setting up filter..."))
        self.set_up()
        self.debug_msg(_("Running filter..."))
        self.run_filter()
        self.debug_msg(_("Tearing down filter..."))
        self.tear_down()

    @staticmethod
    def kind():
        """
        :return: The kind of the filter
        """
        return FILTER_KIND.UNKNOWN

    @staticmethod
    def get_needed_settings():
        """
        This method has to determine which settings are needed by this filter. The user will be prompted for needed
        settings that are not available in the settings file so don't include settings where a default value would do.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        return {}
