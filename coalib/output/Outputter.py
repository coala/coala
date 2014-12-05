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
from coalib.bears.results.LineResult import Result, LineResult


class Outputter:
    def _print_result(self, result):
        raise NotImplementedError

    def _print_line_result(self, result):
        # You probably want to overwrite this method!
        return self._print_result(result)

    def print_result(self, result):
        """
        Prints the result appropriate to the output medium.

        :param result: A derivative of Result.
        """
        if not isinstance(result, Result):
            raise TypeError("print_result can only handle objects which inherit from Result.")

        if type(result) == LineResult:
            return self._print_line_result(result)

        return self._print_result(result)

    def print_local_results(self, local_result_list, file_dict):
        """
        Prints all given local results. They will be sorted.

        :param local_result_list: List of the local results
        :param file_dict: Dictionary containing filename: file_contents
        """
        raise NotImplementedError

    def acquire_settings(self, settings):
        """
        This method prompts the user for the given settings.

        :param settings: a dictionary with the settings name as key and a list containing a description in [0] and the
                         name of the bears who need this setting in [1] and following. Example:
        {"UseTabs": ["describes whether tabs should be used instead of spaces",
                     "SpaceConsistencyBear",
                     "SomeOtherBear"]}

        :return: a dictionary with the settings name as key and the given value as value.
        """
        raise NotImplementedError
