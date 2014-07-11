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

class LOG_LEVEL:
    DEBUG = 0
    WARNING = 1
    ERROR = 2


class LogMessage:
    def __init__(self, log_level, message):
        assert(isinstance(LOG_LEVEL, log_level))
        self.log_level = log_level
        self.message = message

    def __str__(self):
        return '[{}] {}'.format({LOG_LEVEL.DEBUG: "DEBUG",
                                 LOG_LEVEL.WARNING: "WARNING",
                                 LOG_LEVEL.ERROR: "ERROR"}.get(self.log_level, "ERROR"), self.message)
