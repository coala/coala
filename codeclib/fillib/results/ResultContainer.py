__author__ = 'fabian'
from functools import total_ordering


@total_ordering
class ResultContainer:

    def __init__(self, caption, settings, line_result_list=None, type='file'):
        self.settings = settings
        if line_result_list:
            self.line_result_list = sorted(line_result_list)
        else:
            self.line_result_list = []
        self.caption = caption
        if type == 'filter':
            self.type = type
            if self.__nonzero__():
                self.caption = self.line_result_list[0].filter_name
        else:
            self.type = 'file'
            if self.__nonzero__():
                self.caption = self.line_result_list[0].filename

    def add(self, line_result):

        self.line_result_list.append(line_result)
        self.line_result_list = sorted(self.line_result_list)
        if not self.caption:
            if self.type == 'filter':
                self.caption = self.line_result_list[0].filter_name
            else:
                self.caption = self.line_result_list[0].filename

    def __nonzero__(self):
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

        if not self.__nonzero__():
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
