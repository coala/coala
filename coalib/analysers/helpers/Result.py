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
from coalib.analysers.helpers.ANNOTATION_SEVERITY import ANNOTATION_SEVERITY
from coalib.misc.i18n import _


class Result:
    def __init__(self,
                 file_name,
                 line_nr,
                 line,
                 relevant_lines_before=1,
                 severity=ANNOTATION_SEVERITY.NORMAL):
        self.file_name = file_name
        self.line_nr = line_nr
        self.line = line
        self.relevant_lines_before = relevant_lines_before
        self.severity = severity

    def __eq__(self, other):
        self.__check_other_for_comparision(other)

        return ((self.line_nr == other.line_nr) and
                (self.line == other.line) and
                (self.severity == other.severity) and
                (self.relevant_lines_before == other.relevant_lines_before))

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        self.__check_other_for_comparision(other)

        return ((self.line_nr < other.line_nr) or
                (self.line_nr == other.line_nr and
                 self.line == other.line and
                 self.severity < other.severity))

    def __gt__(self, other):
        self.__check_other_for_comparision(other)

        return ((self.line_nr > other.line_nr) or
                (self.line_nr == other.line_nr and
                 self.line == other.line and
                 self.severity > other.severity))

    def __le__(self, other):
        self.__check_other_for_comparision(other)

        return ((self.line_nr <= other.line_nr) or
                (self.line_nr == other.line_nr and
                 self.line == other.line and
                 self.severity <= other.severity))

    def __ge__(self, other):
        self.__check_other_for_comparision(other)

        return ((self.line_nr >= other.line_nr) or
                (self.line_nr == other.line_nr and
                 self.line == other.line and
                 self.severity >= other.severity))

    def __check_other_for_comparision(self, other):
        if not isinstance(other, Result):
            raise TypeError(_("Comparision of a Result with a non-Result is impossible."))

        if self.file_name != other.file_name:
            raise AttributeError(_("Comparision of results affecting different files is impossible."))
