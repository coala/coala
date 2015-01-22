from coalib.output.ColorPrinter import ColorPrinter
from coalib.output.LogPrinter import LogPrinter


class NullPrinter(ColorPrinter, LogPrinter):
    def __init__(self):
        ColorPrinter.__init__(self)
        LogPrinter.__init__(self)

    def print(self, *args, delimiter=' ', end='\n', **kwargs):
        return

    def log_message(self, log_message, timestamp=None, **kwargs):
        return
