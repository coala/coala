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
import os
from coalib.misc.StringConverter import StringConverter


def path(obj):
    return obj.__path__()

class Setting(StringConverter):
    def __init__(self, key, value, origin="", strip_whitespaces=True):
        StringConverter.__init__(self, value, strip_whitespaces=strip_whitespaces)
        self.key = str(key)
        if self.key == "":
            raise ValueError("An empty key is not allowed for a setting.")
        self.origin = str(origin)

    def __path__(self):
        if self.origin == "":
            raise ValueError("Cannot determine path without origin.")
        return os.path.join(self.origin, str(self))
