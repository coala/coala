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


from codeclib.fillib import FilterBase

class LocalFilter(FilterBase.FilterBase):

    @staticmethod
    def kind():
        return FilterBase.FILTER_KIND.LOCAL

    def run(self, filename, file):
        """
        Checks the given file.

        :param filename: The filename of the file
        :param file: The file contents as string array
        :return: A list of LineResult
        """
        raise NotImplementedError("This function has to be implemented for a runnable filter.")
