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
from coalib.analysers.helpers.RESULT_SEVERITY import RESULT_SEVERITY


class Result:
    def __init__(self, origin, message, file=None, severity=RESULT_SEVERITY.NORMAL):
        self.origin = origin
        self.message = message
        self.file = file
        self.severity = severity

    def __eq__(self, other):
        return isinstance(other, Result) and \
            self.origin == other.origin and \
            self.message == other.message and \
            self.file == other.file and \
            self.severity == other.severity

    def __ne__(self, other):
        return not self.__eq__(other)
