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


class Printer:
    def _print(self, output, **kwargs):
        raise NotImplementedError

    def print(self, *args, delimiter=' ', end='\n', **kwargs):
        output = ""
        delim = ""
        for arg in args:
            output += delim + str(arg)
            delim = str(delimiter)
        output += str(end)

        return self._print(output, **kwargs)
