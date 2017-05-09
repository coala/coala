import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import search_for
from coalib.parsing.StringProcessing import split
from coalib.parsing.StringProcessing import unescaped_split
from coalib.parsing.StringProcessing import search_in_between
from coalib.parsing.StringProcessing import unescaped_search_in_between


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
        self.setUp_search_for()
        self.setUp_split()
        self.setUp_unescaped_split()
        self.setUp_search_in_between()
        self.setUp_unescaped_search_in_between()

    def setUp_search_for(self):
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

    def setUp_split(self):
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

    def setUp_unescaped_split(self):
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

    def setUp_search_in_between(self):
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

    def setUp_unescaped_search_in_between(self):
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
        separator_pattern = self.test_split_pattern
        expected_results = self.test_split_expected_results

        self.assertEqual(len(expected_results), len(self.test_strings))
        for i in range(0, len(expected_results)):
            return_value = split(separator_pattern,
                                 self.test_strings[i])
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

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

            self.assertEqual(len(expected_results), len(self.test_strings))
            for x in range(0, len(expected_results)):
                return_value = split(separator_pattern,
                                     self.test_strings[x],
                                     max_split)
                self.assertIteratorElementsEqual(iter(expected_results[x]),
                                                 return_value)

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
        separator = self.test_split_auto_trim_pattern
        expected_results = self.test_split_auto_trim_expected_results

        self.assertEqual(len(expected_results),
                         len(self.auto_trim_test_strings))
        for i in range(0, len(expected_results)):
            return_value = split(separator,
                                 self.auto_trim_test_strings[i],
                                 0,
                                 True)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the basic unescaped_split() functionality.
    def test_unescaped_split(self):
        separator_pattern = self.test_unescaped_split_pattern
        expected_results = self.test_unescaped_split_expected_results

        self.assertEqual(len(expected_results), len(self.test_strings))
        for i in range(0, len(expected_results)):
            return_value = unescaped_split(separator_pattern,
                                           self.test_strings[i])
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

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

            self.assertEqual(len(expected_results), len(self.test_strings))
            for x in range(0, len(expected_results)):
                return_value = unescaped_split(separator_pattern,
                                               self.test_strings[x],
                                               max_split)
                self.assertIteratorElementsEqual(iter(expected_results[x]),
                                                 return_value)

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
        separator = self.test_unescaped_split_auto_trim_pattern
        expected_results = self.test_unescaped_split_auto_trim_expected_results

        self.assertEqual(len(expected_results),
                         len(self.auto_trim_test_strings))
        for i in range(0, len(expected_results)):
            return_value = unescaped_split(separator,
                                           self.auto_trim_test_strings[i],
                                           0,
                                           True)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the basic search_in_between() functionality.
    def test_search_in_between(self):
        sequence = self.test_search_in_between_pattern
        expected_results = self.test_search_in_between_expected_results

        self.assertEqual(len(expected_results), len(self.test_strings))
        for i in range(0, len(expected_results)):
            return_value = search_in_between(sequence,
                                             sequence,
                                             self.test_strings[i])
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the search_in_between() while varying the max_match
    # parameter.
    def test_search_in_between_max_match(self):
        sequence = self.test_search_in_between_max_match_pattern
        expected_master_results = (
            self.test_search_in_between_max_match_expected_master_results)

        for max_match in [1, 2, 3, 4, 5, 100]:
            expected_results = [
                expected_master_results[j][0 : max_match]
                for j in range(len(expected_master_results))]

            self.assertEqual(len(expected_results), len(self.test_strings))
            for x in range(0, len(expected_results)):
                return_value = search_in_between(sequence,
                                                 sequence,
                                                 self.test_strings[x],
                                                 max_match)
                self.assertIteratorElementsEqual(iter(expected_results[x]),
                                                 return_value)

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
        sequence = self.test_search_in_between_auto_trim_pattern
        expected_results = (
            self.test_search_in_between_auto_trim_expected_results)

        self.assertEqual(len(expected_results),
                         len(self.auto_trim_test_strings))
        for i in range(0, len(expected_results)):
            return_value = search_in_between(sequence,
                                             sequence,
                                             self.auto_trim_test_strings[i],
                                             0,
                                             True)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the basic unescaped_search_in_between() functionality.
    def test_unescaped_search_in_between(self):
        sequence = self.test_unescaped_search_in_between_pattern
        expected_results = (
            self.test_unescaped_search_in_between_expected_results)

        self.assertEqual(len(expected_results), len(self.test_strings))
        for i in range(0, len(expected_results)):
            return_value = unescaped_search_in_between(sequence,
                                                       sequence,
                                                       self.test_strings[i])
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the unescaped_search_in_between() while varying the max_match
    # parameter.
    def test_unescaped_search_in_between_max_match(self):
        sequence = self.test_unescaped_search_in_between_max_match_pattern

        expected_master_results = (
            self.test_unescaped_search_in_between_max_match_expected_m_results)

        for max_match in [1, 2, 3, 4, 5, 67]:
            expected_results = [
                expected_master_results[j][0 : max_match]
                for j in range(len(expected_master_results))]

            self.assertEqual(len(expected_results), len(self.test_strings))
            for x in range(0, len(expected_results)):
                return_value = unescaped_search_in_between(
                    sequence,
                    sequence,
                    self.test_strings[x],
                    max_match)
                self.assertIteratorElementsEqual(iter(expected_results[x]),
                                                 return_value)

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
        sequence = self.test_unescaped_search_in_between_auto_trim_pattern
        expected_results = (
            self.test_unescaped_search_in_between_auto_trim_expected_results)

        self.assertEqual(len(expected_results),
                         len(self.auto_trim_test_strings))
        for i in range(0, len(expected_results)):
            return_value = unescaped_search_in_between(
                sequence,
                sequence,
                self.auto_trim_test_strings[i],
                0,
                True)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)


if __name__ == '__main__':
    unittest.main(verbosity=2)

