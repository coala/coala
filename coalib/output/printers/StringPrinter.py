from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.printers.LogPrinter import LogPrinter


class StringPrinter(LogPrinter):
    """
    This is a simple printer that prints everything to a string.
    """

    def __init__(self, log_level=LOG_LEVEL.WARNING, timestamp_format="%X"):
        """
        Creates a new StringPrinter with an empty print string.

        :param log_level:        The minimum log level, everything below will
                                 not be logged.
        :param timestamp_format: The format string for the
                                 datetime.today().strftime(format) method.
        """
        LogPrinter.__init__(self, log_level, timestamp_format)

        self._string = ""

    def _print(self, output, **kwargs):
        self._string += output

    def clear(self):
        """
        Clears the print string.
        """
        self._string = ""

    @property
    def string(self):
        """
        Gets the print string.
        """
        return self._string
