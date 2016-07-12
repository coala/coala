import traceback
import logging

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.processes.communication.LogMessage import LogMessage


class LogPrinterMixin:
    """
    Provides access to the logging interfaces (e.g. err, warn, info) by routing
    them to the log_message method, which should be implemented by descendants
    of this class.
    """

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
        :param timestamp: The time at which this log occurred. Defaults to
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
            LogMessage(LOG_LEVEL.INFO,
                       "Exception was:" + "\n" + traceback_str,
                       timestamp=timestamp),
            **kwargs)

    def log_message(self, log_message, **kwargs):
        """
        It is your reponsibility to implement this method, if you're using this
        mixin.
        """
        raise NotImplementedError


class LogPrinter(LogPrinterMixin):
    """
    This class is deprecated and will be soon removed. To get logger use
    logging.getLogger(__name__). Make sure that you're getting it when the
    logging configuration is loaded.

    The LogPrinter class allows to print log messages to an underlying Printer.

    This class is an adapter, means you can create a LogPrinter from every
    existing Printer instance.
    """

    def __init__(self,
                 printer=None,
                 log_level=LOG_LEVEL.DEBUG,
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
        self.logger = logging.getLogger()

        self._printer = printer
        self.log_level = log_level
        self.timestamp_format = timestamp_format

    @property
    def log_level(self):
        """
        Returns current log_level used in logger.
        """
        return self.logger.getEffectiveLevel()

    @log_level.setter
    def log_level(self, log_level):
        """
        Sets log_level for logger.
        """
        self.logger.setLevel(log_level)

    @property
    def printer(self):
        """
        Returns the underlying printer where logs are printed to.
        """
        return self._printer

    def log_message(self, log_message, **kwargs):
        if not isinstance(log_message, LogMessage):
            raise TypeError("log_message should be of type LogMessage.")
        self.logger.log(log_message.log_level, log_message.message)

    def __getstate__(self):
        # on Windows there are problems with serializing loggers, so omit it
        oldict = self.__dict__.copy()
        del oldict['logger']
        return oldict

    def __setstate__(self, newdict):
        self.__dict__.update(newdict)
        # restore logger by name
        self.logger = logging.getLogger()
