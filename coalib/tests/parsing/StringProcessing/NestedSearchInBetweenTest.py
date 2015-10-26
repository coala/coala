import sys
import unittest

sys.path.insert(0, ".")
from coalib.tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)
from coalib.parsing.StringProcessing import nested_search_in_between


class NestedSearchInBetweenTest(StringProcessingTestBase):
    bs = StringProcessingTestBase.bs

    test_basic_expected_results = [
        [r"", r"This is a word", r"(in a word) another "],
        [r"((((((((((((((((((1)2)3))))))))))))))))"],
        [r"do (it ) more ", r"", r"hello."],
        [r"", r"This\ is a word" + bs, r"(in a\\\ word\\\\\) another " + bs],
        [r"\(\((((((\\\(((((((((((1)2)3))\\\\\)))))))))))))\)" + bs],
        [r"do (it ) more ", r"", r"hello."]]

    # Test the basic functionality of nested_search_in_between().
    def test_basic(self):
        self.assertResultsEqual(
            nested_search_in_between,
            {(self.search_in_between_begin_pattern,
              self.search_in_between_end_pattern,
              test_string,
              0,
              False,
              False): result
             for test_string, result in zip(
                 self.search_in_between_test_strings,
                 self.test_basic_expected_results)},
            list)

    # Test nested_search_in_between() when feeding it with the same begin- and
    # end-sequences.
    def test_same_pattern(self):
        self.assertResultsEqual(
            nested_search_in_between,
            {(pattern, pattern, test_string, 0, False, False): []
             for test_string in self.search_in_between_test_strings
             for pattern in [self.search_in_between_begin_pattern,
                             self.search_in_between_end_pattern]},
            list)

    # Test nested_search_in_between() for its max_match parameter.
    def test_max_match(self):
        self.assertResultsEqual(
            nested_search_in_between,
            {(self.search_in_between_begin_pattern,
              self.search_in_between_end_pattern,
              test_string,
              max_match,
              False,
              False): result
             for max_match in [1, 2, 5, 22]
             for test_string, result in zip(
                 self.search_in_between_test_strings,
                 [elem[0:max_match]
                     for elem in self.test_basic_expected_results])},
            list)

    # Test nested_search_in_between() with a regex pattern.
    def test_regex_pattern(self):
        self.assertResultsEqual(
            nested_search_in_between,
            {(r"(?:)\(", r"\)(?:)", test_string, 0, False, True): result
             for test_string, result in zip(
                 self.search_in_between_test_strings,
                 self.test_basic_expected_results)},
            list)

    # Test nested_search_in_between() for its auto_trim feature.
    def test_auto_trim(self):
        expected_results = [
            [r"This is a word", r"(in a word) another "],
            [r"((((((((((((((((((1)2)3))))))))))))))))"],
            [r"do (it ) more ", r"hello."],
            [r"This\ is a word" + self.bs,
                r"(in a\\\ word\\\\\) another " + self.bs],
            [r"\(\((((((\\\(((((((((((1)2)3))\\\\\)))))))))))))\)" + self.bs],
            [r"do (it ) more ", r"hello."]]

        self.assertResultsEqual(
            nested_search_in_between,
            {(begin_pattern,
              end_pattern,
              test_string,
              0,
              True,
              use_regex): result
             for test_string, result in zip(
                 self.search_in_between_test_strings,
                 expected_results)
             for use_regex, begin_pattern, end_pattern in [
                 (True, r"\(", r"\)"),
                 (False,
                  self.search_in_between_begin_pattern,
                  self.search_in_between_end_pattern)]},
            list)

    # Test for special cases that exposed bugs earlier.
    def test_special(self):
        self.assertResultsEqual(
            nested_search_in_between,
            {("(", ")", "a)b(c", 0, True, False): []},
            list)


if __name__ == '__main__':
    unittest.main(verbosity=2)

