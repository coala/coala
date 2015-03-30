import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import search_for
from coalib.parsing.StringProcessing import split
from coalib.parsing.StringProcessing import unescaped_split
from coalib.parsing.StringProcessing import search_in_between
from coalib.parsing.StringProcessing import unescaped_search_in_between
from coalib.parsing.StringProcessing import position_escaped
from coalib.parsing.StringProcessing import unescaped_find
from coalib.parsing.StringProcessing import unescaped_rfind


class StringProcessingTest(unittest.TestCase):
    def setUp(self):
        # The backslash character. Needed since there are limitations when
        # using backslashes at the end of raw-strings in front of the
        # terminating " or '.
        self.bs = "\\"

        self.test_strings = [
            r"out1 'escaped-escape:        \\ ' out2",
            r"out1 'escaped-quote:         \' ' out2",
            r"out1 'escaped-anything:      \X ' out2",
            r"out1 'two escaped escapes: \\\\ ' out2",
            r"out1 'escaped-quote at end:   \'' out2",
            r"out1 'escaped-escape at end:  \\' out2",
            r"out1           'str1' out2 'str2' out2",
            r"out1 \'        'str1' out2 'str2' out2",
            r"out1 \\\'      'str1' out2 'str2' out2",
            r"out1 \\        'str1' out2 'str2' out2",
            r"out1 \\\\      'str1' out2 'str2' out2",
            r"out1         \\'str1' out2 'str2' out2",
            r"out1       \\\\'str1' out2 'str2' out2",
            r"out1           'str1''str2''str3' out2",
            r"",
            r"out1 out2 out3",
            self.bs,
            2 * self.bs]

        # Test string for multi-pattern tests (since we want to variate the
        # pattern, not the test string).
        self.multi_pattern_test_string = (r"abcabccba###\\13q4ujsabbc\+'**'ac"
                                          r"###.#.####-ba")

        # Multiple patterns for the multi-pattern tests.
        self.multi_patterns = [r"abc",
                               r"ab",
                               r"ab|ac",
                               2 * self.bs,
                               r"#+",
                               r"(a)|(b)|(#.)",
                               r"(?:a(b)*c)+",
                               r"1|\+"]

        # Test strings for the remove_empty_matches feature (alias auto-trim).
        self.auto_trim_test_strings = [
            r";;;;;;;;;;;;;;;;",
            r"\\;\\\\\;\\#;\\\';;\;\\\\;+ios;;",
            r"1;2;3;4;5;6;",
            r"1;2;3;4;5;6;7",
            r"",
            r"Hello world",
            r"\;",
            r"\\;",
            r"abc;a;;;;;asc"]

        # Set up test dependent variables.
        self.set_up_search_for()
        self.set_up_split()
        self.set_up_unescaped_split()
        self.set_up_search_in_between()
        self.set_up_unescaped_search_in_between()

    def set_up_search_for(self):
        # Match either "out1" or "out2".
        self.test_search_for_pattern = "out1|out2"
        # These are the expected results for the zero-group of the
        # returned MatchObject's.
        self.test_search_for_expected_results = [
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

        self.test_search_for_simple_pattern_pattern = "'"
        self.test_search_for_simple_pattern_expected_results = [
            i * [r"'"] for i in
                [2, 3, 2, 2, 3, 2, 4, 5, 5, 4, 4, 4, 4, 6, 0, 0, 0, 0]]

        self.test_search_for_empty_pattern_pattern = ""
        self.test_search_for_empty_pattern_expected_results = [
            (len(elem) + 1) * [r""] for elem in self.test_strings]

        self.test_search_for_max_match_pattern = self.test_search_for_pattern
        self.test_search_for_max_match_expected_master_result = (
            self.test_search_for_expected_results)

    def set_up_split(self):
        self.test_split_pattern = "'"
        self.test_split_expected_results = [
            [r"out1 ", r"escaped-escape:        \\ ", r" out2"],
            [r"out1 ", r"escaped-quote:         " + self.bs, r" ", r" out2"],
            [r"out1 ", r"escaped-anything:      \X ", r" out2"],
            [r"out1 ", r"two escaped escapes: \\\\ ", r" out2"],
            [r"out1 ", r"escaped-quote at end:   " + self.bs, r"", r" out2"],
            [r"out1 ", r"escaped-escape at end:  " + 2 * self.bs, r" out2"],
            [r"out1           ", r"str1", r" out2 ", r"str2", r" out2"],
            [r"out1 " + self.bs, r"        ", r"str1", r" out2 ", r"str2",
                r" out2"],
            [r"out1 " + 3 * self.bs, r"      ", r"str1", r" out2 ", r"str2",
                r" out2"],
            [r"out1 \\        ", r"str1", r" out2 ", r"str2", r" out2"],
            [r"out1 \\\\      ", r"str1", r" out2 ", r"str2", r" out2"],
            [r"out1         " + 2 * self.bs, r"str1", r" out2 ", r"str2",
                r" out2"],
            [r"out1       " + 4 * self.bs, r"str1", r" out2 ", r"str2",
                r" out2"],
            [r"out1           ", r"str1", r"", r"str2", r"", r"str3",
                r" out2"],
            [r""],
            [r"out1 out2 out3"],
            [self.bs],
            [2 * self.bs]]

        self.test_split_max_split_pattern = self.test_split_pattern
        self.test_split_max_split_expected_master_results = (
            self.test_split_expected_results)

        self.test_split_regex_pattern_expected_results = [
            [r"", r"", r"cba###\\13q4ujsabbc\+'**'ac###.#.####-ba"],
            [r"", r"c", r"ccba###\\13q4ujs", r"bc\+'**'ac###.#.####-ba"],
            [r"", r"c", r"ccba###\\13q4ujs", r"bc\+'**'", r"###.#.####-ba"],
            [r"abcabccba###", r"", r"13q4ujsabbc", r"+'**'ac###.#.####-ba"],
            [r"abcabccba", r"\\13q4ujsabbc\+'**'ac", r".", r".", r"-ba"],
            [r"", r"", r"c", r"", r"cc", r"", r"", r"", r"\13q4ujs", r"", r"",
                r"c\+'**'", r"c", r"", r"", r"", r"", r"-", r"", r""],
            [r"", r"cba###\\13q4ujs", r"\+'**'", r"###.#.####-ba"],
            [r"abcabccba###" + 2 * self.bs, r"3q4ujsabbc" + self.bs,
                r"'**'ac###.#.####-ba"]]

        self.test_split_auto_trim_pattern = ";"
        self.test_split_auto_trim_expected_results = [
            [],
            [2 * self.bs, 5 * self.bs, r"\\#", r"\\\'", self.bs, 4 * self.bs,
                r"+ios"],
            [r"1", r"2", r"3", r"4", r"5", r"6"],
            [r"1", r"2", r"3", r"4", r"5", r"6", r"7"],
            [],
            [r"Hello world"],
            [self.bs],
            [2 * self.bs],
            [r"abc", r"a", r"asc"]]

    def set_up_unescaped_split(self):
        self.test_unescaped_split_pattern = "'"
        self.test_unescaped_split_expected_results = [
            [r"out1 ", r"escaped-escape:        \\ ", r" out2"],
            [r"out1 ", r"escaped-quote:         \' ", r" out2"],
            [r"out1 ", r"escaped-anything:      \X ", r" out2"],
            [r"out1 ", r"two escaped escapes: \\\\ ", r" out2"],
            [r"out1 ", r"escaped-quote at end:   \'", r" out2"],
            [r"out1 ", r"escaped-escape at end:  " + 2 * self.bs, r" out2"],
            [r"out1           ", r"str1", r" out2 ", r"str2", r" out2"],
            [r"out1 \'        ", r"str1", r" out2 ", r"str2", r" out2"],
            [r"out1 \\\'      ", r"str1", r" out2 ", r"str2", r" out2"],
            [r"out1 \\        ", r"str1", r" out2 ", r"str2", r" out2"],
            [r"out1 \\\\      ", r"str1", r" out2 ", r"str2", r" out2"],
            [r"out1         " + 2 * self.bs, r"str1", r" out2 ", r"str2",
                r" out2"],
            [r"out1       " + 4 * self.bs, r"str1", r" out2 ", r"str2",
                r" out2"],
            [r"out1           ", r"str1", r"", r"str2", r"", r"str3",
                r" out2"],
            [r""],
            [r"out1 out2 out3"],
            [self.bs],
            [2 * self.bs]]

        self.test_unescaped_split_max_split_pattern = (
            self.test_unescaped_split_pattern)
        self.test_unescaped_split_max_split_expected_master_results = (
            self.test_unescaped_split_expected_results)

        self.test_unescaped_split_regex_pattern_expected_results = [
            [r"", r"", r"cba###\\13q4ujsabbc\+'**'ac###.#.####-ba"],
            [r"", r"c", r"ccba###\\13q4ujs", r"bc\+'**'ac###.#.####-ba"],
            [r"", r"c", r"ccba###\\13q4ujs", r"bc\+'**'", r"###.#.####-ba"],
            [r"abcabccba###", r"\13q4ujsabbc", r"+'**'ac###.#.####-ba"],
            [r"abcabccba", r"\\13q4ujsabbc\+'**'ac", r".", r".", r"-ba"],
            [r"", r"", r"c", r"", r"cc", r"", r"", r"", r"\13q4ujs", r"", r"",
                r"c\+'**'", r"c", r"", r"", r"", r"", r"-", r"", r""],
            [r"", r"cba###\\13q4ujs", r"\+'**'", r"###.#.####-ba"],
            [r"abcabccba###" + 2 * self.bs,
                r"3q4ujsabbc\+'**'ac###.#.####-ba"]]

        self.test_unescaped_split_auto_trim_pattern = ";"
        self.test_unescaped_split_auto_trim_expected_results = [
            [],
            [2 * self.bs, r"\\\\\;\\#", r"\\\'", r"\;\\\\", r"+ios"],
            [r"1", r"2", r"3", r"4", r"5", r"6"],
            [r"1", r"2", r"3", r"4", r"5", r"6", r"7"],
            [],
            [r"Hello world"],
            [r"\;"],
            [2 * self.bs],
            [r"abc", r"a", r"asc"]]

    def set_up_search_in_between(self):
        self.test_search_in_between_pattern = "'"
        self.test_search_in_between_expected_results = [
            [r"escaped-escape:        \\ "],
            [r"escaped-quote:         " + self.bs],
            [r"escaped-anything:      \X "],
            [r"two escaped escapes: \\\\ "],
            [r"escaped-quote at end:   " + self.bs],
            [r"escaped-escape at end:  " + 2 * self.bs],
            [r"str1", r"str2"],
            [r"        ", r" out2 "],
            [r"      ", r" out2 "],
            [r"str1", r"str2"],
            [r"str1", r"str2"],
            [r"str1", r"str2"],
            [r"str1", r"str2"],
            [r"str1", r"str2", r"str3"],
            [],
            [],
            [],
            []]

        self.test_search_in_between_max_match_pattern = (
            self.test_search_in_between_pattern)
        self.test_search_in_between_max_match_expected_master_results = (
            self.test_search_in_between_expected_results)

        self.test_search_in_between_regex_pattern_expected_results = [
            [r""],
            [r"c"],
            [r"c", r"bc\+'**'"],
            [r""],
            [r"\\13q4ujsabbc\+'**'ac", r"."],
            [r"", r"", r"", r"", r"", r"c\+'**'", r"", r"", r"-"],
            [r"cba###\\13q4ujs"],
            [r"3q4ujsabbc" + self.bs]]

        self.test_search_in_between_auto_trim_pattern = ";"
        self.test_search_in_between_auto_trim_expected_results = [
            [],
            [5 * self.bs, r"\\\'", self.bs, r"+ios"],
            [r"2", r"4", r"6"],
            [r"2", r"4", r"6"],
            [],
            [],
            [],
            [],
            [r"a"]]

    def set_up_unescaped_search_in_between(self):
        self.test_unescaped_search_in_between_pattern = "'"
        self.test_unescaped_search_in_between_expected_results = [
            [r"escaped-escape:        \\ "],
            [r"escaped-quote:         \' "],
            [r"escaped-anything:      \X "],
            [r"two escaped escapes: \\\\ "],
            [r"escaped-quote at end:   \'"],
            [r"escaped-escape at end:  " + 2 * self.bs],
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

        self.test_unescaped_search_in_between_max_match_pattern = (
            self.test_unescaped_search_in_between_pattern)
        self.test_unescaped_search_in_between_max_match_expected_m_results = (
            self.test_unescaped_search_in_between_expected_results)

        self.test_unescaped_search_in_between_regex_pattern_expected = [
            [r""],
            [r"c"],
            [r"c", r"bc\+'**'"],
            [r"\13q4ujsabbc"],
            [r"\\13q4ujsabbc\+'**'ac", r"."],
            [r"", r"", r"", r"", r"", r"c\+'**'", r"", r"", r"-"],
            [r"cba###\\13q4ujs"],
            []]

        self.test_unescaped_search_in_between_auto_trim_pattern = ";"
        self.test_unescaped_search_in_between_auto_trim_expected_results = [
            [],
            [r"\\\\\;\\#", r"+ios"],
            [r"2", r"4", r"6"],
            [r"2", r"4", r"6"],
            [],
            [],
            [],
            [],
            [r"a"]]

    def assertSearchForResultEqual(self,
                                   pattern,
                                   test_strings,
                                   expected_strings,
                                   flags = 0,
                                   max_match = 0):
        """
        Checks whether the given test_strings do equal the expected_strings
        after feeding search_for() with them.

        :param pattern:          The pattern to pass to search_for().
        :param test_strings:     The test string to pass to search_for().
        :param expected_strings: The expected results to make the asserts for.
        :param flags:            Passed to the parameter flags in search_for().
        :param max_match:        The number of matches to perform. 0 or
                                 less would not limit the number of matches.
        """
        self.assertEqual(len(expected_strings), len(test_strings))
        for i in range(0, len(expected_strings)):
            return_value = search_for(pattern,
                                      test_strings[i],
                                      flags,
                                      max_match)

            # Check each MatchObject. Need to iterate over the return_value
            # since the return value is an iterator object pointing to the
            # MatchObject's.
            n = 0
            for x in return_value:
                self.assertEqual(expected_strings[i][n], x.group(0))
                n += 1

            self.assertEqual(n, len(expected_strings[i]))

    def assertSplitEquals(self,
                          test_strings,
                          expected_results,
                          pattern,
                          max_split=0,
                          remove_empty_matches=False):
        """
        Checks whether all supplied test strings are returned as expected from
        split().

        :param test_strings:         The list of test strings.
        :param expected_results:     The list of the expected results.
        :param pattern:              The pattern to invoke split() with.
        :param max_split:            The maximum number of splits to perform
                                     when invoking split().
        :param remove_empty_matches: Whether to remove empty entries or not.
        """
        self.assertEqual(len(expected_results), len(test_strings))
        for i in range(0, len(expected_results)):
            return_value = split(pattern,
                                 test_strings[i],
                                 max_split,
                                 remove_empty_matches)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    def assertUnescapedSplitEquals(self,
                                   test_strings,
                                   expected_results,
                                   pattern,
                                   max_split=0,
                                   remove_empty_matches=False):
        """
        Checks whether all supplied test strings are returned as expected from
        unescaped_split().

        :param test_strings:         The list of test strings.
        :param expected_results:     The list of the expected results.
        :param pattern:              The pattern to invoke unescaped_split()
                                     with.
        :param max_split:            The maximum number of splits to perform
                                     when invoking unescaped_split().
        :param remove_empty_matches: Whether to remove empty entries or not.
        """
        self.assertEqual(len(expected_results), len(test_strings))
        for i in range(0, len(expected_results)):
            return_value = unescaped_split(pattern,
                                           test_strings[i],
                                           max_split,
                                           remove_empty_matches)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    def assertSearchInBetweenEquals(self,
                                    test_strings,
                                    expected_results,
                                    begin,
                                    end,
                                    max_match=0,
                                    remove_empty_matches=False):
        """
        Checks whether all supplied test strings are returned as expected from
        search_in_between().

        :param test_strings:         The list of test strings.
        :param expected_results:     The list of the expected results.
        :param begin:                The beginning pattern to invoke
                                     search_in_between() with.
        :param end:                  The ending pattern to invoke
                                     search_in_between() with.
        :param max_match:            The maximum number of matches to perform
                                     when invoking search_in_between().
        :param remove_empty_matches: Whether to remove empty entries or not.
        """
        self.assertEqual(len(expected_results), len(test_strings))
        for i in range(0, len(expected_results)):
            return_value = search_in_between(begin,
                                             end,
                                             test_strings[i],
                                             max_match,
                                             remove_empty_matches)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    def assertUnescapedSearchInBetweenEquals(self,
                                             test_strings,
                                             expected_results,
                                             begin,
                                             end,
                                             max_match=0,
                                             remove_empty_matches=False):
        """
        Checks whether all supplied test strings are returned as expected from
        unescaped_search_in_between().

        :param test_strings:         The list of test strings.
        :param expected_results:     The list of the expected results.
        :param begin:                The beginning pattern to invoke
                                     unescaped_search_in_between() with.
        :param end:                  The ending pattern to invoke
                                     unescaped_search_in_between() with.
        :param max_match:            The maximum number of matches to perform
                                     when invoking
                                     unescaped_search_in_between().
        :param remove_empty_matches: Whether to remove empty entries or not.
        """
        self.assertEqual(len(expected_results), len(test_strings))
        for i in range(0, len(expected_results)):
            return_value = unescaped_search_in_between(begin,
                                                       end,
                                                       test_strings[i],
                                                       max_match,
                                                       remove_empty_matches)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    def assertIteratorElementsEqual(self, iterator1, iterator2):
        """
        Checks whether each element in the iterators and their length do equal.

        :param iterator1: The first iterator.
        :param iterator2: The second iterator.
        """
        for x in iterator1:
            self.assertEqual(x, next(iterator2))

        self.assertRaises(StopIteration, next, iterator2)

    # Test the search_for() function.
    def test_search_for(self):
        search_pattern = self.test_search_for_pattern
        expected_results = self.test_search_for_expected_results

        self.assertSearchForResultEqual(search_pattern,
                                        self.test_strings,
                                        expected_results)

    # Test search_for() with a simple pattern.
    def test_search_for_simple_pattern(self):
        search_pattern = self.test_search_for_simple_pattern_pattern
        expected_results = self.test_search_for_simple_pattern_expected_results

        self.assertSearchForResultEqual(search_pattern,
                                        self.test_strings,
                                        expected_results)

    # Test search_for() with an empty pattern.
    def test_search_for_empty_pattern(self):
        search_pattern = self.test_search_for_empty_pattern_pattern
        expected_results = self.test_search_for_empty_pattern_expected_results

        self.assertSearchForResultEqual(search_pattern,
                                        self.test_strings,
                                        expected_results)

    # Test search_for() for its max_match parameter.
    def test_search_for_max_match(self):
        search_pattern = self.test_search_for_max_match_pattern
        expected_master_results = (
            self.test_search_for_max_match_expected_master_result)

        for i in [1, 2, 3, 4, 5, 6, 987, 100928321]:
            expected_results = [
                expected_master_results[j][0 : i]
                for j in range(len(expected_master_results))]
            self.assertSearchForResultEqual(search_pattern,
                                            self.test_strings,
                                            expected_results,
                                            0,
                                            i)

    # Test the basic split() functionality.
    def test_split(self):
        self.assertSplitEquals(self.test_strings,
                               self.test_split_expected_results,
                               self.test_split_pattern)

    # Test the split() function while varying the max_split parameter.
    def test_split_max_split(self):
        separator_pattern = self.test_split_max_split_pattern
        expected_master_results = (
            self.test_split_max_split_expected_master_results)

        for max_split in [1, 2, 3, 4, 5, 6, 7, 8, 9, 112]:
            expected_results = [
                expected_master_results[j][0 : max_split]
                    for j in range(len(expected_master_results))]

            for j in range(len(expected_master_results)):
                if max_split < len(expected_master_results[j]):
                    # max_split is less the length of our master result list,
                    # need to append the rest as a joined string.
                    expected_results[j].append(
                        str.join(separator_pattern,
                                 expected_master_results[j][max_split : ]))

            self.assertSplitEquals(self.test_strings,
                                   expected_results,
                                   separator_pattern,
                                   max_split)

    # Test the split() function with different regex patterns.
    def test_split_regex_pattern(self):
        expected_results = self.test_split_regex_pattern_expected_results

        self.assertEqual(len(expected_results), len(self.multi_patterns))
        for i in range(0, len(expected_results)):
            return_value = split(self.multi_patterns[i],
                                 self.multi_pattern_test_string)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the split() function for its remove_empty_matches feature.
    def test_split_auto_trim(self):
        self.assertSplitEquals(self.auto_trim_test_strings,
                               self.test_split_auto_trim_expected_results,
                               self.test_split_auto_trim_pattern,
                               0,
                               True)

    # Test the basic unescaped_split() functionality.
    def test_unescaped_split(self):
        self.assertUnescapedSplitEquals(
            self.test_strings,
            self.test_unescaped_split_expected_results,
            self.test_unescaped_split_pattern)

    # Test the unescaped_split() function while varying the max_split
    # parameter.
    def test_unescaped_split_max_split(self):
        separator_pattern = self.test_unescaped_split_max_split_pattern
        expected_master_results = (
            self.test_unescaped_split_max_split_expected_master_results)

        for max_split in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99918829]:
            expected_results = [
                expected_master_results[j][0 : max_split]
                for j in range(len(expected_master_results))]

            for j in range(len(expected_master_results)):
                if max_split < len(expected_master_results[j]):
                    # max_split is less the length of our master result list,
                    # need to append the rest as a joined string.
                    expected_results[j].append(
                        str.join(separator_pattern,
                                 expected_master_results[j][max_split : ]))

            self.assertUnescapedSplitEquals(self.test_strings,
                                            expected_results,
                                            separator_pattern,
                                            max_split)

    # Test the unescaped_split() function with different regex patterns.
    def test_unescaped_split_regex_pattern(self):
        expected_results = (
            self.test_unescaped_split_regex_pattern_expected_results)

        self.assertEqual(len(expected_results), len(self.multi_patterns))
        for i in range(0, len(expected_results)):
            return_value = unescaped_split(self.multi_patterns[i],
                                           self.multi_pattern_test_string)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the unescaped_split() function for its remove_empty_matches feature.
    def test_unescaped_split_auto_trim(self):
        self.assertUnescapedSplitEquals(
            self.auto_trim_test_strings,
            self.test_unescaped_split_auto_trim_expected_results,
            self.test_unescaped_split_auto_trim_pattern,
            0,
            True)

    # Test the basic search_in_between() functionality.
    def test_search_in_between(self):
        self.assertSearchInBetweenEquals(
            self.test_strings,
            self.test_search_in_between_expected_results,
            self.test_search_in_between_pattern,
            self.test_search_in_between_pattern)

    # Test the search_in_between() while varying the max_match
    # parameter.
    def test_search_in_between_max_match(self):
        expected_master_results = (
            self.test_search_in_between_max_match_expected_master_results)

        for max_match in [1, 2, 3, 4, 5, 100]:
            expected_results = [
                expected_master_results[j][0 : max_match]
                for j in range(len(expected_master_results))]

            self.assertSearchInBetweenEquals(
                self.test_strings,
                expected_results,
                self.test_search_in_between_max_match_pattern,
                self.test_search_in_between_max_match_pattern,
                max_match)

    # Test the search_in_between() function with different regex
    # patterns.
    def test_search_in_between_regex_pattern(self):
        expected_results = (
            self.test_search_in_between_regex_pattern_expected_results)

        self.assertEqual(len(expected_results), len(self.multi_patterns))
        for i in range(0, len(expected_results)):
            # Use each pattern as begin and end sequence.
            return_value = search_in_between(self.multi_patterns[i],
                                             self.multi_patterns[i],
                                             self.multi_pattern_test_string)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the search_in_between() function for its
    # remove_empty_matches feature.
    def test_search_in_between_auto_trim(self):
        self.assertSearchInBetweenEquals(
            self.auto_trim_test_strings,
            self.test_search_in_between_auto_trim_expected_results,
            self.test_search_in_between_auto_trim_pattern,
            self.test_search_in_between_auto_trim_pattern,
            0,
            True)

    # Test the basic unescaped_search_in_between() functionality.
    def test_unescaped_search_in_between(self):
        self.assertUnescapedSearchInBetweenEquals(
            self.test_strings,
            self.test_unescaped_search_in_between_expected_results,
            self.test_unescaped_search_in_between_pattern,
            self.test_unescaped_search_in_between_pattern)

    # Test the unescaped_search_in_between() while varying the max_match
    # parameter.
    def test_unescaped_search_in_between_max_match(self):
        expected_master_results = (
            self.test_unescaped_search_in_between_max_match_expected_m_results)

        for max_match in [1, 2, 3, 4, 5, 67]:
            expected_results = [
                expected_master_results[j][0 : max_match]
                for j in range(len(expected_master_results))]

            self.assertUnescapedSearchInBetweenEquals(
                self.test_strings,
                expected_results,
                self.test_unescaped_search_in_between_max_match_pattern,
                self.test_unescaped_search_in_between_max_match_pattern,
                max_match)

    # Test the unescaped_search_in_between() function with different regex
    # patterns.
    def test_unescaped_search_in_between_regex_pattern(self):
        expected_results = (
            self.test_unescaped_search_in_between_regex_pattern_expected)

        self.assertEqual(len(expected_results), len(self.multi_patterns))
        for i in range(0, len(expected_results)):
            # Use each pattern as begin and end sequence.
            return_value = unescaped_search_in_between(
                self.multi_patterns[i],
                self.multi_patterns[i],
                self.multi_pattern_test_string)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the unescaped_search_in_between() function for its
    # remove_empty_matches feature.
    def test_unescaped_search_in_between_auto_trim(self):
        self.assertUnescapedSearchInBetweenEquals(
            self.auto_trim_test_strings,
            self.test_unescaped_search_in_between_auto_trim_expected_results,
            self.test_unescaped_search_in_between_auto_trim_pattern,
            self.test_unescaped_search_in_between_auto_trim_pattern,
            0,
            True)

    def test_position_escaped(self):
        self.assertRaises(ValueError, position_escaped, *(1, 1))
        self.assertRaises(ValueError, position_escaped, *("str", -1))
        self.assertRaises(ValueError, position_escaped, *("str", 3))

        test_string = "\\a\\\\b\\\\\\\\\\c\nx\n\\y\nz"
        self.assertEqual([position_escaped(test_string, i) for i in range(18)],
                         [False,
                          True,
                          False,
                          True,
                          False,
                          False,
                          True,
                          False,
                          True,
                          False,
                          True,
                          False,
                          False,
                          False,
                          False,
                          True,
                          False,
                          False])

    def test_unescaped_find(self):
        self.assertRaises(ValueError, unescaped_find, *(1, 1, 1, 1))
        self.assertRaises(ValueError, unescaped_find, *("s", 1, 1, 1))
        self.assertRaises(ValueError, unescaped_find, *("s", "s", "s", "1"))
        self.assertRaises(ValueError, unescaped_find, *("s", "s", 0, "s"))

        self.assertEqual(unescaped_find("abcde", "c"), 2)
        self.assertEqual(unescaped_find("abcde", "c", 1, 3), 2)
        self.assertEqual(unescaped_find("abcde", "c", 3, 4), -1)
        self.assertEqual(unescaped_find("abcde", "z"), -1)
        self.assertEqual(unescaped_find("ab\\cdec", "c"), 6)

    def test_unescaped_rfind(self):
        self.assertRaises(ValueError, unescaped_rfind, *(1, 1, 1, 1))
        self.assertRaises(ValueError, unescaped_rfind, *("s", 1, 1, 1))
        self.assertRaises(ValueError, unescaped_rfind, *("s", "s", "s", "1"))
        self.assertRaises(ValueError, unescaped_rfind, *("s", "s", 0, "s"))

        self.assertEqual(unescaped_rfind("abcde", "c"), 2)
        self.assertEqual(unescaped_rfind("abcde", "c", 1, 3), 2)
        self.assertEqual(unescaped_rfind("abcde", "c", 3, 4), -1)
        self.assertEqual(unescaped_rfind("abcde", "z"), -1)
        self.assertEqual(unescaped_rfind("acb\\cdec", "c"), 7)
        self.assertEqual(unescaped_rfind("acb\\cde\\c", "c"), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)

