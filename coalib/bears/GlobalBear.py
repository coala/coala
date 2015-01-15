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
from coalib.bears.Bear import Bear
from coalib.bears.BEAR_KIND import BEAR_KIND


class GlobalBear(Bear):
    """
    A GlobalBear is able to analyze semantical facts across several file.

    The results of a GlobalBear will be presented grouped by the origin Bear. Therefore Results spanning above multiple
    files are allowed and will be handled right.

    If you only look at one file at once anyway a LocalBear is better for your needs. (And better for performance and
    usability for both user and developer.)
    """

    def __init__(self,
                 file_dict,  # filename : file contents
                 section,
                 message_queue,
                 TIMEOUT=0):
        Bear.__init__(self, section, message_queue, TIMEOUT)
        self.file_dict = file_dict

    @staticmethod
    def kind():
        return BEAR_KIND.GLOBAL

    def run_bear(self, *args):
        """
        Handles all files in file_dict.

        :return: A list of Result type.
        """
        raise NotImplementedError("This function has to be implemented for a runnable bear.")
