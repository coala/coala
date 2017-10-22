from contextlib import contextmanager
import platform
import shlex
from subprocess import PIPE, Popen
from shutil import which


class ShellCommandResult(tuple):
    """
    The result of a :func:`coalib.misc.run_shell_command` call.

    It is based on a ``(stdout, stderr)`` string tuple like it is returned
    form ``subprocess.Popen.communicate`` and was originally returned from
    :func:`coalib.misc.run_shell_command`. So it is backwards-compatible.

    It additionally stores the return ``.code``:

    >>> process = Popen(['python', '-c',
    ...                  'import sys; print(sys.stdin.readline().strip() +'
    ...                  '                  " processed")'],
    ...                 stdin=PIPE, stdout=PIPE, stderr=PIPE,
    ...                 universal_newlines=True)

    >>> stdout, stderr = process.communicate(input='data')
    >>> stderr
    ''
    >>> result = ShellCommandResult(process.returncode, stdout, stderr)
    >>> result[0]
    'data processed\\n'
    >>> result[1]
    ''
    >>> result.code
    0
    """

    def __new__(cls, code, stdout, stderr):
        """
        Creates the basic tuple from `stdout` and `stderr`.
        """
        return tuple.__new__(cls, (stdout, stderr))

    def __init__(self, code, stdout, stderr):
        """
        Stores the return `code`.
        """
        self.code = code


@contextmanager
def run_interactive_shell_command(command, **kwargs):
    """
    Runs a single command in shell and provides stdout, stderr and stdin
    streams.

    This function creates a context manager that sets up the process (using
    ``subprocess.Popen()``), returns to caller and waits for process to exit on
    leaving.

    By default the process is opened in ``universal_newlines`` mode and creates
    pipes for all streams (stdout, stderr and stdin) using ``subprocess.PIPE``
    special value. These pipes are closed automatically, so if you want to get
    the contents of the streams you should retrieve them before the context
    manager exits.

    >>> with run_interactive_shell_command(["echo", "TEXT"]) as p:
    ...     stdout = p.stdout
    ...     stdout_text = stdout.read()
    >>> stdout_text
    'TEXT\\n'
    >>> stdout.closed
    True

    Custom streams provided are not closed except of ``subprocess.PIPE``.

    >>> from tempfile import TemporaryFile
    >>> stream = TemporaryFile()
    >>> with run_interactive_shell_command(["echo", "TEXT"],
    ...                                    stdout=stream) as p:
    ...     stderr = p.stderr
    >>> stderr.closed
    True
    >>> stream.closed
    False

    :param command: The command to run on shell. This parameter can either
                    be a sequence of arguments that are directly passed to
                    the process or a string. A string gets splitted beforehand
                    using ``shlex.split()``. If providing ``shell=True`` as a
                    keyword-argument, no ``shlex.split()`` is performed and the
                    command string goes directly to ``subprocess.Popen()``.
    :param kwargs:  Additional keyword arguments to pass to
                    ``subprocess.Popen`` that are used to spawn the process.
    :return:        A context manager yielding the process started from the
                    command.
    """
    if not kwargs.get('shell', False) and isinstance(command, str):
        command = shlex.split(command)
    else:
        command = list(command)

    if platform.system() == 'Windows':  # pragma: no cover
        # subprocess doesn't implicitly look for .bat and .cmd scripts when
        # running commands under Windows
        command[0] = which(command[0])

    args = {'stdout': PIPE,
            'stderr': PIPE,
            'stdin': PIPE,
            'universal_newlines': True}
    args.update(kwargs)

    process = Popen(command, **args)
    try:
        yield process
    finally:
        if args['stdout'] is PIPE:
            process.stdout.close()
        if args['stderr'] is PIPE:
            process.stderr.close()
        if args['stdin'] is PIPE:
            process.stdin.close()

        process.wait()


def run_shell_command(command, stdin=None, **kwargs):
    """
    Runs a single command in shell and returns the read stdout and stderr data.

    This function waits for the process (created using ``subprocess.Popen()``)
    to exit. Effectively it wraps ``run_interactive_shell_command()`` and uses
    ``communicate()`` on the process.

    See also ``run_interactive_shell_command()``.

    :param command: The command to run on shell. This parameter can either
                    be a sequence of arguments that are directly passed to
                    the process or a string. A string gets splitted beforehand
                    using ``shlex.split()``.
    :param stdin:   Initial input to send to the process.
    :param kwargs:  Additional keyword arguments to pass to
                    ``subprocess.Popen`` that is used to spawn the process.
    :return:        A tuple with ``(stdoutstring, stderrstring)``.
    """
    with run_interactive_shell_command(command, **kwargs) as p:
        ret = p.communicate(stdin)
    return ShellCommandResult(p.returncode, *ret)
