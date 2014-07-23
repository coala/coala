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

from coalib.misc.i18n import _
from coalib.processes.communication.LOG_LEVEL import LOG_LEVEL


class LogMessage:
    def __init__(self, log_level=LOG_LEVEL.DEBUG, message=""):
        self.log_level = log_level
        self.message = str(message)

    def __str__(self):
        return '[{}] {}'.format({LOG_LEVEL.DEBUG: _("DEBUG"),
                                 LOG_LEVEL.WARNING: _("WARNING"),
                                 LOG_LEVEL.ERROR: _("ERROR")}.get(self.log_level, _("ERROR")), self.message)
