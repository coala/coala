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
from coalib.parsing.Parser import Parser


class ConfParser(Parser):
    def parse(self, input_data, overwrite=False):
        """
        Parses the input and adds the new data to the existing

        :param input_data: filename
        :param overwrite: behaves like reparse if this is True
        :return a non empty string containing an error message on failure
        """
        raise NotImplementedError

    def reparse(self, input_data):
        """
        Parses the input and overwrites all existent data

        :param input_data: filename
        :return a non empty string containing an error message on failure
        """
        return self.parse(input_data, overwrite=True)
