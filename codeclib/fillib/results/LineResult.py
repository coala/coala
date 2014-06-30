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

from functools import total_ordering

@total_ordering
class LineResult:
    def __init__(self, filename, filter_name, error_message, line_number, original, replacement=None):
        self.filename = filename
        self.filter_name = filter_name
        self.error_message = error_message
        self.line_number = line_number
        self.original = original
        self.replacement = replacement
        self.counter = 0

    def __lt__(self, other):
        if self.filename == other.filename:
            if self.line_number == other.line_number:
                if self.filter_name == other.filter_name:
                    if self.counter < other.counter:
                        return True
                    else:
                        return False
                elif self.filter_name < other.filter_name:
                    return True
                else:
                    return False
            elif self.line_number < other.line_number:
                return True
            else:
                return False
        elif self.filename.lower() < other.filename.lower():
            return True
        elif self.filename.lower() > other.filename.lower():
            return False
        else:
            if self.filename < other.filename:
                return True
            else:
                return False

    def __eq__(self, other):
        return type(self)       == type(other)       and \
               self.filename    == other.filename    and \
               self.line_number == other.line_number and \
               self.filter_name == other.filter_name and \
               self.counter == other.counter
