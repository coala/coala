import sys
import unittest

sys.path.insert(0, ".")
from coalib.tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)
from coalib.parsing.StringProcessing import unescaped_search_in_between


class UnescapedSearchInBetweenTest(StringProcessingTestBase):
    bs = StringProcessingTestBase.bs

    test_basic_pattern = "'"
    test_basic_expected_results = [
        [r"escaped-escape:        \\ "],
        [r"escaped-quote:         \' "],
        [r"escaped-anything:      \X "],
        [r"two escaped escapes: \\\\ "],
        [r"escaped-quote at end:   \'"],
        [r"escaped-escape at end:  " + 2 * bs],
        [r"str1", r"str2"],
        [r"str1", r"str2"],
        [r"str1", r"str2"],
        [r"str1", r"str2"],
        [r"str1", r"str2"],
        [r"str1", r"str2"],
        [r"str1", r"str2"],
        [r"str1", r"str2", r"str3"],
        [],
        [],
        [],
        []]

    # Test the basic unescaped_search_in_between() functionality.
    def test_basic(self):
        expected_results = self.test_basic_expected_results

        self.assertResultsEqual(
            unescaped_search_in_between,
            {(self.test_basic_pattern,
              self.test_basic_pattern,
              test_string,
              0,
              False,
              use_regex): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)
             for use_regex in [True, False]},
            list)

    # Test the unescaped_search_in_between() while varying the max_match
    # parameter.
    def test_max_match(self):
        search_pattern = self.test_basic_pattern
        expected_master_results = self.test_basic_expected_results

        self.assertResultsEqual(
            unescaped_search_in_between,
            {(search_pattern,
              search_pattern,
              test_string,
              max_match,
              False,
              use_regex): result
             for max_match in [1, 2, 3, 4, 5, 100]
             for test_string, result in zip(
                 self.test_strings,
                 [elem[0 : max_match] for elem in expected_master_results])
             for use_regex in [True, False]},
            list)

    # Test the unescaped_search_in_between() function with different regex
    # patterns.
    def test_regex_pattern(self):
        expected_results = [
            [r""],
            [r"c"],
            [r"c", r"bc\+'**'"],
            [r"\13q4ujsabbc"],
            [r"\\13q4ujsabbc\+'**'ac", r"."],
            [r"", r"", r"", r"", r"", r"c\+'**'", r"", r"", r"-"],
            [r"cba###\\13q4ujs"],
            []]

        self.assertResultsEqual(
            unescaped_search_in_between,
            {(pattern,
              pattern,
              self.multi_pattern_test_string,
              0,
              False,
              True): result
             for pattern, result in zip(self.multi_patterns,
                                        expected_results)},
            list)

    # Test the unescaped_search_in_between() function for its
    # remove_empty_matches feature.
    def test_auto_trim(self):
        expected_results = [
            [],
            [r"\\\\\;\\#", r"+ios"],
            [r"2", r"4", r"6"],
            [r"2", r"4", r"6"],
            [],
            [],
            [],
            [],
            [r"a"]]

        self.assertResultsEqual(
            unescaped_search_in_between,
            {(self.auto_trim_test_pattern,
              self.auto_trim_test_pattern,
              test_string,
              0,
              True,
              use_regex): result
             for test_string, result in zip(self.auto_trim_test_strings,
                                            expected_results)
             for use_regex in [True, False]},
            list)

    # Test the unescaped_search_in_between() function for its use_regex
    # parameter.
    def test_disabled_regex(self):
        search_pattern = r"'()?"
        expected_results = [[] for x in range(len(self.test_strings))]

        self.assertResultsEqual(
            unescaped_search_in_between,
            {(search_pattern,
              search_pattern,
              test_string,
              0,
              auto_trim, # For remove_empty_matches both works, True and False.
              False): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)
             for auto_trim in [True, False]},
            list)

    # Test the unescaped_search_in_between() function using the test-strings
    # specific for search-in-between functions.
    def test_extended(self):
        expected_results = [
            [r"", r"This is a word", r"(in a word"],
            [r"((((((((((((((((((1"],
            [r"do (it ", r"", r"hello."],
            [r"", r"This\ is a word\)and((in a\\\ word\\\\\) another \)"],
            [r"((((\\\(((((((((((1"],
            [r"it ", r"", r"hello."]]

        self.assertResultsEqual(
            unescaped_search_in_between,
            {(begin_pattern,
              end_pattern,
              test_string,
              0,
              False,
              use_regex): result
             for test_string, result in zip(
                 self.search_in_between_test_strings,
                 expected_results)
             for use_regex, begin_pattern, end_pattern in
                 [(True, r"\(", r"\)"),
                  (False,
                   self.search_in_between_begin_pattern,
                   self.search_in_between_end_pattern)]},
            list)


if __name__ == '__main__':
    unittest.main(verbosity=2)

