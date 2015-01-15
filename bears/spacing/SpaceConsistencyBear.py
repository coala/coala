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
    def run_bear(self,
                 filename,
                 file,
                 UseSpaces: bool,
                 AllowTrailingSpaces: bool=False,
                 tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH):
        """
        Checks the space consistency for each line.

        :param UseSpaces: True if spaces are to be used instead of tabs.
        :param AllowTrailingSpaces: Wether to allow trailing whitespace or not.
        :param tab_width: Number of spaces representing one tab.
        """
        results = []
        filtername = self.__class__.__name__

        spacing_helper = SpacingHelper(tab_width)

        for line_number, line in enumerate(file):
            if not AllowTrailingSpaces:
                replacement = line.rstrip(" \t\n") + "\n"
                if replacement != line:
                    results.append(LineResult(filtername,
                                              line_number+1,
                                              line,
                                              self._("Line has trailing whitespace characters"),
                                              filename))
                    line = replacement

            if UseSpaces:
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
