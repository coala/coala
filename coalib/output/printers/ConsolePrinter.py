import platform
from pyprint.ColorPrinter import ColorPrinter


class ConsolePrinter(ColorPrinter):
    """
    A simple printer for the console that supports colors and logs.

    Note that pickling will not pickle the output member.
    """
    def __init__(self,
                 print_colored=platform.system() in ("Linux",)):
        ColorPrinter.__init__(self, print_colored)

    def _print_uncolored(self, output, **kwargs):
        print(output, end="")

    def _print_colored(self, output, color=None, **kwargs):
        color_code_dict = {
            'black': '0;30',
            'bright gray': '0;37',
            'blue': '0;34',
            'white': '1;37',
            'green': '0;32',
            'bright blue': '1;34',
            'cyan': '0;36',
            'bright green': '1;32',
            'red': '0;31',
            'bright cyan': '1;36',
            'purple': '0;35',
            'bright red': '1;31',
            'yellow': '0;33',
            'bright purple': '1;35',
            'dark gray': '1;30',
            'bright yellow': '1;33',
            'normal': '0'}
        try:
            color_code = color_code_dict[color]
        except KeyError:
            raise ValueError("Invalid color value.")

        print('\033[' + color_code + 'm' + output + '\033[0m', end="")
