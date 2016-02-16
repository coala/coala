import sys

from coalib.misc.ContextManagers import retrieve_stdout


def execute_coala(func, binary, *args):
    """
    Executes the main function with the given argument string from given module.

    :param function: A main function from coala_json, coala_ci module etc.
    :param binary:   A binary to execute coala test
    :return:         A tuple holding a return value first and
                     a stdout output as second element.
    """
    sys.argv = [binary] + list(args)
    with retrieve_stdout() as stdout:
        retval = func()
        return retval, stdout.getvalue()
