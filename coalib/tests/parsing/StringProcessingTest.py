import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import *

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

    # Test the basic unescaped_split() functionality.
    def test_unescaped_split(self):
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
            [r"out1           ", r"str1", r"", r"str2", r"", r"str3", r" out2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_split(separator_pattern,
                                           self.test_strings[i])
            self.assertEqual(expected_results[i], return_value)

    # Test the unescaped_split() function while variating the max_split
    # parameter.
    def test_unescaped_split_max_split(self):
        separator_pattern = "'"

        # Testing max_split = 1.
        max_split = 1
        expected_results = [
            [r"out1 ", r"escaped-escape:        \\ ' out2"],
            [r"out1 ", r"escaped-quote:         \' ' out2"],
            [r"out1 ", r"escaped-anything:      \X ' out2"],
            [r"out1 ", r"two escaped escapes: \\\\ ' out2"],
            [r"out1 ", r"escaped-quote at end:   \'' out2"],
            [r"out1 ", r"escaped-escape at end:  \\' out2"],
            [r"out1           ", r"str1' out2 'str2' out2"],
            [r"out1 " + self.bs, r"        'str1' out2 'str2' out2"],
            [r"out1 " + 3 * self.bs, r"      'str1' out2 'str2' out2"],
            [r"out1 \\        ", r"str1' out2 'str2' out2"],
            [r"out1 \\\\      ", r"str1' out2 'str2' out2"],
            [r"out1         " + 2 * self.bs, r"str1' out2 'str2' out2"],
            [r"out1       " + 4 * self.bs, r"str1' out2 'str2' out2"],
            [r"out1           ", r"str1''str2''str3' out2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_split(separator_pattern,
                                           self.test_strings[i],
                                           max_split)
            self.assertEqual(expected_results[i], return_value)

        # Testing max_split = 2.
        max_split = 2
        expected_results = [
            [r"out1 ", r"escaped-escape:        \\ ", r" out2"],
            [r"out1 ", r"escaped-quote:         " + self.bs, r" ' out2"],
            [r"out1 ", r"escaped-anything:      \X ", r" out2"],
            [r"out1 ", r"two escaped escapes: \\\\ ", r" out2"],
            [r"out1 ", r"escaped-quote at end:   " + self.bs, r"' out2"],
            [r"out1 ", r"escaped-escape at end:  " + 2 * self.bs, r" out2"],
            [r"out1           ", r"str1", r" out2 'str2' out2"],
            [r"out1 " + self.bs, r"        ", r"str1' out2 'str2' out2"],
            [r"out1 " + 3 * self.bs, r"      ", r"str1' out2 'str2' out2"],
            [r"out1 \\        ", r"str1", r" out2 'str2' out2"],
            [r"out1 \\\\      ", r"str1", r" out2 'str2' out2"],
            [r"out1         " + 2 * self.bs, r"str1", r" out2 'str2' out2"],
            [r"out1       " + 4 * self.bs, r"str1", r" out2 'str2' out2"],
            [r"out1           ", r"str1", r"'str2''str3' out2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_split(separator_pattern,
                                           self.test_strings[i],
                                           max_split)
            self.assertEqual(expected_results[i], return_value)

        # Testing max_split = 10.
        # For the given test string this result should be equal with defining
        # max_split = 0, since we haven't 10 separators in a test string.
        max_split = 10
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
            [r"out1           ", r"str1", r"", r"str2", r"", r"str3", r" out2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_split(separator_pattern,
                                           self.test_strings[i],
                                           max_split)
            self.assertEqual(expected_results[i], return_value)

    # Test the unescaped_split() function with different regex patterns.
    def test_unescaped_split_regex_pattern(self):
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
                r"'**'ac###.#.####-ba"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_split(self.multi_patterns[i],
                                           self.multi_pattern_test_string)
            self.assertEqual(expected_results[i], return_value)

    # Test the unescaped_split() function for its remove_empty_matches feature.
    def test_unescaped_split_auto_trim(self):
        separator = ";"
        expected_results = [
            [],
            [2 * self.bs, 5 * self.bs, r"\\#", r"\\\'", self.bs, 4 * self.bs,
                r"+ios"],
            [r"1", r"2", r"3", r"4", r"5", r"6"],
            [r"1", r"2", r"3", r"4", r"5", r"6", r"7"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_split(separator,
                                           self.auto_trim_test_strings[i],
                                           0,
                                           True)
            self.assertEqual(expected_results[i], return_value)

    # Test the basic escaped_split() functionality.
    def test_escaped_split(self):
        separator_pattern = "'"
        expected_results = [
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
            [r"out1           ", r"str1", r"", r"str2", r"", r"str3", r" out2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_split(separator_pattern,
                                         self.test_strings[i])
            self.assertEqual(expected_results[i], return_value)

    # Test the escaped_split() function while variating the max_split
    # parameter.
    def test_escaped_split_max_split(self):
        separator_pattern = "'"

        # Testing max_split = 1.
        max_split = 1
        expected_results = [
            [r"out1 ", r"escaped-escape:        \\ ' out2"],
            [r"out1 ", r"escaped-quote:         \' ' out2"],
            [r"out1 ", r"escaped-anything:      \X ' out2"],
            [r"out1 ", r"two escaped escapes: \\\\ ' out2"],
            [r"out1 ", r"escaped-quote at end:   \'' out2"],
            [r"out1 ", r"escaped-escape at end:  \\' out2"],
            [r"out1           ", r"str1' out2 'str2' out2"],
            [r"out1 \'        ", r"str1' out2 'str2' out2"],
            [r"out1 \\\'      ", r"str1' out2 'str2' out2"],
            [r"out1 \\        ", r"str1' out2 'str2' out2"],
            [r"out1 \\\\      ", r"str1' out2 'str2' out2"],
            [r"out1         " + 2 * self.bs, r"str1' out2 'str2' out2"],
            [r"out1       " + 4 * self.bs, r"str1' out2 'str2' out2"],
            [r"out1           ", r"str1''str2''str3' out2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_split(separator_pattern,
                                         self.test_strings[i],
                                         max_split)
            self.assertEqual(expected_results[i], return_value)

        # Testing max_split = 2.
        max_split = 2
        expected_results = [
            [r"out1 ", r"escaped-escape:        \\ ", r" out2"],
            [r"out1 ", r"escaped-quote:         \' ", r" out2"],
            [r"out1 ", r"escaped-anything:      \X ", r" out2"],
            [r"out1 ", r"two escaped escapes: \\\\ ", r" out2"],
            [r"out1 ", r"escaped-quote at end:   \'", r" out2"],
            [r"out1 ", r"escaped-escape at end:  " + 2 * self.bs, r" out2"],
            [r"out1           ", r"str1", r" out2 'str2' out2"],
            [r"out1 \'        ", r"str1", r" out2 'str2' out2"],
            [r"out1 \\\'      ", r"str1", r" out2 'str2' out2"],
            [r"out1 \\        ", r"str1", r" out2 'str2' out2"],
            [r"out1 \\\\      ", r"str1", r" out2 'str2' out2"],
            [r"out1         " + 2 * self.bs, r"str1", r" out2 'str2' out2"],
            [r"out1       " + 4 * self.bs, r"str1", r" out2 'str2' out2"],
            [r"out1           ", r"str1", r"'str2''str3' out2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_split(separator_pattern,
                                         self.test_strings[i],
                                         max_split)
            self.assertEqual(expected_results[i], return_value)

        # Testing max_split = 10.
        # For the given test string this result should be equal with defining
        # max_split = 0, since we haven't 10 separators in a test string.
        max_split = 10
        expected_results = [
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
            [r"out1           ", r"str1", r"", r"str2", r"", r"str3", r" out2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_split(separator_pattern,
                                         self.test_strings[i],
                                         max_split)
            self.assertEqual(expected_results[i], return_value)

    # Test the escaped_split() function with different regex patterns.
    def test_escaped_split_regex_pattern(self):
        expected_results = [
            [r"", r"", r"cba###\\13q4ujsabbc\+'**'ac###.#.####-ba"],
            [r"", r"c", r"ccba###\\13q4ujs", r"bc\+'**'ac###.#.####-ba"],
            [r"", r"c", r"ccba###\\13q4ujs", r"bc\+'**'", r"###.#.####-ba"],
            [r"abcabccba###", r"\13q4ujsabbc", r"+'**'ac###.#.####-ba"],
            [r"abcabccba", r"\\13q4ujsabbc\+'**'ac", r".", r".", r"-ba"],
            [r"", r"", r"c", r"", r"cc", r"", r"", r"", r"\13q4ujs", r"", r"",
                r"c\+'**'", r"c", r"", r"", r"", r"", r"-", r"", r""],
            [r"", r"cba###\\13q4ujs", r"\+'**'", r"###.#.####-ba"],
            [r"abcabccba###" + 2 * self.bs, r"3q4ujsabbc\+'**'ac###.#.####-ba"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_split(self.multi_patterns[i],
                                         self.multi_pattern_test_string)
            self.assertEqual(expected_results[i], return_value)

    # Test the escaped_split() function for its remove_empty_matches feature.
    def test_escaped_split_auto_trim(self):
        separator = ";"
        expected_results = [
            [],
            [2 * self.bs, r"\\\\\;\\#", r"\\\'", r"\;\\\\", r"+ios"],
            [r"1", r"2", r"3", r"4", r"5", r"6"],
            [r"1", r"2", r"3", r"4", r"5", r"6", r"7"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_split(separator,
                                         self.auto_trim_test_strings[i],
                                         0,
                                         True)
            self.assertEqual(expected_results[i], return_value)

    # Test the basic unescaped_search_in_between() functionality.
    def test_unescaped_search_in_between(self):
        begin_sequence = "'"
        end_sequence = "'"
        expected_results = [
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
            [r"str1", r"str2", r"str3"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_search_in_between(begin_sequence,
                                                       end_sequence,
                                                       self.test_strings[i])
            self.assertEqual(expected_results[i], return_value)

    # Test the unsecaped_search_in_between() while variating the max_match
    # parameter.
    def test_unescaped_search_in_between_max_match(self):
        begin_sequence = "'"
        end_sequence = "'"

        # Testing max_match = 1
        max_match = 1
        expected_results = [
            [r"escaped-escape:        \\ "],
            [r"escaped-quote:         " + self.bs],
            [r"escaped-anything:      \X "],
            [r"two escaped escapes: \\\\ "],
            [r"escaped-quote at end:   " + self.bs],
            [r"escaped-escape at end:  " + 2 * self.bs],
            [r"str1"],
            [r"        "],
            [r"      "],
            [r"str1"],
            [r"str1"],
            [r"str1"],
            [r"str1"],
            [r"str1"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_search_in_between(begin_sequence,
                                                       end_sequence,
                                                       self.test_strings[i],
                                                       max_match)
            self.assertEqual(expected_results[i], return_value)

        # Testing max_match = 2
        max_match = 2
        expected_results = [
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
            [r"str1", r"str2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_search_in_between(begin_sequence,
                                                       end_sequence,
                                                       self.test_strings[i],
                                                       max_match)
            self.assertEqual(expected_results[i], return_value)

        # Testing max_match = 10
        max_match = 10
        expected_results = [
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
            [r"str1", r"str2", r"str3"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_search_in_between(begin_sequence,
                                                       end_sequence,
                                                       self.test_strings[i],
                                                       max_match)
            self.assertEqual(expected_results[i], return_value)

    # Test the unescaped_search_in_between() function with different regex
    # patterns.
    def test_unescaped_search_in_between_regex_pattern(self):
        expected_results = [
            [r""],
            [r"c"],
            [r"c", r"bc\+'**'"],
            [r""],
            [r"\\13q4ujsabbc\+'**'ac", r"."],
            [r"", r"", r"", r"", r"", r"c\+'**'", r"", r"", r"-"],
            [r"cba###\\13q4ujs"],
            [r"3q4ujsabbc" + self.bs]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            # Use each pattern as begin and end sequence.
            return_value = unescaped_search_in_between(
                self.multi_patterns[i],
                self.multi_patterns[i],
                self.multi_pattern_test_string)
            self.assertEqual(expected_results[i], return_value)

    # Test the unescaped_search_in_between() function for its
    # remove_empty_matches feature.
    def test_unescaped_search_in_between_auto_trim(self):
        begin_sequence = ";"
        end_sequence = ";"
        expected_results = [
            [],
            [5 * self.bs, r"\\\'", self.bs, r"+ios"],
            [r"2", r"4", r"6"],
            [r"2", r"4", r"6"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = unescaped_search_in_between(
                begin_sequence,
                end_sequence,
                self.auto_trim_test_strings[i],
                0,
                True)
            self.assertEqual(expected_results[i], return_value)

    # Test the basic escaped_search_in_between() functionality.
    def test_escaped_search_in_between(self):
        begin_sequence = "'"
        end_sequence = "'"
        expected_results = [
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
            [r"str1", r"str2", r"str3"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_search_in_between(begin_sequence,
                                                     end_sequence,
                                                     self.test_strings[i])
            self.assertEqual(expected_results[i], return_value)

    # Test the secaped_search_in_between() while variating the max_match
    # parameter.
    def test_escaped_search_in_between_max_match(self):
        begin_sequence = "'"
        end_sequence = "'"

        # Testing max_match = 1
        max_match = 1
        expected_results = [
            [r"escaped-escape:        \\ "],
            [r"escaped-quote:         \' "],
            [r"escaped-anything:      \X "],
            [r"two escaped escapes: \\\\ "],
            [r"escaped-quote at end:   \'"],
            [r"escaped-escape at end:  " + 2 * self.bs],
            [r"str1"],
            [r"str1"],
            [r"str1"],
            [r"str1"],
            [r"str1"],
            [r"str1"],
            [r"str1"],
            [r"str1"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_search_in_between(begin_sequence,
                                                     end_sequence,
                                                     self.test_strings[i],
                                                     max_match)
            self.assertEqual(expected_results[i], return_value)

        # Testing max_match = 2
        max_match = 2
        expected_results = [
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
            [r"str1", r"str2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_search_in_between(begin_sequence,
                                                     end_sequence,
                                                     self.test_strings[i],
                                                     max_match)
            self.assertEqual(expected_results[i], return_value)

        # Testing max_match = 10
        max_match = 10
        expected_results = [
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
            [r"str1", r"str2", r"str3"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_search_in_between(begin_sequence,
                                                     end_sequence,
                                                     self.test_strings[i],
                                                     max_match)
            self.assertEqual(expected_results[i], return_value)

    # Test the escaped_search_in_between() function with different regex
    # patterns.
    def test_escaped_search_in_between_regex_pattern(self):
        expected_results = [
            [r""],
            [r"c"],
            [r"c", r"bc\+'**'"],
            [r"\13q4ujsabbc"],
            [r"\\13q4ujsabbc\+'**'ac", r"."],
            [r"", r"", r"", r"", r"", r"c\+'**'", r"", r"", r"-"],
            [r"cba###\\13q4ujs"],
            []
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            # Use each pattern as begin and end sequence.
            return_value = escaped_search_in_between(
                self.multi_patterns[i],
                self.multi_patterns[i],
                self.multi_pattern_test_string)
            self.assertEqual(expected_results[i], return_value)

    # Test the escaped_search_in_between() function for its
    # remove_empty_matches feature.
    def test_escaped_search_in_between_auto_trim(self):
        begin_sequence = ";"
        end_sequence = ";"
        expected_results = [
            [],
            [r"\\\\\;\\#", r"+ios"],
            [r"2", r"4", r"6"],
            [r"2", r"4", r"6"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = escaped_search_in_between(
                begin_sequence,
                end_sequence,
                self.auto_trim_test_strings[i],
                0,
                True)
            self.assertEqual(expected_results[i], return_value)

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
            [r"out1", r"out2"]
        ]

        for i in range(0, len(expected_results)):
            # Execute function under test.
            return_value = search_for(search_pattern, self.test_strings[i])

            # Check each MatchObject. Need to iterate over the return_value
            # since the return value is an iterator object pointing to the
            # MatchObject's.
            n = 0
            for x in return_value:
                self.assertEqual(expected_results[i][n], x.group(0))
                n += 1

if __name__ == '__main__':
    unittest.main(verbosity=2)

