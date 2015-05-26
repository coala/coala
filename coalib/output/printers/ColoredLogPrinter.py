from coalib.output.printers.ColorPrinter import ColorPrinter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL, LOG_LEVEL_COLORS
from coalib.output.printers.LogPrinter import LogPrinter


class ColoredLogPrinter(ColorPrinter, LogPrinter):
    def __init__(self,
                 log_level=LOG_LEVEL.WARNING,
                 timestamp_format="%X",
                 print_colored=True):
        ColorPrinter.__init__(self, print_colored=print_colored)
        LogPrinter.__init__(self, log_level, timestamp_format)

    def _print_log_message(self, prefix, log_message, **kwargs):
        """
        Override this if you want to influence how the log message is printed.
        """
        color = LOG_LEVEL_COLORS[log_message.log_level]
        self.print(prefix, end=" ", color=color, **kwargs)
        self.print(log_message.message, **kwargs)
