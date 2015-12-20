from pyprint.NullPrinter import NullPrinter

from coalib.output.printers.LogPrinter import LogPrinter
from coalib.misc.Constants import Constants


def get_exitcode(exception, log_printer=None):
    log_printer = log_printer or LogPrinter(NullPrinter())

    if isinstance(exception, KeyboardInterrupt):  # Ctrl+C
        print("Program terminated by user.")
        exitcode = 130
    elif isinstance(exception, EOFError):  # Ctrl+D
        print("Found EOF. Exiting gracefully.")
        exitcode = 0
    elif isinstance(exception, SystemExit):
        exitcode = exception.code
    elif isinstance(exception, BaseException):
        log_printer.log_exception(Constants.CRASH_MESSAGE, exception)
        exitcode = 255
    else:
        exitcode = 0

    return exitcode
