from codeclib.internal.util import CONSOLE_COLOR, ColorPrinter

__author__ = 'lasse'


class OutputFormatter:
    def __init__(self, settings):
        self.settings = settings

    def output_file_results(self, filename, result_list):
        okcol = self.settings.get('fileokcolor').value
        badcol = self.settings.get('filebadcolor').value
        if len(result_list) == 0:
            ColorPrinter.ColorPrinter.print(okcol, filename)
            return

        for val in result_list:
            # TODO
            ColorPrinter.ColorPrinter.print(badcol, "UNIMPLEMENTED")

    def __output_line_result(self, line_result):
        # TODO
        pass
