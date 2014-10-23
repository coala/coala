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
from coalib.analysers.helpers.Result import Result


class Outputter:
    def _print_result(self, result):
        raise NotImplementedError

    def print_result(self, result):
        if not isinstance(result, Result):
            raise TypeError("print_result can only handle objects which inherit from Result.")

        # TODO add API for special results as soon as they're there, if not fallback to:
        return self._print_result(result)

    def acquire_settings(self, settings):
        """
        This method prompts the user for the given settings.

        :param settings: a dictionary with the settings name as key and a list containing a description in [0] and the
                         name of the filters who need this setting in [1] and following. Example:
        {"UseTabs": ["describes whether tabs should be used instead of spaces",
                     "SpaceConsistencyFilter",
                     "SomeOtherFilter"]}

        :return: a dictionary with the settings name as key and the given value as value.
        """
        raise NotImplementedError
