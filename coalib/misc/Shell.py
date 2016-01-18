from contextlib import contextmanager
import platform
from subprocess import Popen, PIPE

from coalib.parsing.StringProcessing import escape


def escape_path_argument(path, os=platform.system()):
    """
    Makes a raw path ready for using as parameter in a shell command (escapes
    illegal characters, surrounds with quotes etc.).

    :param path: The path to make ready for shell.
    :param os:   The shell platform to escape the path argument for. Possible
                 values are "Windows" and "Linux" (others will be ignored and
                 return the given path without modification).
    :return:     The escaped path argument.
    """
    if os == "Windows":
        # If a quote (") occurs in path (which is illegal for NTFS file
        # systems, but maybe for others), escape it by preceding it with
        # a caret (^).
        return '"' + escape(path, '"', '^') + '"'
    elif os == "Linux":
        return escape(path, " ")
    else:
        # Any other non-supported system doesn't get a path escape.
        return path


@contextmanager
def run_interactive_shell_command(command):
    """
    Runs a command in shell and provides stdout, stderr and stdin streams.

    This function creates a context manager that sets up the process, returns
    to caller, closes streams and waits for process to exit on leaving.

    The process is opened in `universal_newlines` mode.

    :param command: The command to run on shell.
    :return:        A context manager yielding the process started from the
                    command.
    """
    process = Popen(command,
                    shell=True,
                    stdout=PIPE,
                    stderr=PIPE,
                    stdin=PIPE,
                    universal_newlines=True)
    try:
        yield process
    finally:
        process.stdout.close()
        process.stderr.close()
        process.stdin.close()
        process.wait()
