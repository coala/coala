from coala_utils.Comparable import Comparable


def _assert_comparable_equal(observed_result, expected_result):
    """
    Compares individual fields of the result objects using
    `__compare_fields__` of `coala_utils.Comparable` class
    and yields messages in case of an attribute mismatch.
    """

    if not len(observed_result) == len(expected_result):
        assert observed_result == expected_result, '%s != %s' % (
            observed_result, expected_result)

    messages = ''
    for observed, expected in zip(observed_result, expected_result):
        if (isinstance(observed, Comparable) and
            isinstance(expected, Comparable)) and (type(observed) is
                                                   type(expected)):
            for attribute in type(observed).__compare_fields__:
                try:
                    assert getattr(observed, attribute) == getattr(
                        expected, attribute), (
                        '{} mismatch: {}, {} != {}, {}'.format(
                            attribute,
                            observed.origin, observed.message,
                            expected.origin, expected.message))
                except AssertionError as ex:
                    messages += (str(ex) + '\n\n')
        else:
            assert observed_result == expected_result, '%s != %s' % (
                observed_result, expected_result)

    if messages:
        raise AssertionError(messages)


class BaseTestHelper:
    """
    This is a base class for all Bears' tests of coala's testing API.
    """

    def assert_result_equal(self,
                            observed_result,
                            expected_result):
        """
        Asserts that an observed result from a bear is exactly same
        as the expected result from the bear.

        :param observed_result: The observed result from a bear
        :param expected_result: The expected result from a bear
        """

        return _assert_comparable_equal(observed_result, expected_result)
