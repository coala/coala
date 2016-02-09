import re
import unittest

from coalib.parsing.StringProcessing.Filters import trim_empty_matches


class TrimEmptyMatchesTest(unittest.TestCase):
    # Maps the given iterator of MatchObject's to their zero-group, so it can
    # be compared and collects the results into a tuple.
    comparable_map = lambda matches: tuple(map(lambda x: x.group(0), matches))

    def test_single_group(self):
        comparable_map = TrimEmptyMatchesTest.comparable_map

        teststring = "AHelloB   s A B ABAB do what you want."
        regex = "A(.*?)B"

        # Using the iterator itself would require to invoke re.finditer again
        # and again before each assert.
        real = tuple(re.finditer(regex, teststring))

        # Ensure our regex is working like expected.
        self.assertEqual(comparable_map(real),
                         ("AHelloB", "A B", "AB", "AB"))

        # Default mode checks for group 0.
        self.assertEqual(comparable_map(trim_empty_matches(real)),
                         ("AHelloB", "A B", "AB", "AB"))

        self.assertEqual(comparable_map(trim_empty_matches(real, (1,))),
                         ("AHelloB", "A B"))

        self.assertEqual(comparable_map(trim_empty_matches(real, (0, 1))),
                         ("AHelloB", "A B", "AB", "AB"))

        self.assertEqual(comparable_map(trim_empty_matches(real, (1, 0))),
                         ("AHelloB", "A B", "AB", "AB"))

    def test_multi_group(self):
        comparable_map = TrimEmptyMatchesTest.comparable_map

        teststring = ("A1B2C3D no match.'~ Awhat doByouCthink??D ABisCD ABCD"
                      "AneverBCmindD  __ ABCXD ABC")
        regex = "A(.*?)B(.*?)C(?P<cd>.*?)D"

        real = tuple(re.finditer(regex, teststring))

        # Check again if our regex works.
        self.assertEqual(comparable_map(real),
                         ("A1B2C3D", "Awhat doByouCthink??D", "ABisCD", "ABCD",
                          "AneverBCmindD", "ABCXD"))

        self.assertEqual(comparable_map(trim_empty_matches(real)),
                         ("A1B2C3D", "Awhat doByouCthink??D", "ABisCD", "ABCD",
                          "AneverBCmindD", "ABCXD"))

        self.assertEqual(comparable_map(trim_empty_matches(real, (1, 3))),
                         ("A1B2C3D", "Awhat doByouCthink??D", "AneverBCmindD",
                          "ABCXD"))

        self.assertEqual(comparable_map(trim_empty_matches(real, (2,))),
                         ("A1B2C3D", "Awhat doByouCthink??D", "ABisCD"))

        self.assertEqual(comparable_map(trim_empty_matches(real, ("cd",))),
                         ("A1B2C3D", "Awhat doByouCthink??D", "AneverBCmindD",
                          "ABCXD"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
