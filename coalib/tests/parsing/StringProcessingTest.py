import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import search_in_between
from coalib.parsing.StringProcessing import unescaped_search_in_between
from coalib.parsing.StringProcessing import unescape
from coalib.parsing.StringProcessing import position_is_escaped


class StringProcessingTest(unittest.TestCase):
    def setUp(self):
        # The backslash character. Needed since there are limitations when
        # using backslashes at the end of raw-strings in front of the
        # terminating " or '.
        self.bs = "\\"

        # Basic test strings all StringProcessing functions should test.
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
        self.auto_trim_test_pattern = r";"
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
        self.set_up_search_in_between()
        self.set_up_unescaped_search_in_between()
        self.set_up_unescape()

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

        self.test_search_in_between_disabled_regex_pattern = r"\'"
        self.test_search_in_between_disabled_regex_expected_results = (
            [[] for x in range(len(self.test_strings))])

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

        self.test_unescaped_search_in_between_disabled_regex_pattern = r"'()?"
        self.test_unescaped_search_in_between_disabled_regex_expected = (
            [[] for x in range(len(self.test_strings))])

    def set_up_unescape(self):
        self.test_unescape_expected_results = [
            r"out1 'escaped-escape:        \ ' out2",
            r"out1 'escaped-quote:         ' ' out2",
            r"out1 'escaped-anything:      X ' out2",
            r"out1 'two escaped escapes: \\ ' out2",
            r"out1 'escaped-quote at end:   '' out2",
            r"out1 'escaped-escape at end:  \' out2",
            r"out1           'str1' out2 'str2' out2",
            r"out1 '        'str1' out2 'str2' out2",
            r"out1 \'      'str1' out2 'str2' out2",
            r"out1 \        'str1' out2 'str2' out2",
            r"out1 \\      'str1' out2 'str2' out2",
            r"out1         \'str1' out2 'str2' out2",
            r"out1       \\'str1' out2 'str2' out2",
            r"out1           'str1''str2''str3' out2",
            r"",
            r"out1 out2 out3",
            r"",
            self.bs]

    def assertSearchInBetweenEquals(self,
                                    test_strings,
                                    expected_results,
                                    begin,
                                    end,
                                    max_match,
                                    remove_empty_matches,
                                    use_regex):
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
        :param use_regex:            Whether to treat begin and end patterns as
                                     regexes or not.
        """
        self.assertEqual(len(expected_results), len(test_strings))
        for i in range(0, len(expected_results)):
            return_value = search_in_between(begin,
                                             end,
                                             test_strings[i],
                                             max_match,
                                             remove_empty_matches,
                                             use_regex)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    def assertUnescapedSearchInBetweenEquals(self,
                                             test_strings,
                                             expected_results,
                                             begin,
                                             end,
                                             max_match,
                                             remove_empty_matches,
                                             use_regex):
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
        :param use_regex:            Whether to treat begin and end patterns as
                                     regexes or not.
        """
        self.assertEqual(len(expected_results), len(test_strings))
        for i in range(0, len(expected_results)):
            return_value = unescaped_search_in_between(begin,
                                                       end,
                                                       test_strings[i],
                                                       max_match,
                                                       remove_empty_matches,
                                                       use_regex)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    def assertResultsEqual(self,
                           func,
                           invocation_and_results,
                           postprocess=lambda result: result):
        """
        Tests each given invocation against the given results with the
        specified function.

        :param func:                   The function to test.
        :param invocation_and_results: A dict containing the invocation tuple
                                       as key and the result as value.
        :param postprocess:            A function that shall process the
                                       returned result from the tested
                                       function. The function must accept only
                                       one parameter as postprocessing input.
                                       Performs no postprocessing by default.
        """
        for args, result in invocation_and_results.items():
            self.assertEqual(postprocess(func(*args)), result)

    def assertResultsEqualEx(self,
                             func,
                             invocation_and_results,
                             postprocess=lambda result: result):
        """
        Tests each given invocation against the given results with the
        specified function. This is an extended version of assertResultsEqual()
        that supports also **kwargs.

        :param func:                   The function to test.
        :param invocation_and_results: A dict containing the invocation tuple
                                       as key and the result as value. The
                                       tuple contains (args, kwargs).
        :param postprocess:            A function that shall process the
                                       returned result from the tested
                                       function. The function must accept only
                                       one parameter as postprocessing input.
                                       Performs no postprocessing by default.
        """
        for (args, kwargs), result in invocation_and_results.items():
            self.assertEqual(postprocess(func(*args, **kwargs)), result)

    def assertIteratorElementsEqual(self, iterator1, iterator2):
        """
        Checks whether each element in the iterators and their length do equal.

        :param iterator1: The first iterator.
        :param iterator2: The second iterator.
        """
        for x in iterator1:
            self.assertEqual(x, next(iterator2))

        self.assertRaises(StopIteration, next, iterator2)

    # Test the basic search_in_between() functionality.
    def test_search_in_between(self):
        for use_regex in [True, False]:
            self.assertSearchInBetweenEquals(
                self.test_strings,
                self.test_search_in_between_expected_results,
                self.test_search_in_between_pattern,
                self.test_search_in_between_pattern,
                0,
                False,
                use_regex)

    # Test the search_in_between() while varying the max_match
    # parameter.
    def test_search_in_between_max_match(self):
        expected_master_results = (
            self.test_search_in_between_max_match_expected_master_results)

        for max_match in [1, 2, 3, 4, 5, 100]:
            expected_results = [
                expected_master_results[j][0 : max_match]
                for j in range(len(expected_master_results))]

            for use_regex in [True, False]:
                self.assertSearchInBetweenEquals(
                    self.test_strings,
                    expected_results,
                    self.test_search_in_between_max_match_pattern,
                    self.test_search_in_between_max_match_pattern,
                    max_match,
                    False,
                    use_regex)

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
                                             self.multi_pattern_test_string,
                                             0,
                                             False,
                                             True)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the search_in_between() function for its
    # remove_empty_matches feature.
    def test_search_in_between_auto_trim(self):
        for use_regex in [True, False]:
            self.assertSearchInBetweenEquals(
                self.auto_trim_test_strings,
                self.test_search_in_between_auto_trim_expected_results,
                self.test_search_in_between_auto_trim_pattern,
                self.test_search_in_between_auto_trim_pattern,
                0,
                True,
                use_regex)

    # Test the search_in_between() function for its use_regex parameter.
    def test_search_in_between_disabled_regex(self):
        self.assertSearchInBetweenEquals(
            self.test_strings,
            self.test_search_in_between_disabled_regex_expected_results,
            self.test_search_in_between_disabled_regex_pattern,
            self.test_search_in_between_disabled_regex_pattern,
            0,
            True,
            False)

    # Test the basic unescaped_search_in_between() functionality.
    def test_unescaped_search_in_between(self):
        for use_regex in [True, False]:
            self.assertUnescapedSearchInBetweenEquals(
                self.test_strings,
                self.test_unescaped_search_in_between_expected_results,
                self.test_unescaped_search_in_between_pattern,
                self.test_unescaped_search_in_between_pattern,
                0,
                False,
                use_regex)

    # Test the unescaped_search_in_between() while varying the max_match
    # parameter.
    def test_unescaped_search_in_between_max_match(self):
        expected_master_results = (
            self.test_unescaped_search_in_between_max_match_expected_m_results)

        for max_match in [1, 2, 3, 4, 5, 67]:
            expected_results = [
                expected_master_results[j][0 : max_match]
                for j in range(len(expected_master_results))]

            for use_regex in [True, False]:
                self.assertUnescapedSearchInBetweenEquals(
                    self.test_strings,
                    expected_results,
                    self.test_unescaped_search_in_between_max_match_pattern,
                    self.test_unescaped_search_in_between_max_match_pattern,
                    max_match,
                    False,
                    use_regex)

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
                self.multi_pattern_test_string,
                0,
                False,
                True)
            self.assertIteratorElementsEqual(iter(expected_results[i]),
                                             return_value)

    # Test the unescaped_search_in_between() function for its
    # remove_empty_matches feature.
    def test_unescaped_search_in_between_auto_trim(self):
        expected_results = (
            self.test_unescaped_search_in_between_auto_trim_expected_results)

        for use_regex in [True, False]:
            self.assertUnescapedSearchInBetweenEquals(
                self.auto_trim_test_strings,
                expected_results,
                self.test_unescaped_search_in_between_auto_trim_pattern,
                self.test_unescaped_search_in_between_auto_trim_pattern,
                0,
                True,
                use_regex)

    # Test the unescaped_search_in_between() function for its use_regex
    # parameter.
    def test_unescaped_search_in_between_disabled_regex(self):
        self.assertUnescapedSearchInBetweenEquals(
            self.test_strings,
            self.test_unescaped_search_in_between_disabled_regex_expected,
            self.test_unescaped_search_in_between_disabled_regex_pattern,
            self.test_unescaped_search_in_between_disabled_regex_pattern,
            0,
            True,
            False)

    # Test unescape() function.
    def test_unescape(self):
        results = [unescape(elem) for elem in self.test_strings]
        compare = zip(self.test_unescape_expected_results, results)

        for elem in compare:
            self.assertEqual(elem[0], elem[1])

    # Test unescape() for some special possible flaws.
    def test_unescape_custom(self):
        self.assertEqual(unescape("hello\\"), "hello")
        self.assertEqual(unescape("te\st\\\\"), "test\\")
        self.assertEqual(unescape("\\\\\\"), "\\")

    # Test the position_is_escaped() function with a basic test string.
    def test_position_is_escaped(self):
        test_string = r"\\\\\abcabccba###\\13q4ujsabbc\+'**'ac###.#.####-ba"
        result_dict = {
            0: False,
            1: True,
            2: False,
            3: True,
            4: False,
            5: True,
            6: False,
            7: False,
            17: False,
            18: True,
            19: False,
            30: False,
            31: True,
            50: False,
            51: False,
            6666666: False,
            -1: False,
            -20: True,
            -21: False}
        for position, value in result_dict.items():
            self.assertEqual(position_is_escaped(test_string, position), value)

    # Test the position_is_escaped() with more test strings from this class.
    def test_position_is_escaped_advanced(self):
        expected_results = [
            30 * [False] + [True] + 7 * [False],
            30 * [False] + [True] + 7 * [False],
            30 * [False] + [True] + 7 * [False],
            28 * [False] + [True, False, True] + 7 * [False],
            31 * [False] + [True] + 6 * [False],
            31 * [False] + [True] + 6 * [False],
            38 * [False],
            6 * [False] + [True] + 31 * [False],
            6 * [False] + [True, False, True] + 29 * [False],
            6 * [False] + [True] + 31 * [False],
            6 * [False] + [True, False, True] + 29 * [False],
            14 * [False] + [True] + 23 * [False],
            12 * [False] + [True, False, True] + 23 * [False],
            38 * [False],
            [],
            14 * [False],
            [False],
            [False, True]]

        results = [[position_is_escaped(test_string, i)
                    for i in range(len(test_string))]
                   for test_string in self.test_strings]

        zipped = [zip(x, y) for x, y in zip(expected_results, results)]
        flattened = [item for sublist in zipped for item in sublist]

        for elem in flattened:
            self.assertEqual(elem[0], elem[1])

if __name__ == '__main__':
    unittest.main(verbosity=2)

