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
from coalib.analysers.Analyser import Analyser
from coalib.analysers.ANALYSER_KIND import ANALYSER_KIND


class LocalAnalyzer(Analyser):
    def __init__(self,
                 settings,
                 message_queue,
                 TIMEOUT=0):
        Analyser.__init__(self, settings, message_queue, TIMEOUT)

    @staticmethod
    def kind():
        return ANALYSER_KIND.LOCAL

    def run_analyser(self, filename, file):
        """
        Checks the given file.

        :param filename: The filename of the file
        :param file: The file contents as string array
        :return: A list of Result
        """
        raise NotImplementedError("This function has to be implemented for a runnable filter.")
