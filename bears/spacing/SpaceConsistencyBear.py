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
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.results.LineResult import LineResult
from coalib.bears.LocalBear import LocalBear


class SpaceConsistencyBear(LocalBear):
    """
    This bear checks the space consistency of each line.
    """
    def run_bear(self, filename, file):
        results = []
        filtername = self.__class__.__name__

        use_spaces = bool(self.section["UseSpaces"])
        allow_trailing_spaces = bool(self.section.get("AllowTrailingSpaces", "false"))
        spacing_helper = SpacingHelper.from_section(self.section)

        for line_number, line in enumerate(file):
            if not allow_trailing_spaces:
                replacement = line.rstrip(" \t\n") + "\n"
                if replacement != line:
                    results.append(LineResult(filtername,
                                              line_number+1,
                                              line,
                                              self._("Line has trailing whitespace characters"),
                                              filename))
                    line = replacement

            if use_spaces:
                replacement = spacing_helper.replace_tabs_with_spaces(line)
                if replacement != line:
                    results.append(LineResult(filtername,
                                              line_number+1,
                                              line,
                                              self._("Line contains one or more tabs"),
                                              filename))
            else:
                replacement = spacing_helper.replace_spaces_with_tabs(line)
                if replacement != line:
                    results.append(LineResult(filtername,
                                              line_number+1,
                                              line,
                                              self._("Line contains with tab replaceable spaces"),
                                              filename))

        return results

    @staticmethod
    def get_needed_settings():
        needed_settings = SpacingHelper.get_minimal_needed_settings()
        needed_settings.update({"UseSpaces": "True if spaces are to be used, false for tabs"})

        return needed_settings
