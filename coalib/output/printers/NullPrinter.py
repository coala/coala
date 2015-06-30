from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.ColorPrinter import ColorPrinter


class NullPrinter(ColorPrinter, LogPrinter):
    def __init__(self):
        ColorPrinter.__init__(self)
        LogPrinter.__init__(self)

    def print(self, *args, **kwargs):
        return

    def log_message(self, log_message, timestamp=None, **kwargs):
        return
