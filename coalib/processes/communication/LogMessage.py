from coalib.misc.i18n import _
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL


class LogMessage:
    def __init__(self, log_level, *messages, delimiter=" "):
        if log_level not in LOG_LEVEL.reverse:
            raise ValueError("log_level has to be a valid LOG_LEVEL.")

        str_messages = [str(message) for message in messages]
        self.message = str(delimiter).join(str_messages).rstrip()
        if self.message == "":
            raise ValueError("Empty log messages are not allowed.")

        self.log_level = log_level

    def __str__(self):
        log_level = _(LOG_LEVEL.reverse.get(self.log_level, "ERROR"))
        return '[{}] {}'.format(log_level, self.message)

    def __eq__(self, other):
        return (isinstance(other, LogMessage) and
                other.log_level == self.log_level and
                other.message == self.message)

    def __ne__(self, other):
        return not self.__eq__(other)
