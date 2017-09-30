import logging
import traceback

from coalib.misc import Constants
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL

from pkg_resources import VersionConflict


def get_exitcode(exception, log_printer=None):
    if isinstance(exception, KeyboardInterrupt):  # Ctrl+C
        print('Program terminated by user.')
        exitcode = 130
    elif isinstance(exception, EOFError):  # Ctrl+D
        print('Found EOF. Exiting gracefully.')
        exitcode = 0
    elif isinstance(exception, SystemExit):
        exitcode = exception.code
    elif isinstance(exception, VersionConflict):
        log_message = Constants.VERSION_CONFLICT_MESSAGE % str(exception.req)
        log_exception(log_message, exception)
        exitcode = 13
    elif isinstance(exception, BaseException):
        log_exception(Constants.CRASH_MESSAGE, exception)
        exitcode = 255
    else:
        exitcode = 0

    return exitcode


def log_exception(message, exception, log_level=LOG_LEVEL.ERROR):
    logging.log(log_level, message)
    traceback_str = '\n'.join(
        traceback.format_exception(type(exception),
                                   exception,
                                   exception.__traceback__))
    logging.info('Exception was:\n' + traceback_str)
