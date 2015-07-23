import traceback

from coalib.output.printers.Printer import Printer
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.misc.i18n import _
from coalib.processes.communication.LogMessage import LogMessage


class LogPrinter(Printer):
    """
    The LogPrinter class is a Printer that provides logging features.

    To use these logging features in your custom printer, just inherit this
    class.
    """
    def __init__(self, log_level=LOG_LEVEL.WARNING, timestamp_format="%X"):
        """
        Creates a new log printer. The log printer adds logging capabilities to
        any normal printer, just derive from this class and you should have
        this logging capabilities for free. (Note: LogPrinter itself is
        abstract.)

        :param log_level:        The minimum log level, everything below will
                                 not be logged.
        :param timestamp_format: The format string for the
                                 datetime.today().strftime(format) method.
        """
        Printer.__init__(self)

        self.log_level = log_level
        self.timestamp_format = timestamp_format

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

        :param prefix:      The prefix to print (as string).
        :param log_message: The LogMessage object to print.
        :param kwargs:      Any other keyword arguments.
        """
        self.print(prefix, log_message.message, **kwargs)
