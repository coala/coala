__author__ = 'fabian'
from functools import total_ordering
import os

@total_ordering
class ResultContainer:

    @staticmethod
    def fixed_length(str, length):
        assert(length > 4)
        if len(str) < length:
            str += ' '*(length-len(str))
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

    def get_replacement_line_results(self):
        possible_changes = []
        for LineResult in self.line_result_list:
            if LineResult.replacement:
                possible_changes.append(LineResult)
        return possible_changes

    def add(self, line_result):
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
        FileOkColor = self.settings['fileokcolor'].to_color_code(0)
        FileBadColor = self.settings['filebadcolor'].to_color_code(0)
        FilterColor = self.settings['filtercolor'].to_color_code(0)
        NormalColor = '\033[0m'

        str = ""

        if not bool(self):
            str += FileOkColor + self.caption + NormalColor
        else:
            str += FileBadColor + self.caption + NormalColor + '\n'
            if self.type == 'file':
                for i in range(len(self.line_result_list)):
                    str += "\t"+FilterColor+self.line_result_list[i].filter_name+': '+NormalColor\
                           +"line {}: ".format(self.line_result_list[i].line_number)\
                           +self.line_result_list[i].error_message
                    if i < len(self.line_result_list)-1:
                        str += '\n'
            else:  # type = 'filter'
                for i in range(len(self.line_result_list)):
                    str += "\t"+FilterColor+self.line_result_list[i].filename+': '+NormalColor\
                           +"line {}: ".format(self.line_result_list[i].line_number)\
                           +self.line_result_list[i].error_message
                    if i < len(self.line_result_list)-1:
                        str += '\n'

        return str
