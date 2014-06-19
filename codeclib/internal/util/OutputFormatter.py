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
from codeclib.internal.util import ColorPrinter


class OutputFormatter:
    def __init__(self, settings):
        self.settings = settings

    def output_file_results(self, filename, result_list):
        if len(result_list) == 0:
            okcol = self.settings.get('fileokcolor').value
            ColorPrinter.ColorPrinter.print(okcol, filename)
            return

        for val in result_list:
            self.__output_line_result(val)

    def __output_line_result(self, line_result):
        badcol = self.settings.get('filebadcolor').value
        # TODO
        ColorPrinter.ColorPrinter.print(badcol, "UNIMPLEMENTED")
