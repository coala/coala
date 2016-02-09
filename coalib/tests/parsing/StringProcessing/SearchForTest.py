import unittest

from coalib.tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)
from coalib.parsing.StringProcessing import search_for


class SearchForTest(StringProcessingTestBase):
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

    # Test the search_for() function.
    def test_basic(self):
        expected_results = self.test_basic_expected_results

        self.assertResultsEqual(
            search_for,
            {(self.test_basic_pattern, test_string, 0, 0, True): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)},
            self.list_zero_group)

    # Test search_for() with a simple pattern.
    def test_simple_pattern(self):
        expected_results = [
            i * [r"'"] for i in
                [2, 3, 2, 2, 3, 2, 4, 5, 5, 4, 4, 4, 4, 6, 0, 0, 0, 0]]

        self.assertResultsEqual(
            search_for,
            {(r"'", test_string, 0, 0, use_regex): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)
             for use_regex in [True, False]},
            self.list_zero_group)

    # Test search_for() with an empty pattern.
    def test_empty_pattern(self):
        expected_results = [
            (len(elem) + 1) * [r""] for elem in self.test_strings]

        self.assertResultsEqual(
            search_for,
            {(r"", test_string, 0, 0, use_regex): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)
             for use_regex in [True, False]},
            self.list_zero_group)

    # Test search_for() for its max_match parameter.
    def test_max_match(self):
        search_pattern = self.test_basic_pattern
        expected_master_results = self.test_basic_expected_results

        self.assertResultsEqual(
            search_for,
            {(search_pattern, test_string, 0, max_match, True): result
             for max_match in [1, 2, 3, 4, 5, 6, 987, 100928321]
             for test_string, result in zip(
                 self.test_strings,
                 [elem[0: max_match] for elem in expected_master_results])},
            self.list_zero_group)

    # Test search_for() with regexes disabled.
    def test_disabled_regex(self):
        search_pattern = r"\'"
        expected_results = [
            [],
            [search_pattern],
            [],
            [],
            [search_pattern],
            [search_pattern],
            [],
            [search_pattern],
            [search_pattern],
            [],
            [],
            [search_pattern],
            [search_pattern],
            [],
            [],
            [],
            [],
            []]

        self.assertResultsEqual(
            search_for,
            {(search_pattern, test_string, 0, 0, False): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)},
            self.list_zero_group)


if __name__ == '__main__':
    unittest.main(verbosity=2)
