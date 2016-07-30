import logging

from pyprint.ColorPrinter import ColorPrinter

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL_COLORS
from coalib.processes.communication.LogMessage import LogMessage


class LogPrinter:
    """
    The LogPrinter class allows to print log messages to an underlying Printer.

    This class is an adapter, means you can create a LogPrinter from every
    existing Printer instance.
    """

    def __init__(self,
                 printer,
                 log_level=LOG_LEVEL.INFO,
                 timestamp_format="%X"):
        """
        Creates a new log printer from an existing Printer.

        :param printer:          The underlying Printer where log messages
                                 shall be written to. If you inherit from
                                 LogPrinter, set it to self.
        :param log_level:        The minimum log level, everything below will
                                 not be logged.
        :param timestamp_format: The format string for the
                                 datetime.today().strftime(format) method.
        """
        self._printer = printer
        self.log_level = log_level
        self.timestamp_format = timestamp_format

    @property
    def printer(self):
        """
        Returns the underlying printer where logs are printed to.
        """
        return self._printer

    def _get_log_prefix(self, log_level, timestamp):
        datetime_string = timestamp.strftime(self.timestamp_format)

        if datetime_string != "":
            datetime_string = "[" + datetime_string + "]"

        return '[{}]{}'.format(LOG_LEVEL.reverse.get(log_level, "ERROR"),
                               datetime_string)

    def debug(self, *messages, delimiter=" ", timestamp=None, **kwargs):
        logging.debug(self._compile_message(*messages, delimiter=delimiter))

    def info(self, *messages, delimiter=" ", timestamp=None, **kwargs):
        logging.info(self._compile_message(*messages, delimiter=delimiter))

    def warn(self, *messages, delimiter=" ", timestamp=None, **kwargs):
        logging.warning(self._compile_message(*messages, delimiter=delimiter))

    def err(self, *messages, delimiter=" ", timestamp=None, **kwargs):
        logging.error(self._compile_message(*messages, delimiter=delimiter))

    def _compile_message(self, *messages, delimiter):
        return str(delimiter).join(str(message)
                                   for message in messages).rstrip()

    def log_exception(self,
                      message,
                      exception: BaseException,
                      log_level=LOG_LEVEL.ERROR,
                      timestamp=None,
                      **kwargs):
        """
        If the log_level of the printer is greater than DEBUG, it prints
        only the message. If it is DEBUG or lower, it shows the message
        along with the traceback of the exception.

        :param message:   The message to print.
        :param exception: The exception to print.
        :param log_level: The log_level of this message (not used when
                          logging the traceback. Tracebacks always have
                          a level of DEBUG).
        :param timestamp: The time at which this log occured. Defaults to
                          the current time.
        :param kwargs:    Keyword arguments to be passed when logging the
                          message (not used when logging the traceback).
        """
        if not isinstance(exception, BaseException):
            raise TypeError("log_exception can only log derivatives of "
                            "BaseException.")

        logging.exception(message, exc_info=exception)
