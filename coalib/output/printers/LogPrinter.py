import traceback
from pyprint.ColorPrinter import ColorPrinter

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL, LOG_LEVEL_COLORS
from coalib.misc.i18n import _
from coalib.processes.communication.LogMessage import LogMessage


class LogPrinter:
    """
    The LogPrinter class allows to print log messages to an underlying Printer.

    This class is an adapter, means you can create a LogPrinter from every
    existing Printer instance.
    """
    def __init__(self,
                 printer,
                 log_level=LOG_LEVEL.WARNING,
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

        return '[{}]{}'.format(_(LOG_LEVEL.reverse.get(log_level, "ERROR")),
                                datetime_string)

    def debug(self, *messages, delimiter=" ", timestamp=None, **kwargs):
        self.log_message(LogMessage(LOG_LEVEL.DEBUG,
                                    *messages,
                                    delimiter=delimiter,
                                    timestamp=timestamp),
                         **kwargs)

    def info(self, *messages, delimiter=" ", timestamp=None, **kwargs):
        self.log_message(LogMessage(LOG_LEVEL.INFO,
                                    *messages,
                                    delimiter=delimiter,
                                    timestamp=timestamp),
                         **kwargs)

    def warn(self, *messages, delimiter=" ", timestamp=None, **kwargs):
        self.log_message(LogMessage(LOG_LEVEL.WARNING,
                                    *messages,
                                    delimiter=delimiter,
                                    timestamp=timestamp),
                         **kwargs)

    def err(self, *messages, delimiter=" ", timestamp=None, **kwargs):
        self.log_message(LogMessage(LOG_LEVEL.ERROR,
                                    *messages,
                                    delimiter=delimiter,
                                    timestamp=timestamp),
                         **kwargs)

    def log(self, log_level, message, timestamp=None, **kwargs):
        self.log_message(LogMessage(log_level,
                                    message,
                                    timestamp=timestamp),
                         **kwargs)

    def log_exception(self,
                      message,
                      exception,
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

        traceback_str = "\n".join(
            traceback.format_exception(type(exception),
                                       exception,
                                       exception.__traceback__))

        self.log(log_level, message, timestamp=timestamp, **kwargs)
        self.log_message(
            LogMessage(LOG_LEVEL.DEBUG,
                       _("Exception was:") + "\n" + traceback_str,
                       timestamp=timestamp),
            **kwargs)

    def log_message(self, log_message, **kwargs):
        if not isinstance(log_message, LogMessage):
            raise TypeError("log_message should be of type LogMessage.")

        if log_message.log_level < self.log_level:
            return

        self._print_log_message(
            self._get_log_prefix(log_message.log_level, log_message.timestamp),
            log_message,
            **kwargs)

    def _print_log_message(self, prefix, log_message, **kwargs):
        """
        Override this if you want to influence how the log message is printed.

        If the underlying printer is a ColorPrinter, then colored logging is
        used. You can turn it off in the underlying ColorPrinter if you want to
        print uncolored.

        :param prefix:      The prefix to print (as string).
        :param log_message: The LogMessage object to print.
        :param kwargs:      Any other keyword arguments.
        """
        if isinstance(self._printer, ColorPrinter):
            self.printer.print(prefix,
                               end=" ",
                               color=LOG_LEVEL_COLORS[log_message.log_level],
                               **kwargs)
            self.printer.print(log_message.message, **kwargs)
        else:
            self.printer.print(prefix, log_message.message, **kwargs)
