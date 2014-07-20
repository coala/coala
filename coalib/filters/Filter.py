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
from coalib.filters import FILTER_KIND
from coalib.processes.Process import Process


class Filter(Process):
    def __init__(self, settings):
        self.settings = settings

    def tear_up(self):
        pass

    def tear_down(self):
        pass

    def debug_msg(self, *args, delimiter=' '):
        # TODO throw message into queue
        pass

    def warn_msg(self, *args, delimiter=' '):
        # TODO throw warning into queue
        pass

    def fail_msg(self, *args, delimiter=' '):
        # TODO throw error into queue
        pass

    def run_filter(self):
        raise NotImplementedError

    def run(self):
        self.debug_msg(_("Tearing up filter..."))
        self.tear_up()
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
