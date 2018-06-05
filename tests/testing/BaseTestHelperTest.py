import pytest

from coalib.results.Result import Result
from coalib.testing.BaseTestHelper import BaseTestHelper


class BaseTestHelperTest(BaseTestHelper):
    def test_good_assert_result_equal(self):
        self.assert_result_equal(['a', 'b'], ['a', 'b'])

    def test_inequality_assert_result_equal(self):
        with pytest.raises(AssertionError) as ex:
            self.assert_result_equal(['a', 'b'], ['a', 'b', None])
        assert '[\'a\', \'b\'] != [\'a\', \'b\', None]' in str(ex.value)

    def test_not_comparable_assert_result_equal(self):
        with pytest.raises(AssertionError) as ex:
            self.assert_result_equal(['a', 'b'], ['a', 'c'])
        assert '[\'a\', \'b\'] != [\'a\', \'c\']' in str(ex.value)

    def test_comparable_assert_result_equal(self):
        expected = [Result.from_values(origin='AnyBea',
                                       message='This file has 2 lines.',
                                       file='anyfile')]
        observed = [Result.from_values(origin='AnyBear',
                                       message='This file has 2 lines.',
                                       file='anyfile')]
        with pytest.raises(AssertionError) as ex:
            self.assert_result_equal(expected, observed)
        assert ('origin mismatch: AnyBea, This file has 2 lines. != AnyBear, '
                'This file has 2 lines.\n\n') == str(ex.value)
