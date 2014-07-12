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
from coalib.fillib.results.Result import Result


class AnnotationResult(Result):
    def __init__(self, filename, line_number, line, annotation, filter_name):
        self.filename=filename
        self.line_number = line_number
        self.line = line
        self.annotation = annotation
        self.filter_name = filter_name
