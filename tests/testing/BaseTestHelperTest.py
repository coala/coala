from coalib.results.Result import Result
from coalib.testing.BaseTestHelper import BaseTestHelper


class BaseTestHelperTest(BaseTestHelper):
    def test_good_assert_result_equal(self):
        self.assert_result_equal(['a', 'b'], ['a', 'b'])

    def test_inequality_assert_result_equal(self):
        with self.assertRaises(AssertionError) as ex:
            self.assert_result_equal(['a', 'b'], ['a', 'b', None])
        self.assertEqual("Lists differ: ['a', 'b'] != ['a', 'b', None]\n\n"
                         'Second list contains 1 additional elements.\n'
                         'First extra element 2:\n'
                         'None\n\n'
                         "- ['a', 'b']\n"
                         "+ ['a', 'b', None]\n"
                         '?          ++++++\n', str(ex.exception))

    def test_not_comparable_assert_result_equal(self):
        with self.assertRaises(AssertionError) as ex:
            self.assert_result_equal(['a', 'b'], ['a', 'c'])
        self.assertEqual("'b' != 'c'\n"
                         '- b\n'
                         '+ c\n', str(ex.exception))

    def test_comparable_assert_result_equal(self):
        expected = [Result.from_values(origin='AnyBea',
                                       message='This file has 2 lines.',
                                       file='anyfile')]
        observed = [Result.from_values(origin='AnyBear',
                                       message='This file has 3 lines.',
                                       file='anyfile')]
        with self.assertRaises(AssertionError) as ex:
            self.assert_result_equal(expected, observed)
        self.assertEqual("'AnyBea' != 'AnyBear'\n"
                         '- AnyBea\n'
                         '+ AnyBear\n'
                         '?       +\n'
                         ' : origin mismatch.\n\n'
                         "'This file has 2 lines.' != 'This file "
                         "has 3 lines.'\n"
                         '- This file has 2 lines.\n'
                         '?               ^\n'
                         '+ This file has 3 lines.\n'
                         '?               ^\n'
                         ' : message_base mismatch.', str(ex.exception))
