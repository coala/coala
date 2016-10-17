import logging
from pkg_resources import VersionConflict

from pyprint.NullPrinter import NullPrinter

from coalib.misc import Constants


def get_exitcode(exception):

    if isinstance(exception, KeyboardInterrupt):  # Ctrl+C
        print("Program terminated by user.")
        exitcode = 130
    elif isinstance(exception, EOFError):  # Ctrl+D
        print("Found EOF. Exiting gracefully.")
        exitcode = 0
    elif isinstance(exception, SystemExit):
        exitcode = exception.code
    elif isinstance(exception, VersionConflict):
        logging.exception(Constants.VERSION_CONFLICT_MESSAGE %
                          str(exception.req))
        exitcode = 13
    elif isinstance(exception, BaseException):
        logging.exception(Constants.CRASH_MESSAGE)
        exitcode = 255
    else:
        exitcode = 0

    return exitcode
