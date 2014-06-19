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


class FILTER_KIND:
    UNKNOWN = 0
    LOCAL   = 1
    GLOBAL  = 2


class FilterBase(object):
    def __init__(self, settings):
        self.settings = settings

    def tear_up(self):
        pass

    def tear_down(self):
        pass

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
