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


class GlobalAnalyzer(Analyser):
    def __init__(self,
                 file_dict,  # filename : file contents
                 settings,
                 message_queue,
                 TIMEOUT=0.2):
        Analyser.__init__(self, settings, message_queue, TIMEOUT)
        self.file_dict = file_dict

    @staticmethod
    def kind():
        return ANALYSER_KIND.GLOBAL
