from contextlib import contextmanager, closing
import sys
import os
from io import StringIO
import builtins
import copy


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
def suppress_stdout():
    """
    Suppresses everything going to stdout.
    """
    with open(os.devnull, "w") as devnull, replace_stdout(devnull):
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
        yield sio


@contextmanager
def simulate_console_inputs(*inputs):
    """
    Does some magic to simulate the given inputs to any calls to the `input`
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

    :param inputs: Any inputs to simulate. An IndexError will be raised if
                   input is called more often then the number of provided
                   inputs.
    """
    class InputGenerator:
        def __init__(self, inputs):
            self.last_input = -1
            self.inputs = inputs

        def generate_input(self, x=''):
            self.last_input += 1
            return self.inputs[self.last_input]

    input_generator = InputGenerator(list(inputs))
    _input = builtins.__dict__["input"]
    builtins.__dict__["input"] = input_generator.generate_input
    try:
        yield input_generator
    finally:
        builtins.__dict__["input"] = _input


@contextmanager
def preserve_sys_path():
    _path = copy.copy(sys.path)
    try:
        yield
    finally:
        sys.path = _path
