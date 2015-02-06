from coalib.misc.i18n import _
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL


class LogMessage:
    def __init__(self, log_level, message):
        if not log_level in [LOG_LEVEL.DEBUG, LOG_LEVEL.WARNING, LOG_LEVEL.ERROR]:
            raise ValueError("log_level has to be a valid LOG_LEVEL.")
        if message == "":
            raise ValueError("Empty log messages are not allowed.")

        self.log_level = log_level
        self.message = str(message).rstrip()

    def __str__(self):
        return '[{}] {}'.format({LOG_LEVEL.DEBUG: _("DEBUG"),
                                 LOG_LEVEL.WARNING: _("WARNING"),
                                 LOG_LEVEL.ERROR: _("ERROR")}.get(self.log_level, _("ERROR")), self.message)

    def __eq__(self, other):
        return isinstance(other, LogMessage) and other.log_level == self.log_level and other.message == self.message

    def __ne__(self, other):
        return not self.__eq__(other)
