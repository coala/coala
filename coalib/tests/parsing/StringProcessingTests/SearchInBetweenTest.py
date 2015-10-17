import sys
import unittest

sys.path.insert(0, ".")
from coalib.tests.parsing.StringProcessingTest import StringProcessingTest
from coalib.parsing.StringProcessing import (InBetweenMatch,
                                             Match,
                                             search_in_between)


class SearchInBetweenTest(StringProcessingTest):
    bs = StringProcessingTest.bs

    test_basic_pattern = "'"
    test_basic_expected_results = [
        [InBetweenMatch(Match(test_basic_pattern, 5),
                        Match(r"escaped-escape:        \\ ", 6),
                        Match(test_basic_pattern, 32))],
        [InBetweenMatch(Match(test_basic_pattern, 5),
                        Match(r"escaped-quote:         " + bs, 6),
                        Match(test_basic_pattern, 30))],
        [InBetweenMatch(Match(test_basic_pattern, 5),
                        Match(r"escaped-anything:      \X ", 6),
                        Match(test_basic_pattern, 32))],
        [InBetweenMatch(Match(test_basic_pattern, 5),
                        Match(r"two escaped escapes: \\\\ ", 6),
                        Match(test_basic_pattern, 32))],
        [InBetweenMatch(Match(test_basic_pattern, 5),
                        Match("escaped-quote at end:   " + bs, 6),
                        Match(test_basic_pattern, 31))],
        [InBetweenMatch(Match(test_basic_pattern, 5),
                        Match("escaped-escape at end:  " + 2 * bs, 6),
                        Match(test_basic_pattern, 32))],
        [InBetweenMatch(Match(test_basic_pattern, 15),
                        Match("str1", 16),
                        Match(test_basic_pattern, 20)),
         InBetweenMatch(Match(test_basic_pattern, 27),
                        Match("str2", 28),
                        Match(test_basic_pattern, 32))],
        [InBetweenMatch(Match(test_basic_pattern, 6),
                        Match("        ", 7),
                        Match(test_basic_pattern, 15)),
         InBetweenMatch(Match(test_basic_pattern, 20),
                        Match(" out2 ", 21),
                        Match(test_basic_pattern, 27))],
        [InBetweenMatch(Match(test_basic_pattern, 8),
                        Match("      ", 9),
                        Match(test_basic_pattern, 15)),
         InBetweenMatch(Match(test_basic_pattern, 20),
                        Match(" out2 ", 21),
                        Match(test_basic_pattern, 27))],
        [InBetweenMatch(Match(test_basic_pattern, 15),
                        Match("str1", 16),
                        Match(test_basic_pattern, 20)),
         InBetweenMatch(Match(test_basic_pattern, 27),
                        Match("str2", 28),
                        Match(test_basic_pattern, 32))],
        [InBetweenMatch(Match(test_basic_pattern, 15),
                        Match("str1", 16),
                        Match(test_basic_pattern, 20)),
         InBetweenMatch(Match(test_basic_pattern, 27),
                        Match("str2", 28),
                        Match(test_basic_pattern, 32))],
        [InBetweenMatch(Match(test_basic_pattern, 15),
                        Match("str1", 16),
                        Match(test_basic_pattern, 20)),
         InBetweenMatch(Match(test_basic_pattern, 27),
                        Match("str2", 28),
                        Match(test_basic_pattern, 32))],
        [InBetweenMatch(Match(test_basic_pattern, 15),
                        Match("str1", 16),
                        Match(test_basic_pattern, 20)),
         InBetweenMatch(Match(test_basic_pattern, 27),
                        Match("str2", 28),
                        Match(test_basic_pattern, 32))],
        [InBetweenMatch(Match(test_basic_pattern, 15),
                        Match("str1", 16),
                        Match(test_basic_pattern, 20)),
         InBetweenMatch(Match(test_basic_pattern, 21),
                        Match("str2", 22),
                        Match(test_basic_pattern, 26)),
         InBetweenMatch(Match(test_basic_pattern, 27),
                        Match("str3", 28),
                        Match(test_basic_pattern, 32))],
        [],
        [],
        [],
        []]

    # Test the basic search_in_between() functionality.
    def test_basic(self):
        expected_results = self.test_basic_expected_results

        self.assertResultsEqual(
            search_in_between,
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

    # Test the search_in_between() while varying the max_match
    # parameter.
    def test_max_match(self):
        search_pattern = self.test_basic_pattern
        expected_master_results = self.test_basic_expected_results

        self.assertResultsEqual(
            search_in_between,
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

    # Test the search_in_between() function with different regex
    # patterns.
    def test_regex_pattern(self):
        expected_results = [
            [InBetweenMatch(Match("abc", 0), Match("", 3), Match("abc", 3))],
            [InBetweenMatch(Match("ab", 0), Match("c", 2), Match("ab", 3))],
            [InBetweenMatch(Match("ab", 0), Match("c", 2), Match("ab", 3)),
             InBetweenMatch(Match("ab", 21),
                            Match(r"bc\+'**'", 23),
                            Match("ac", 31))],
            [InBetweenMatch(Match(self.bs, 12),
                            Match("", 13),
                            Match(self.bs, 13))],
            [InBetweenMatch(Match("###", 9),
                            Match(r"\\13q4ujsabbc\+'**'ac", 12),
                            Match("###", 33)),
             InBetweenMatch(Match("#", 37),
                            Match(".", 38),
                            Match("####", 39))],
            [InBetweenMatch(Match("a", 0), Match("", 1), Match("b", 1)),
             InBetweenMatch(Match("a", 3), Match("", 4), Match("b", 4)),
             InBetweenMatch(Match("b", 7), Match("", 8), Match("a", 8)),
             InBetweenMatch(Match("##", 9), Match("", 11), Match("#\\", 11)),
             InBetweenMatch(Match("a", 21), Match("", 22), Match("b", 22)),
             InBetweenMatch(Match("b", 23),
                            Match(r"c\+'**'", 24),
                            Match("a", 31)),
             InBetweenMatch(Match("##", 33), Match("", 35), Match("#.", 35)),
             InBetweenMatch(Match("#.", 37), Match("", 39), Match("##", 39)),
             InBetweenMatch(Match("##", 41), Match("-", 43), Match("b", 44))],
            [InBetweenMatch(Match("abcabc", 0),
                            Match(r"cba###\\13q4ujs", 6),
                            Match("abbc", 21))],
            [InBetweenMatch(Match("1", 14),
                            Match("3q4ujsabbc" + self.bs, 15),
                            Match("+", 26))]]

        self.assertResultsEqual(
            search_in_between,
            {(pattern,
              pattern,
              self.multi_pattern_test_string,
              0,
              False,
              True): result
             for pattern, result in zip(self.multi_patterns,
                                        expected_results)},
            list)

    # Test the search_in_between() function for its
    # remove_empty_matches feature.
    def test_auto_trim(self):
        expected_results = [
            [],
            [InBetweenMatch(Match(";", 2),
                            Match(5 * self.bs, 3),
                            Match(";", 8)),
             InBetweenMatch(Match(";", 12),
                            Match(r"\\\'", 13),
                            Match(";", 17)),
             InBetweenMatch(Match(";", 18),
                            Match(self.bs, 19),
                            Match(";", 20)),
             InBetweenMatch(Match(";", 25),
                            Match("+ios", 26),
                            Match(";", 30))],
            [InBetweenMatch(Match(";", 1), Match("2", 2), Match(";", 3)),
             InBetweenMatch(Match(";", 5), Match("4", 6), Match(";", 7)),
             InBetweenMatch(Match(";", 9), Match("6", 10), Match(r";", 11))],
            [InBetweenMatch(Match(";", 1), Match("2", 2), Match(";", 3)),
             InBetweenMatch(Match(";", 5), Match("4", 6), Match(";", 7)),
             InBetweenMatch(Match(";", 9), Match("6", 10), Match(r";", 11))],
            [],
            [],
            [],
            [],
            [InBetweenMatch(Match(";", 3), Match(r"a", 4), Match(";", 5))]]

        self.assertResultsEqual(
            search_in_between,
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

    # Test the search_in_between() function for its use_regex parameter.
    def test_disabled_regex(self):
        search_pattern = r"\'"
        expected_results = [[] for x in range(len(self.test_strings))]

        self.assertResultsEqual(
            search_in_between,
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

    # Test the search_in_between() function using the test-strings specific
    # for search-in-between functions.
    def test_extended(self):
        expected_results = [
            [InBetweenMatch(Match("(", 0), Match("", 1), Match(")", 1)),
             InBetweenMatch(Match("(", 6),
                            Match("This is a word", 7),
                            Match(")", 21)),
             InBetweenMatch(Match("(", 25),
                            Match("(in a word", 26),
                            Match(")", 36))],
            [InBetweenMatch(Match("(", 4),
                            Match("((((((((((((((((((1", 5),
                            Match(")", 24))],
            [InBetweenMatch(Match("(", 6), Match("do (it ", 7), Match(")", 14)),
             InBetweenMatch(Match("(", 41), Match("", 42), Match(")", 42)),
             InBetweenMatch(Match("(", 44),
                            Match("hello.", 45),
                            Match(")", 51))],
            [InBetweenMatch(Match("(", 0), Match("", 1), Match(")", 1)),
             InBetweenMatch(Match("(", 8),
                            Match(r"This\ is a word" + self.bs, 9),
                            Match(")", 25)),
             InBetweenMatch(Match("(", 29),
                            Match(r"(in a\\\ word" + 5 * self.bs, 30),
                            Match(")", 48))],
            [InBetweenMatch(Match("(", 5),
                            Match(r"\(\((((((\\\(((((((((((1", 6),
                            Match(")", 30))],
            [InBetweenMatch(Match("(", 7), Match("do (it ", 8), Match(")", 15)),
             InBetweenMatch(Match("(", 45), Match("", 46), Match(")", 46)),
             InBetweenMatch(Match("(", 48),
                            Match("hello.", 49),
                            Match(")", 55))]]

        self.assertResultsEqual(
            search_in_between,
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

