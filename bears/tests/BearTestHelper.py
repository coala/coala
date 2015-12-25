def generate_skip_test(bear):
    """
    Creates a skip_test function for a `unittest` module test from a bear.

    `check_prerequisites` is used to determine a test skip.

    :param bear: The bear whose prerequisites determine the test skip.
    """
    def skip_bear_test():
        result = bear.check_prerequisites()
        return result if isinstance(result, str) else not result

    return skip_bear_test
