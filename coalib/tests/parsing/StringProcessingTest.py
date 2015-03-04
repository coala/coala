import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import search_for


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

        # Set up test dependent variables.
        self.setUp_search_for()

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


if __name__ == '__main__':
    unittest.main(verbosity=2)

