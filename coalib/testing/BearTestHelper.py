from unittest.case import skip, skipIf


def generate_skip_decorator(bear):
    """
    Creates a skip decorator for a `unittest` module test from a bear.

    `check_prerequisites` is used to determine a test skip.

    :param bear: The bear whose prerequisites determine the test skip.
    :return:     A decorator that skips the test if appropriate.
    """
    result = bear.check_prerequisites()

    return (skip(result) if isinstance(result, str)
            else skipIf(not result, '(No reason given.)'))
