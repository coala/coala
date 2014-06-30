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

from codeclib.fillib import LocalFilter
from codeclib.fillib.results.LineResult import LineResult
from codeclib.fillib.util import SpacingHelper
from codeclib.fillib.util.settings import Settings


class SpaceConsistencyFilter(LocalFilter.LocalFilter):

    def run(self, filename, file):
        results = []
        filtername = self.__class__.__name__
        assert isinstance(self.settings, Settings)

        use_spaces = self.settings.get_bool_setting("UseSpaces")
        tab_width = self.settings.get_int_setting("TabWidth")
        allow_trailing_spaces = self.settings.get_bool_setting("AllowTrailingSpaces", False)
        indent_helper = SpacingHelper.SpacingHelper(tab_width)

        for line_number, line in enumerate(file):
            if not allow_trailing_spaces:
                replacement = line.rstrip(" \t\n") + "\n"
                if replacement != line:
                    results.append(LineResult(filename,
                                              filtername,
                                              "Line has trailing whitespace characters",
                                              line_number+1,
                                              line,
                                              replacement))
                    line = replacement

            indentation, rest, count = indent_helper.get_indentation(line)
            if use_spaces:
                if indentation.find("\t") >= 0:
                    results.append(LineResult(filename,
                                              filtername,
                                              "Line contains one or more tabs",
                                              line_number+1,
                                              line,
                                              ' '*count + rest))
                continue

            if indentation.find(' '*tab_width) >= 0 or indentation.find(" \t") >= 0:
                    tabs = int(count/tab_width)
                    spaces = count - tabs*tab_width
                    results.append(LineResult(filename,
                                              filtername,
                                              "Line does not use tabs consistently",
                                              line_number+1,
                                              line,
                                              "\t"*tabs + ' '*spaces + rest))

        return results

    @staticmethod
    def get_needed_settings():
        return {"TabWidth" : "Number of spaces to display for a tab",
                "UseSpaces": "True if spaces are to be used, false for tabs"}
