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


class SpacingHelper:
    def __init__(self, tab_width):
        self.tab_width = tab_width

    def get_indentation(self, line):
        """
        Checks the line for indentation
        :param line: the line to check
        :return: (indentation, everything else, indentation count in spaces)
        """
        count = 0
        for i, char in enumerate(line):
            if char == ' ':
                count += 1
                continue

            if char == '\t':
                rest = count % self.tab_width
                count += self.tab_width - rest
                continue

            return line[0:i], line[i:], count
        return line, "", count
