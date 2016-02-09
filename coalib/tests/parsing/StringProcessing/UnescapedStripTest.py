import unittest

from coalib.tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)
from coalib.parsing.StringProcessing import unescaped_rstrip, unescaped_strip


class UnescapedStripTest(StringProcessingTestBase):
    test_strings2 = ("hello\\",
                     "te\\st\\\\",
                     r"A\ ",
                     r"A\       ",
                     r"   A \ \  ",
                     r"    \ A \    ",
                     r"  \\ A",
                     r" \\\\\  ",
                     r" \\\\  ")

    def test_rstrip(self):
        expected_results = ("hello\\",
                            "te\\st\\\\",
                            r"A\ ",
                            r"A\ ",
                            r"   A \ \ ",
                            r"    \ A \ ",
                            r"  \\ A",
                            r" \\\\\ ",
                            " \\\\\\\\")

        self.assertResultsEqual(
            unescaped_rstrip,
            {(test_string,): result
             for test_string, result in zip(self.test_strings2,
                                            expected_results)})

    def test_strip(self):
        expected_results = ("hello\\",
                            "te\\st\\\\",
                            r"A\ ",
                            r"A\ ",
                            r"A \ \ ",
                            r"\ A \ ",
                            r"\\ A",
                            r"\\\\\ ",
                            "\\\\\\\\")

        self.assertResultsEqual(
            unescaped_strip,
            {(test_string,): result
             for test_string, result in zip(self.test_strings2,
                                            expected_results)})

    def test_no_whitespaced_strings(self):
        # When no leading or trailing whitespaces exist, nothing should happen.
        # By the way: self.test_strings comes from the base class.
        self.assertResultsEqual(
            unescaped_strip,
            {(test_string,): test_string
             for test_string in self.test_strings})


if __name__ == '__main__':
    unittest.main(verbosity=2)
