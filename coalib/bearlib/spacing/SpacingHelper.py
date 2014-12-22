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
from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coalib.settings.Section import Section


class SpacingHelper(SectionCreatable):
    DEFAULT_TAB_WIDTH = 4

    def __init__(self, tab_width=DEFAULT_TAB_WIDTH):
        if not isinstance(tab_width, int):
            raise TypeError("The 'tab_width' parameter should be an integer.")

        self.tab_width = tab_width

    @classmethod
    def from_section(cls, section, **kwargs):
        if not isinstance(section, Section):
            raise TypeError("The 'section' parameter should be a coalib.settings.Section instance.")

        return cls(tab_width=int(section.get("tab_width", kwargs.get("tab_width", cls.DEFAULT_TAB_WIDTH))))

    @staticmethod
    def get_minimal_needed_settings():
        return {}

    @staticmethod
    def get_needed_settings():
        return {"tab_width": "The number of spaces which visually equals a tab."}

    def get_indentation(self, line):
        """
        Checks the lines indentation.

        :param line: A string to check for indentation.
        :return: The indentation count in spaces.
        """
        if not isinstance(line, str):
            raise TypeError("The 'line' parameter should be a string.")

        count = 0
        for char in line:
            if char == ' ':
                count += 1
                continue

            if char == '\t':
                count += self.tab_width - (count % self.tab_width)
                continue

            break

        return count

    def replace_tabs_with_spaces(self, line):
        """
        Replaces tabs in this line with the appropriate number of spaces.

        Example: " \t" will be converted to "    ", assuming the tab_width is set to 4.

        :param line: The string with tabs to replace.
        :return: A string with no tabs.
        """
        if not isinstance(line, str):
            raise TypeError("The 'line' parameter should be a string.")

        result = ""
        for i, char in enumerate(line):
            if char == '\t':
                result += (self.tab_width - i % self.tab_width) * " "
                continue

            result += char

        return result
