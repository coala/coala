import unittest

from coalib.tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)
from coalib.parsing.StringProcessing import (InBetweenMatch,
                                             nested_search_in_between)


class NestedSearchInBetweenTest(StringProcessingTestBase):
    bs = StringProcessingTestBase.bs

    test_basic_expected_results = [
        [("(", 0, "", 1, ")", 1),
         ("(", 6, "This is a word", 7, ")", 21),
         ("(", 25, "(in a word) another ", 26, ")", 46)],
        [("(", 4, "((((((((((((((((((1)2)3))))))))))))))))", 5, ")", 44)],
        [("(", 6, "do (it ) more ", 7, ")", 21),
         ("(", 41, "", 42, ")", 42),
         ("(", 44, "hello.", 45, ")", 51)],
        [("(", 0, "", 1, ")", 1),
         ("(", 8, r"This\ is a word" + bs, 9, ")", 25),
         ("(", 29, r"(in a\\\ word\\\\\) another " + bs, 30, ")", 59)],
        [("(", 5,
          r"\(\((((((\\\(((((((((((1)2)3))\\\\\)))))))))))))\)" + bs, 6,
          ")", 57)],
        [("(", 7, "do (it ) more ", 8, ")", 22),
         ("(", 45, "", 46, ")", 46),
         ("(", 48, "hello.", 49, ")", 55)]]

    # Test the basic functionality of nested_search_in_between().
    def test_basic(self):
        self.assertResultsEqual(
            nested_search_in_between,
            {(self.search_in_between_begin_pattern,
              self.search_in_between_end_pattern,
              test_string,
              0,
              False,
              False): [InBetweenMatch.from_values(*args)
                       for args in result]
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
              False): [InBetweenMatch.from_values(*args)
                       for args in result]
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
            {(r"(?:)\(", r"\)(?:)", test_string, 0, False, True):
             [InBetweenMatch.from_values(*args) for args in result]
             for test_string, result in zip(
                 self.search_in_between_test_strings,
                 self.test_basic_expected_results)},
            list)

    # Test nested_search_in_between() for its auto_trim feature.
    def test_auto_trim(self):
        expected_results = [
            [("(", 6, "This is a word", 7, ")", 21),
             ("(", 25, "(in a word) another ", 26, ")", 46)],
            [("(", 4, "((((((((((((((((((1)2)3))))))))))))))))", 5, ")", 44)],
            [("(", 6, "do (it ) more ", 7, ")", 21),
             ("(", 44, "hello.", 45, ")", 51)],
            [("(", 8, r"This\ is a word" + self.bs, 9, ")", 25),
             ("(", 29,
              r"(in a\\\ word\\\\\) another " + self.bs, 30,
              ")", 59)],
            [("(",
              5,
              r"\(\((((((\\\(((((((((((1)2)3))\\\\\)))))))))))))\)" + self.bs,
              6,
              ")",
              57)],
            [("(", 7, "do (it ) more ", 8, ")", 22),
             ("(", 48, "hello.", 49, ")", 55)]]

        self.assertResultsEqual(
            nested_search_in_between,
            {(begin_pattern,
              end_pattern,
              test_string,
              0,
              True,
              use_regex): [InBetweenMatch.from_values(*args)
                           for args in result]
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
