from codeclib.internal.util import CONSOLE_COLOR, ColorPrinter

__author__ = 'lasse'


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
