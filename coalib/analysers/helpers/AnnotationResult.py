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
from coalib.analysers.helpers.Result import Result


class AnnotationResult(Result):
    def __init__(self,
                 message,
                 file_name,
                 line_nr,
                 line,
                 relevant_lines_before=1,
                 severity=ANNOTATION_SEVERITY.NORMAL):
        Result.__init__(self)
        self.message = message
        self.file_name = file_name
        self.line_nr = line_nr
        self.line = line
        self.relevant_lines_before = relevant_lines_before
        self.severity = severity
