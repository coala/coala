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
from coalib.output.ConsolePrinter import ConsolePrinter
from coalib.output.Outputter import Outputter
from coalib.misc.i18n import _


class ConsoleOutputter(Outputter, ConsolePrinter):
    def __init__(self):
        Outputter.__init__(self)
        ConsolePrinter.__init__(self)

    def require_settings(self, settings):
        result = {}
        for setting, helptext in settings.items():
            result[setting] = self._require_setting(setting, helptext)

        return result

    def _require_setting(self, setting, helptext):
        return input(_("Please enter a value for the needed setting \"{}\" ({}): ").format(setting, helptext))
