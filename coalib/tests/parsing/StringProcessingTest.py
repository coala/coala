import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import search_for
from coalib.parsing.StringProcessing import split


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
            r"out1           'str1''str2''str3' out2"]

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
            r"1;2;3;4;5;6;7"]

    def assertSearchForResultEqual(self,
                                   pattern,
                                   test_strings,
                                   expected_strings,
                                   max_matches = 0,
                                   flags = 0):
        """
        Checks whether the given test_strings do equal the expected_strings
        after feeding search_for() with them.

        :param pattern:          The pattern to pass to search_for().
        :param test_strings:     The test string to pass to search_for().
        :param expected_strings: The expected results to make the asserts for.
        :param max_matches:      Passed to the parameter max_matches in
                                 search_for().
        :param flags:            Passed to the parameter flags in search_for().
        """
        self.assertEqual(len(expected_strings), len(test_strings))
        for i in range(0, len(expected_strings)):
            return_value = search_for(pattern,
                                      test_strings[i],
                                      max_matches,
                                      flags)

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
        # Match either "out1" or "out2".
        search_pattern = "out1|out2"
        # These are the expected results for the zero-group of the
        # returned MatchObject's.
        expected_results = [
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
            [r"out1", r"out2"]]

        self.assertSearchForResultEqual(search_pattern,
                                        self.test_strings,
                                        expected_results)

    # Test the generator function branched into from search_for().
    def test_search_for_generator_branch(self):
        search_pattern = "'"
        expected_results = [
            i * [r"'"] for i in [2, 3, 2, 2, 3, 2, 4, 5, 5, 4, 4, 4, 4, 6]]

        # To test the generator function used by search_for() we need to limit
        # the max_matches to branch into it.
        self.assertSearchForResultEqual(search_pattern,
                                        self.test_strings,
                                        expected_results,
                                        1000)

    # Test search_for() with empty pattern for generator function branch.
    def test_search_for_generator_branch_empty_pattern(self):
        search_pattern = ""
        expected_results = [
            (len(elem) + 1) * [r""] for elem in self.test_strings]

        # Limit again the max_matches to branch into the generator function.
        self.assertSearchForResultEqual(search_pattern,
                                        self.test_strings,
                                        expected_results,
                                        1000)

    # Test the search_for() function while varying the max_matches parameter.
    def test_search_for_max_matches(self):
        search_pattern = "out1|out2"
        expected_master_results = [
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
            [r"out1", r"out2"]]

        for i in range(1, 100):
            expected_results = [
                expected_master_results[j][0 : i]
                    for j in range(len(expected_master_results))]
            self.assertSearchForResultEqual(search_pattern,
                                            self.test_strings,
                                            expected_results,
                                            i)

    # Test what happens when providing a negative max_match parameter for
    # search_for().
    def test_search_for_negative_max_match(self):
        search_pattern = "'"
        # Shall throw ValueError each time.
        for teststr in self.test_strings:
            self.assertRaises(ValueError,
                              search_for,
                              search_pattern,
                              teststr,
                              -1)
            # The same with a crazier number.
            self.assertRaises(ValueError,
                              search_for,
                              search_pattern,
                              teststr,
                              -43287982374112)

    # Test the basic split() functionality.
    def test_split(self):
        separator_pattern = "'"
        expected_results = [
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
                r" out2"]]

        self.assertEqual(len(expected_results), len(self.test_strings))
        for i in range(0, len(expected_results)):
            return_value = split(separator_pattern,
                                 self.test_strings[i])
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the split() function while varying the max_split parameter.
    def test_split_max_split(self):
        separator_pattern = "'"
        expected_master_results = [
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
                r" out2"]]

        for max_split in range(1, 100):
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
        expected_results = [
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

        self.assertEqual(len(expected_results), len(self.multi_patterns))
        for i in range(0, len(expected_results)):
            return_value = split(self.multi_patterns[i],
                                 self.multi_pattern_test_string)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the split() function for its remove_empty_matches feature.
    def test_split_auto_trim(self):
        separator = ";"
        expected_results = [
            [],
            [2 * self.bs, 5 * self.bs, r"\\#", r"\\\'", self.bs, 4 * self.bs,
                r"+ios"],
            [r"1", r"2", r"3", r"4", r"5", r"6"],
            [r"1", r"2", r"3", r"4", r"5", r"6", r"7"]]

        self.assertEqual(len(expected_results),
                         len(self.auto_trim_test_strings))
        for i in range(0, len(expected_results)):
            return_value = split(separator,
                                 self.auto_trim_test_strings[i],
                                 0,
                                 True)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)


if __name__ == '__main__':
    unittest.main(verbosity=2)

