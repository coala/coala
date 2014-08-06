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
from datetime import datetime
from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.output.Printer import Printer
from coalib.misc.i18n import _
from coalib.processes.communication.LogMessage import LogMessage


class LogPrinter(Printer):
    def __init__(self, timestamp_format="%x"):
        self.timestamp_format = timestamp_format

    def _get_log_prefix(self, log_level, timestamp):
        datetime_string = timestamp.strftime(self.timestamp_format)

        if datetime_string != "":
            datetime_string = "["+datetime_string+"]"

        return '[{}]{} '.format({LOG_LEVEL.DEBUG: _("DEBUG"),
                                 LOG_LEVEL.WARNING: _("WARNING"),
                                 LOG_LEVEL.ERROR: _("ERROR")}.get(log_level, _("ERROR")),
                                datetime_string)

    def log(self, log_message, timestamp=None, **kwargs):
        if not isinstance(log_message, LogMessage):
            raise TypeError("log_message should be of type LogMessage.")
        if not isinstance(timestamp, datetime):
            timestamp = datetime.today()

        prefix = self._get_log_prefix(log_message.log_level, timestamp)

        return self.print(prefix, log_message.message, delimiter="", **kwargs)
