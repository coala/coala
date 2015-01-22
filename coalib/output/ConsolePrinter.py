import sys

from coalib.output.ColorPrinter import ColorPrinter
from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.output.LogPrinter import LogPrinter


class ConsolePrinter(LogPrinter, ColorPrinter):
    def __init__(self, output=sys.stdout, log_level=LOG_LEVEL.WARNING, timestamp_format="%X"):
        ColorPrinter.__init__(self)
        LogPrinter.__init__(self, log_level=log_level, timestamp_format=timestamp_format)
        self.output = output

    def _print_uncolored(self, output, **kwargs):
        print(output, file=self.output, end="")

    def _print_colored(self, output, color=None, **kwargs):
        color_code_dict = {
            'black': '0;30', 'bright gray': '0;37',
            'blue': '0;34', 'white': '1;37',
            'green': '0;32', 'bright blue': '1;34',
            'cyan': '0;36', 'bright green': '1;32',
            'red': '0;31', 'bright cyan': '1;36',
            'purple': '0;35', 'bright red': '1;31',
            'yellow': '0;33', 'bright purple': '1;35',
            'dark gray': '1;30', 'bright yellow': '1;33',
            'normal': '0',
        }
        color_code = color_code_dict.get(color, None)
        if color_code is None:
            raise ValueError("Invalid color value")

        print('\033[' + color_code + 'm' + output + '\033[0m', file=self.output, end="")
