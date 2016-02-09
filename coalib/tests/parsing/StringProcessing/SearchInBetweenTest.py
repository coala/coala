import unittest

from coalib.tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)
from coalib.parsing.StringProcessing import InBetweenMatch, search_in_between


class SearchInBetweenTest(StringProcessingTestBase):
    bs = StringProcessingTestBase.bs

    test_basic_pattern = "'"
    test_basic_expected_results = [
        [(test_basic_pattern, 5,
          r"escaped-escape:        \\ ", 6,
          test_basic_pattern, 32)],
        [(test_basic_pattern, 5,
          "escaped-quote:         " + bs, 6,
          test_basic_pattern, 30)],
        [(test_basic_pattern, 5,
          r"escaped-anything:      \X ", 6,
          test_basic_pattern, 32)],
        [(test_basic_pattern, 5,
          r"two escaped escapes: \\\\ ", 6,
          test_basic_pattern, 32)],
        [(test_basic_pattern, 5,
          "escaped-quote at end:   " + bs, 6,
          test_basic_pattern, 31)],
        [(test_basic_pattern, 5,
          "escaped-escape at end:  " + 2 * bs, 6,
          test_basic_pattern, 32)],
        [(test_basic_pattern, 15, "str1", 16, test_basic_pattern, 20),
         (test_basic_pattern, 27, "str2", 28, test_basic_pattern, 32)],
        [(test_basic_pattern, 6, "        ", 7, test_basic_pattern, 15),
         (test_basic_pattern, 20, " out2 ", 21, test_basic_pattern, 27)],
        [(test_basic_pattern, 8, "      ", 9, test_basic_pattern, 15),
         (test_basic_pattern, 20, " out2 ", 21, test_basic_pattern, 27)],
        [(test_basic_pattern, 15, "str1", 16, test_basic_pattern, 20),
         (test_basic_pattern, 27, "str2", 28, test_basic_pattern, 32)],
        [(test_basic_pattern, 15, "str1", 16, test_basic_pattern, 20),
         (test_basic_pattern, 27, "str2", 28, test_basic_pattern, 32)],
        [(test_basic_pattern, 15, "str1", 16, test_basic_pattern, 20),
         (test_basic_pattern, 27, "str2", 28, test_basic_pattern, 32)],
        [(test_basic_pattern, 15, "str1", 16, test_basic_pattern, 20),
         (test_basic_pattern, 27, "str2", 28, test_basic_pattern, 32)],
        [(test_basic_pattern, 15, "str1", 16, test_basic_pattern, 20),
         (test_basic_pattern, 21, "str2", 22, test_basic_pattern, 26),
         (test_basic_pattern, 27, "str3", 28, test_basic_pattern, 32)],
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
              use_regex): [InBetweenMatch.from_values(*args)
                           for args in result]
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
              use_regex): [InBetweenMatch.from_values(*args)
                           for args in result]
             for max_match in [1, 2, 3, 4, 5, 100]
             for test_string, result in zip(
                 self.test_strings,
                 [elem[0: max_match] for elem in expected_master_results])
             for use_regex in [True, False]},
            list)

    # Test the search_in_between() function with different regex
    # patterns.
    def test_regex_pattern(self):
        expected_results = [
            [("abc", 0, "", 3, "abc", 3)],
            [("ab", 0, "c", 2, "ab", 3)],
            [("ab", 0, "c", 2, "ab", 3),
             ("ab", 21, r"bc\+'**'", 23, "ac", 31)],
            [(self.bs, 12, "", 13, self.bs, 13)],
            [("###", 9, r"\\13q4ujsabbc\+'**'ac", 12, "###", 33),
             ("#", 37, ".", 38, "####", 39)],
            [("a", 0, "", 1, "b", 1),
             ("a", 3, "", 4, "b", 4),
             ("b", 7, "", 8, "a", 8),
             ("##", 9, "", 11, "#\\", 11),
             ("a", 21, "", 22, "b", 22),
             ("b", 23, r"c\+'**'", 24, "a", 31),
             ("##", 33, "", 35, "#.", 35),
             ("#.", 37, "", 39, "##", 39),
             ("##", 41, "-", 43, "b", 44)],
            [("abcabc", 0, r"cba###\\13q4ujs", 6, "abbc", 21)],
            [("1", 14, "3q4ujsabbc" + self.bs, 15, "+", 26)]]

        self.assertResultsEqual(
            search_in_between,
            {(pattern,
              pattern,
              self.multi_pattern_test_string,
              0,
              False,
              True): [InBetweenMatch.from_values(*args)
                      for args in result]
             for pattern, result in zip(self.multi_patterns,
                                        expected_results)},
            list)

    # Test the search_in_between() function for its
    # remove_empty_matches feature.
    def test_auto_trim(self):
        expected_results = [
            [],
            [(";", 2, 5 * self.bs, 3, ";", 8),
             (";", 12, r"\\\'", 13, ";", 17),
             (";", 18, self.bs, 19, ";", 20),
             (";", 25, "+ios", 26, ";", 30)],
            [(";", 1, "2", 2, ";", 3),
             (";", 5, "4", 6, ";", 7),
             (";", 9, "6", 10, ";", 11)],
            [(";", 1, "2", 2, ";", 3),
             (";", 5, "4", 6, ";", 7),
             (";", 9, "6", 10, ";", 11)],
            [],
            [],
            [],
            [],
            [(";", 3, "a", 4, ";", 5)]]

        self.assertResultsEqual(
            search_in_between,
            {(self.auto_trim_test_pattern,
              self.auto_trim_test_pattern,
              test_string,
              0,
              True,
              use_regex): [InBetweenMatch.from_values(*args)
                           for args in result]
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
              # For remove_empty_matches both works, True and False.
              auto_trim,
              False): [InBetweenMatch.from_values(*args)
                       for args in result]
             for test_string, result in zip(self.test_strings,
                                            expected_results)
             for auto_trim in [True, False]},
            list)

    # Test the search_in_between() function using the test-strings specific
    # for search-in-between functions.
    def test_extended(self):
        expected_results = [
            [("(", 0, "", 1, ")", 1),
             ("(", 6, "This is a word", 7, ")", 21),
             ("(", 25, "(in a word", 26, ")", 36)],
            [("(", 4, "((((((((((((((((((1", 5, ")", 24)],
            [("(", 6, "do (it ", 7, ")", 14),
             ("(", 41, "", 42, ")", 42),
             ("(", 44, "hello.", 45, ")", 51)],
            [("(", 0, "", 1, ")", 1),
             ("(", 8, r"This\ is a word" + self.bs, 9, ")", 25),
             ("(", 29, r"(in a\\\ word" + 5 * self.bs, 30, ")", 48)],
            [("(", 5, r"\(\((((((\\\(((((((((((1", 6, ")", 30)],
            [("(", 7, "do (it ", 8, ")", 15),
             ("(", 45, "", 46, ")", 46),
             ("(", 48, "hello.", 49, ")", 55)]]

        self.assertResultsEqual(
            search_in_between,
            {(begin_pattern,
              end_pattern,
              test_string,
              0,
              False,
              use_regex): [InBetweenMatch.from_values(*args)
                           for args in result]
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
