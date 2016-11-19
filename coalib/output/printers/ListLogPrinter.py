from pyprint.Printer import Printer

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.printers.LogPrinter import LogPrinterMixin
from coalib.processes.communication.LogMessage import LogMessage


class ListLogPrinter(Printer, LogPrinterMixin):
    """
    A ListLogPrinter is a log printer which collects all LogMessages to a list
    so that the logs can be used at a later time.
    """

    def __init__(self,
                 log_level=LOG_LEVEL.WARNING,
                 timestamp_format='%X'):
        Printer.__init__(self)
        self.log_level = log_level

        self.logs = []

    def log_message(self, log_message, **kwargs):
        if not isinstance(log_message, LogMessage):
            raise TypeError('log_message should be of type LogMessage.')

        if log_message.log_level < self.log_level:
            return

        self.logs.append(log_message)

    def _print(self, output, **kwargs):
        self.info(output, **kwargs)
