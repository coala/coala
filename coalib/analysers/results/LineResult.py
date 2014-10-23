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
from coalib.analysers.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.analysers.results.Result import Result


class LineResult(Result):
    """
    This is a result that affects one specific line in a file.
    """
    def __init__(self, origin, line_nr, line, message, file, replacement=None, severity=RESULT_SEVERITY.NORMAL):
        Result.__init__(self, origin=origin, message=message, file=file, severity=severity)
        self.line_nr = line_nr
        self.line = line
        self.replacement = replacement

    # Result's __ne__ uses __eq__ so no need to overwrite that too
    def __eq__(self, other):
        return Result.__eq__(self, other) and\
            isinstance(other, LineResult) and\
            self.line_nr == other.line_nr and\
            self.line == other.line and\
            self.replacement == other.replacement
