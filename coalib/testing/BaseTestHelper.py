import unittest

from coala_utils.Comparable import Comparable


class BaseTestHelper(unittest.TestCase):
    """
    This is a base class for all Bears' tests of coala's testing API.
    """

    def _assert_comparable_equal(self,
                                 observed_result,
                                 expected_result):
        """
        Compares individual fields of the result objects using
        `__compare_fields__` of `coala_utils.Comparable` class
        and raises messages in case of an attribute mismatch.
        """

        if not len(observed_result) == len(expected_result):
            self.assertEqual(observed_result, expected_result)

        messages = []
        for observed, expected in zip(observed_result, expected_result):
            if (isinstance(observed, Comparable) and
                isinstance(expected, Comparable)) and (
                    Comparable.__eq__(expected, observed)):
                for attribute in observed.__compare_fields__:
                    try:
                        self.assertEqual(getattr(observed, attribute),
                                         getattr(expected, attribute),
                                         msg='{} mismatch.'.format(attribute))
                    except AssertionError as ex:
                        messages.append(str(ex))
            else:
                self.assertEqual(observed, expected)

        if messages:
            raise AssertionError('\n\n'.join(message for message in messages))

    def assert_result_equal(self,
                            observed_result,
                            expected_result):
        """
        Asserts that an observed result from a bear is exactly same
        as the expected result from the bear.

        :param observed_result: The observed result from a bear
        :param expected_result: The expected result from a bear
        """

        return self._assert_comparable_equal(observed_result, expected_result)
