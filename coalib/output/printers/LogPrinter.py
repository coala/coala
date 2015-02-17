from datetime import datetime
import traceback

from coalib.output.printers.Printer import Printer
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.misc.i18n import _
from coalib.processes.communication.LogMessage import LogMessage


class LogPrinter(Printer):
    def __init__(self, log_level=LOG_LEVEL.WARNING, timestamp_format="%X"):
        """
        Creates a new log printer. The log printer adds logging capabilities to
        any normal printer, just derive from this class and you should have
        this logging capabilities for free. (Note: LogPrinter itself is
        abstract.)

        :param log_level: The minimum log level, everything below will not be
        logged.
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

        return '[{}]{} '.format(_(LOG_LEVEL.reverse.get(log_level, "ERROR")),
                                datetime_string)

    def debug(self, message, timestamp=None, **kwargs):
        return self.log_message(LogMessage(LOG_LEVEL.DEBUG, message),
                                timestamp=timestamp,
                                **kwargs)

    def warn(self, message, timestamp=None, **kwargs):
        return self.log_message(LogMessage(LOG_LEVEL.WARNING, message),
                                timestamp=timestamp,
                                **kwargs)

    def err(self, message, timestamp=None, **kwargs):
        return self.log_message(LogMessage(LOG_LEVEL.ERROR, message),
                                timestamp=timestamp,
                                **kwargs)

    def log(self, log_level, message, timestamp=None, **kwargs):
        return self.log_message(LogMessage(log_level, message),
                                timestamp=timestamp,
                                **kwargs)

    def log_exception(self,
                      message,
                      exception,
                      log_level=LOG_LEVEL.ERROR,
                      timestamp=None,
                      **kwargs):
        if not isinstance(exception, BaseException):
            raise TypeError("log_exception can only log derivatives of "
                            "BaseException.")

        traceback_str = "\n".join(
            traceback.format_exception(type(exception),
                                       exception,
                                       exception.__traceback__))

        return self.log_message(
            LogMessage(log_level,
                       message + "\n\n" +
                       _("Exception was:") + "\n" + traceback_str),
            timestamp=timestamp,
            **kwargs)

    def log_message(self, log_message, timestamp=None, **kwargs):
        if not isinstance(log_message, LogMessage):
            raise TypeError("log_message should be of type LogMessage.")

        if log_message.log_level < self.log_level:
            return

        if not isinstance(timestamp, datetime):
            timestamp = datetime.today()

        prefix = self._get_log_prefix(log_message.log_level, timestamp)
        return self.print(prefix, log_message.message, delimiter="", **kwargs)
