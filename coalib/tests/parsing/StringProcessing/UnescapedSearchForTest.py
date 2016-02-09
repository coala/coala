import unittest

from coalib.tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)
from coalib.parsing.StringProcessing import unescaped_search_for


class UnescapedSearchForTest(StringProcessingTestBase):
    # Match either "out1" or "out2".
    test_basic_pattern = "out1|out2"
    # These are the expected results for the zero-group of the
    # returned MatchObject's.
    test_basic_expected_results = [
        [r"out1", r"out2"],
        [r"out1", r"out2"],
        [r"out1", r"out2"],
        [r"out1", r"out2"],
        [r"out1", r"out2"],
        [r"out1", r"out2"],
        [r"out1", r"out2", r"out2"],
        [r"out1", r"out2", r"out2"],
        [r"out1", r"out2", r"out2"],
        [r"out1", r"out2", r"out2"],
        [r"out1", r"out2", r"out2"],
        [r"out1", r"out2", r"out2"],
        [r"out1", r"out2", r"out2"],
        [r"out1", r"out2"],
        [],
        [r"out1", r"out2"],
        [],
        []]

    @staticmethod
    def list_zero_group(it):
        """
        Collects all MatchObject elements from the given iterator and extracts
        their first matching group (group 0).

        :param it: The input iterator where to collect from.
        """
        return [elem.group(0) for elem in it]

    # Test the unescaped_search_for() function.
    def test_basic(self):
        expected_results = self.test_basic_expected_results

        self.assertResultsEqual(
            unescaped_search_for,
            {(self.test_basic_pattern, test_string, 0, 0, True): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)},
            self.list_zero_group)

    # Test unescaped_search_for() with a simple pattern.
    def test_simple_pattern(self):
        expected_results = [
            2 * [r"'"],
            2 * [r"'"],
            2 * [r"'"],
            2 * [r"'"],
            2 * [r"'"],
            2 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            6 * [r"'"],
            [],
            [],
            [],
            []]

        self.assertResultsEqual(
            unescaped_search_for,
            {(r"'", test_string, 0, 0, use_regex): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)
             for use_regex in [True, False]},
            self.list_zero_group)

    # Test unescaped_search_for() with an empty pattern.
    def test_empty_pattern(self):
        # Since an empty pattern can also be escaped, the result contains
        # special cases. Especially we check the completely matched string (and
        # not only the matched pattern itself) we need to place also the
        # matched escape characters inside the result list consumed from the
        # internal regex of unescaped_search_for().
        expected_results = [
            38 * [r""],
            38 * [r""],
            38 * [r""],
            37 * [r""],
            38 * [r""],
            38 * [r""],
            39 * [r""],
            38 * [r""],
            37 * [r""],
            38 * [r""],
            37 * [r""],
            38 * [r""],
            37 * [r""],
            39 * [r""],
            [r""],
            15 * [r""],
            [r""],
            2 * [r""]]

        self.assertResultsEqual(
            unescaped_search_for,
            {(r"", test_string, 0, 0, use_regex): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)
             for use_regex in [True, False]},
            self.list_zero_group)

    # Test unescaped_search_for() for its max_match parameter.
    def test_max_match(self):
        search_pattern = self.test_basic_pattern
        expected_master_results = self.test_basic_expected_results

        self.assertResultsEqual(
            unescaped_search_for,
            {(search_pattern, test_string, 0, max_match, True): result
             for max_match in [1, 2, 3, 4, 5, 6, 987, 1122334455]
             for test_string, result in zip(
                 self.test_strings,
                 [elem[0: max_match] for elem in expected_master_results])},
            self.list_zero_group)

    # Test unescaped_search_for() for its max_match parameter with matches
    # that are also escaped.
    def test_max_match_escaping_flaw(self):
        expected_master_results = [
            2 * [r"'"],
            2 * [r"'"],
            2 * [r"'"],
            2 * [r"'"],
            2 * [r"'"],
            2 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            4 * [r"'"],
            6 * [r"'"],
            [],
            [],
            [],
            []]

        self.assertResultsEqual(
            unescaped_search_for,
            {(r"'", test_string, 0, max_match, use_regex): result
             for max_match in [1, 2, 3, 4, 5, 6, 100]
             for test_string, result in zip(
                 self.test_strings,
                 [elem[0: max_match] for elem in expected_master_results])
             for use_regex in [True, False]},
            self.list_zero_group)

    # Test unescaped_search_for() with regexes disabled.
    def test_disabled_regex(self):
        search_pattern = r"\'"
        expected_results = [
            [],
            [search_pattern],
            [],
            [],
            [search_pattern],
            [],
            [],
            [search_pattern],
            [search_pattern],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []]

        self.assertResultsEqual(
            unescaped_search_for,
            {(search_pattern, test_string, 0, 0, False): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)},
            self.list_zero_group)


if __name__ == '__main__':
    unittest.main(verbosity=2)
