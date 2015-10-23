import sys
import unittest

sys.path.insert(0, ".")
from coalib.tests.parsing.StringProcessingTest import StringProcessingTest
from coalib.parsing.StringProcessing import (
    InBetweenMatch,
    Match,
    nested_search_in_between)


class NestedSearchInBetweenTest(StringProcessingTest):
    bs = StringProcessingTest.bs

    test_basic_expected_results = [
        [InBetweenMatch(Match("(", 0), Match("", 1), Match(")", 1)),
         InBetweenMatch(Match("(", 6),
                        Match("This is a word", 7),
                        Match(")", 21)),
         InBetweenMatch(Match("(", 25),
                        Match("(in a word) another ", 26),
                        Match(")", 46))],
        [InBetweenMatch(Match("(", 4),
                        Match("((((((((((((((((((1)2)3))))))))))))))))", 5),
                        Match(")", 44))],
        [InBetweenMatch(Match("(", 6),
                        Match("do (it ) more ", 7),
                        Match(")", 21)),
         InBetweenMatch(Match("(", 41), Match("", 42), Match(")", 42)),
         InBetweenMatch(Match("(", 44), Match("hello.", 45), Match(")", 51))],
        [InBetweenMatch(Match("(", 0), Match("", 1), Match(")", 1)),
         InBetweenMatch(Match("(", 8),
                        Match(r"This\ is a word" + bs, 9),
                        Match(")", 25)),
         InBetweenMatch(Match("(", 29),
                        Match(r"(in a\\\ word\\\\\) another " + bs, 30),
                        Match(")", 59))],
        [InBetweenMatch(Match("(", 5),
                        Match(r"\(\((((((\\\(((((((((((1)2)3))\\\\\))))))))))))"
                              r")\)" + bs, 6),
                        Match(")", 57))],
        [InBetweenMatch(Match("(", 7),
                        Match("do (it ) more ", 8),
                        Match(")", 22)),
         InBetweenMatch(Match("(", 45),
                        Match("", 46),
                        Match(")", 46)),
         InBetweenMatch(Match("(", 48),
                        Match("hello.", 49),
                        Match(")", 55))]]

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
            [InBetweenMatch(Match("(", 6),
                            Match("This is a word", 7),
                            Match(")", 21)),
             InBetweenMatch(Match("(", 25),
                            Match("(in a word) another ", 26),
                            Match(")", 46))],
            [InBetweenMatch(Match("(", 4),
                            Match("((((((((((((((((((1)2)3))))))))))))))))", 5),
                            Match(")", 44))],
            [InBetweenMatch(Match("(", 6),
                            Match("do (it ) more ", 7),
                            Match(")", 21)),
             InBetweenMatch(Match("(", 44),
                            Match("hello.", 45),
                            Match(")", 51))],
            [InBetweenMatch(Match("(", 8),
                            Match(r"This\ is a word" + self.bs, 9),
                            Match(")", 25)),
             InBetweenMatch(Match("(", 29),
                            Match(r"(in a\\\ word\\\\\) another " + self.bs,
                                  30),
                            Match(")", 59))],
            [InBetweenMatch(Match("(", 5),
                            Match(r"\(\((((((\\\(((((((((((1)2)3))\\\\\))))))))"
                                  r")))))\)" + self.bs, 6),
                            Match(")", 57))],
            [InBetweenMatch(Match("(", 7),
                            Match("do (it ) more ", 8),
                            Match(")", 22)),
             InBetweenMatch(Match("(", 48),
                            Match("hello.", 49),
                            Match(")", 55))]]

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

