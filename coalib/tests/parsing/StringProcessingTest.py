import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import search_for


class StringProcessingTest(unittest.TestCase):
    def setUp(self):
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


if __name__ == '__main__':
    unittest.main(verbosity=2)

