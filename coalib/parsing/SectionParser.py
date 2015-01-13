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


class SectionParser:
    def parse(self, input_data):
        """
        Parses the input and adds the new data to the existing

        :param input_data: filename or other input
        :return: the section dictionary
        """

        raise NotImplementedError

    def reparse(self, input_data):
        """
        Parses the input and overwrites all existent data

        :param input_data: filename or other input
        :return: the section dictionary
        """
        raise NotImplementedError

    def export_to_settings(self):
        """
        :return a dict of section objects representing the current parsed things
        """
        raise NotImplementedError
