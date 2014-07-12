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
from coalib.fillib.misc.StringConstants import StringConstants


class StringConverter:
    def __init__(self, value, strip_whitespaces=True):
        self.value = value
        self.strip_whitespaces = strip_whitespaces

    def __str__(self):
        if self.strip_whitespaces:
            return self.value.strip()

        return self.value

    def __bool__(self):
        if self.value in StringConstants.TRUE_STRINGS:
            return True
        if self.value in StringConstants.FALSE_STRINGS:
            return False
        raise AttributeError
