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

from functools import total_ordering
from codeclib.fillib import ResultOutput
import os

@total_ordering
class ResultContainer:

    @staticmethod
    def fixed_length(str, length):
        assert(length > 4)
        if len(str) < length:
            #str += ' '*(length-len(str))
            return str
        elif len(str) == length:
            return str
        else:  # str longer than length
            if length%2 == 0:  # is even
                a = int((length/2)-2)
                b = int((length/2)-1)
            else:
                a = b = int((length-3)/2)
            str = str[:a]+'...'+str[-b:]
            return str

    def __init__(self, caption, settings, line_result_list=None, type='file'):
        self.settings = settings
        if line_result_list:
            self.line_result_list = sorted(line_result_list)
        else:
            self.line_result_list = []
        self.caption = ResultContainer.fixed_length(caption, 80)
        if type == 'filter':
            self.type = type
        else:
            self.type = 'file'
        self.output = None
        self.LineResultCounter = 0

    def get_replacement_line_results(self):
        possible_changes = []
        for LineResult in self.line_result_list:
            if LineResult.replacement:
                possible_changes.append(LineResult)
        return possible_changes

    def add(self, line_result):
        self.LineResultCounter += 1
        line_result.counter = self.LineResultCounter
        self.line_result_list.append(line_result)
        self.line_result_list = sorted(self.line_result_list)

    def __bool__(self):
        try:
            if len(self.line_result_list) > 0 and self.line_result_list != [None]:
                return True
            else:
                return False
        except ValueError:
            print("nonzero exception")
            return False

    def __lt__(self, other):
        if self.type == 'file' and other.type == 'filter':
            return True
        elif self.type == 'filter' and other.type == 'file':
            return False
        else:
            if self.caption.lower() < other.caption.lower():
                return True
            elif self.caption.lower() > other.caption.lower():
                return False
            else:
                if self.caption < other.caption:
                    return True
                else:
                    return False

    def __eq__(self, other):
        return type(self) == type(other) and self.type == other.type and self.caption == other.caption


    def __str__(self):

        if not self.output:
            FileOkColor = self.settings['fileokcolor'].to_color_code(0)
            FileBadColor = self.settings['filebadcolor'].to_color_code(0)
            FilterColor = self.settings['filtercolor'].to_color_code(0)
            NormalColor = '\033[0m'

            if not bool(self):
                caption = FileOkColor + self.caption + NormalColor
            else:
                caption = FileBadColor + self.caption + NormalColor

            Output = ResultOutput.OutputObject(caption)

            if self.type == 'file':
                for i in range(len(self.line_result_list)):
                    line = ResultOutput.OutputLine()
                    line.add_elem(self.line_result_list[i].filter_name+': ', FilterColor)
                    line.add_elem("line {}: ".format(self.line_result_list[i].line_number, NormalColor))
                    line.add_elem(self.line_result_list[i].error_message, NormalColor)
                    Output.add_line(line)
            else:  # type = filter
                affected_files = []
                for line_result in self.line_result_list:
                    affected_files.append(line_result.filename)
                affected_files = sorted(list(set(affected_files)))
                for i in range(len(affected_files)):
                    line = ResultOutput.OutputLine()
                    line.add_elem(self.fixed_length(affected_files[i],60)+': ', FileBadColor)
                    for ii in range(len(self.line_result_list)):
                        subline = ResultOutput.OutputLine
                        if self.line_result_list[ii].filename == affected_files[i]:
                            subline.add_elem("line {}: ".format(self.line_result_list[ii].line_number, NormalColor))
                            subline.add_elem(self.line_result_list[ii].error_message, NormalColor)
                            line.append_line(subline)
                        Output.add_line(line)
            self.output = Output
        return str(self.output)

