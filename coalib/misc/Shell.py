from contextlib import contextmanager
import functools
import shlex
from subprocess import PIPE, Popen, call, DEVNULL


call_without_output = functools.partial(call, stdout=DEVNULL, stderr=DEVNULL)
"""
Uses subprocess.call to execute a command, but suppresses the output and
the errors.
"""


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
    return ret


def get_shell_type():  # pragma: no cover
    """
    Finds the current shell type based on the outputs of common pre-defined
    variables in them. This is useful to identify which sort of escaping
    is required for strings.

    :return: The shell type. This can be either "powershell" if Windows
             Powershell is detected, "cmd" if command prompt is been
             detected or "sh" if it's neither of these.
    """
    out = run_shell_command('echo $host.name', shell=True)[0]
    if out.strip() == 'ConsoleHost':
        return 'powershell'
    out = run_shell_command('echo $0', shell=True)[0]
    if out.strip() == '$0':
        return 'cmd'
    return 'sh'
