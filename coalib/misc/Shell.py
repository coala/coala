from contextlib import contextmanager
import platform
from subprocess import Popen, PIPE

from coalib.parsing.StringProcessing import escape


def prepare_string_argument(string, os=platform.system()):
    """
    Prepares a string argument for being passed as a parameter on shell.

    On Linux and Darwin this function effectively encloses the given string
    with quotes (either '' or "", depending on content).

    :param string: The string to prepare for shell.
    :param os:     The shell platform to prepare string argument for. Possible
                   "Linux" and "Darwin" (others will be ignored and return the
                   given string without modification).
    :return:       The shell-prepared string.
    """
    if os == "Linux" or os == "Darwin":
        return '"' + escape(string, '"') + '"'
    else:
        return string


def escape_path_argument(path, os=platform.system()):
    """
    Makes a raw path ready for using as parameter in a shell command (escapes
    illegal characters, surrounds with quotes etc.).

    :param path: The path to make ready for shell.
    :param os:   The shell platform to escape the path argument for. Possible
                 values are "Windows", "Linux" and "Darwin" (others will be
                 ignored and return the given path without modification).
    :return:     The escaped path argument.
    """
    if os == "Windows":
        # If a quote (") occurs in path (which is illegal for NTFS file
        # systems, but maybe for others), escape it by preceding it with
        # a caret (^).
        return '"' + escape(path, '"', '^') + '"'
    elif os == "Linux" or os == "Darwin":
        return escape(path, " ")
    else:
        # Any other non-supported system doesn't get a path escape.
        return path


@contextmanager
def run_interactive_shell_command(command, **kwargs):
    """
    Runs a command in shell and provides stdout, stderr and stdin streams.

    This function creates a context manager that sets up the process, returns
    to caller, closes streams and waits for process to exit on leaving.

    The process is opened in `universal_newlines` mode.

    :param command: The command to run on shell.
    :param kwargs:  Additional keyword arguments to pass to `subprocess.Popen`
                    that is used to spawn the process (except `shell`,
                    `stdout`, `stderr`, `stdin` and `universal_newlines`, a
                    `TypeError` is raised then).
    :return:        A context manager yielding the process started from the
                    command.
    """
    process = Popen(command,
                    shell=True,
                    stdout=PIPE,
                    stderr=PIPE,
                    stdin=PIPE,
                    universal_newlines=True,
                    **kwargs)
    try:
        yield process
    finally:
        process.stdout.close()
        process.stderr.close()
        process.stdin.close()
        process.wait()


def run_shell_command(command, stdin=None, **kwargs):
    """
    Runs a command in shell and returns the read stdout and stderr data.

    This function waits for the process to exit.

    :param command: The command to run on shell.
    :param stdin:   Initial input to send to the process.
    :param kwargs:  Additional keyword arguments to pass to `subprocess.Popen`
                    that is used to spawn the process (except `shell`,
                    `stdout`, `stderr`, `stdin` and `universal_newlines`, a
                    `TypeError` is raised then).
    :return:        A tuple with `(stdoutstring, stderrstring)`.
    """
    with run_interactive_shell_command(command, **kwargs) as p:
        ret = p.communicate(stdin)
    return ret
