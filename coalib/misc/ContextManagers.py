import builtins
import os
import platform
import signal
import sys
import tempfile
import threading
from contextlib import closing, contextmanager
from io import StringIO

from coalib.misc.MutableValue import MutableValue


@contextmanager
def subprocess_timeout(sub_process, seconds, kill_pg=False):
    """
    Kill subprocess if the sub process takes more the than the timeout.

    :param sub_process: The sub process to run.
    :param seconds:     The number of seconds to allow the test to run for. If
                        set to 0 or a negative value, it waits indefinitely.
                        Floats can be used to specify units smaller than
                        seconds.
    :param kill_pg:     Boolean whether to kill the process group or only this
                        process. (not applicable for windows)
    """
    timedout = MutableValue(False)

    if seconds <= 0:
        yield timedout
        return

    finished = threading.Event()

    if platform.system() == 'Windows':  # pragma: no cover
        kill_pg = False

    def kill_it():
        finished.wait(seconds)
        if not finished.is_set():
            timedout.value = True
            if kill_pg:
                pgid = os.getpgid(sub_process.pid)
            os.kill(sub_process.pid, signal.SIGINT)
            if kill_pg:
                os.killpg(pgid, signal.SIGINT)

    thread = threading.Thread(name='timeout-killer', target=kill_it)
    try:
        thread.start()
        yield timedout
    finally:
        finished.set()
        thread.join()


@contextmanager
def replace_stdout(replacement):
    """
    Replaces stdout with the replacement, yields back to the caller and then
    reverts everything back.
    """
    _stdout = sys.stdout
    sys.stdout = replacement
    try:
        yield
    finally:
        sys.stdout = _stdout


@contextmanager
def replace_stderr(replacement):
    """
    Replaces stderr with the replacement, yields back to the caller and then
    reverts everything back.
    """
    _stderr = sys.stderr
    sys.stderr = replacement
    try:
        yield
    finally:
        sys.stderr = _stderr


@contextmanager
def suppress_stdout():
    """
    Suppresses everything going to stdout.
    """
    with open(os.devnull, 'w') as devnull, replace_stdout(devnull):
        yield


@contextmanager
def retrieve_stdout():
    """
    Yields a StringIO object from which one can read everything that was
    printed to stdout. (It won't be printed to the real stdout!)

    Example usage:

    with retrieve_stdout() as stdout:
        print("something")  # Won't print to the console
        what_was_printed = stdout.getvalue()  # Save the value
    """
    with closing(StringIO()) as sio, replace_stdout(sio):
        oldprint = builtins.print
        try:
            # Overriding stdout doesn't work with libraries, this ensures even
            # cached variables take this up. Well... it works.
            def newprint(*args, **kwargs):
                kwargs['file'] = sio
                oldprint(*args, **kwargs)

            builtins.print = newprint
            yield sio
        finally:
            builtins.print = oldprint


@contextmanager
def retrieve_stderr():
    """
    Yields a StringIO object from which one can read everything that was
    printed to stderr. (It won't be printed to the real stderr!)

    Example usage:

    with retrieve_stderr() as stderr:
        print("something")  # Won't print to the console
        what_was_printed = stderr.getvalue()  # Save the value
    """
    with closing(StringIO()) as sio, replace_stderr(sio):
        oldprint = builtins.print
        try:
            # Overriding stderr doesn't work with libraries, this ensures even
            # cached variables take this up. Well... it works.
            def newprint(*args, **kwargs):
                kwargs['file'] = sio
                oldprint(*args, **kwargs)

            builtins.print = newprint
            yield sio
        finally:
            builtins.print = oldprint


@contextmanager
def simulate_console_inputs(*inputs):
    """
    Does some magic to simulate the given inputs to any calls to the ``input``
    builtin. This yields back an InputGenerator object so you can check
    which input was already used and append any additional inputs you want.
    Example:

        with simulate_console_inputs(0, 1, 2) as generator:
            assert(input() == 0)
            assert(generator.last_input == 0)
            generator.inputs.append(3)
            assert(input() == 1)
            assert(input() == 2)
            assert(input() == 3)
            assert(generator.last_input == 3)

    :param inputs:      Any inputs to simulate.
    :raises ValueError: Raised when was asked for more input but there's no
                        more provided.
    """
    class InputGenerator:

        def __init__(self, inputs):
            self.last_input = -1
            self.inputs = inputs

        def generate_input(self, prompt=''):
            print(prompt, end='')
            self.last_input += 1
            try:
                return self.inputs[self.last_input]
            except IndexError:
                raise ValueError('Asked for more input, but no more was '
                                 'provided from `simulate_console_inputs`.')

    input_generator = InputGenerator(list(inputs))
    _input = builtins.input
    builtins.input = input_generator.generate_input
    try:
        yield input_generator
    finally:
        builtins.input = _input


@contextmanager
def make_temp(suffix='', prefix='tmp', dir=None):
    """
    Creates a temporary file with a closed stream and deletes it when done.

    :return: A contextmanager retrieving the file path.
    """
    temporary = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    os.close(temporary[0])
    try:
        yield temporary[1]
    finally:
        os.remove(temporary[1])


@contextmanager
def prepare_file(lines,
                 filename,
                 force_linebreaks=True,
                 create_tempfile=True,
                 tempfile_kwargs={}):
    """
    Can create a temporary file (if filename is None) with the lines.
    Can also add a trailing newline to each line specified if needed.

    :param lines:            The lines from the file. (list or tuple of strings)
    :param filename:         The filename to be prepared.
    :param force_linebreaks: Whether to append newlines at each line if needed.
    :param create_tempfile:  Whether to save lines in tempfile if needed.
    :param tempfile_kwargs:  Kwargs passed to tempfile.mkstemp().
    """
    if force_linebreaks:
        lines = type(lines)(line if line.endswith('\n') else line+'\n'
                            for line in lines)

    if not create_tempfile and filename is None:
        filename = 'dummy_file_name'

    if not isinstance(filename, str) and create_tempfile:
        with make_temp(**tempfile_kwargs) as filename:
            with open(filename, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            yield lines, filename
    else:
        yield lines, filename


@contextmanager
def change_directory(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)
