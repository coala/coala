import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import *

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

        # The backslash character. Needed since there are limitations when
        # using backslashes at the end of raw-strings in front of the
        # terminating " or '.
        self.bs = "\\"

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

        for i in range(0, len(self.test_strings)):
            # Execute function under test.
            return_value = unescaped_split(separator_pattern,
                                           self.test_strings[i])
            self.assertEqual(expected_results[i], return_value)

if __name__ == '__main__':
    unittest.main(verbosity=2)

