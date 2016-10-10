from pyprint.Printer import Printer

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.processes.communication.LogMessage import LogMessage


class ListLogPrinter(Printer, LogPrinter):
    """
    A ListLogPrinter is a log printer which collects all LogMessages to a list
    so that the logs can be used at a later time.
    """

    def __init__(self,
                 log_level=LOG_LEVEL.WARNING,
                 timestamp_format="%X"):
        Printer.__init__(self)
        LogPrinter.__init__(self, self, log_level, timestamp_format)

        self.logs = []

    def _print_log_message(self, prefix, log_message, **kwargs):
        self.logs.append(log_message)

    def _print(self, output, **kwargs):
        self.info(output, **kwargs)
