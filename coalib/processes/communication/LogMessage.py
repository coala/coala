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
from coalib.output.LOG_LEVEL import LOG_LEVEL


class LogMessage:
    def __init__(self, log_level, message):
        if not log_level in [LOG_LEVEL.DEBUG, LOG_LEVEL.WARNING, LOG_LEVEL.ERROR]:
            raise ValueError("log_level has to be a valid LOG_LEVEL.")
        if message == "":
            raise ValueError("Empty log messages are not allowed.")

        self.log_level = log_level
        self.message = str(message).strip()

    def __str__(self):
        return '[{}] {}'.format({LOG_LEVEL.DEBUG: _("DEBUG"),
                                 LOG_LEVEL.WARNING: _("WARNING"),
                                 LOG_LEVEL.ERROR: _("ERROR")}.get(self.log_level, _("ERROR")), self.message)

    def __eq__(self, other):
        return isinstance(other, LogMessage) and other.log_level == self.log_level and other.message == self.message

    def __ne__(self, other):
        return not self.__eq__(other)
