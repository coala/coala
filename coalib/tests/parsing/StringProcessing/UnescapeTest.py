import unittest

from coalib.tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)
from coalib.parsing.StringProcessing import unescape


class UnescapeTest(StringProcessingTestBase):
    # Test the unescape() function.

    def test_basic(self):
        expected_results = [
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

        self.assertResultsEqual(
            unescape,
            {(test_string,): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)})

    # Test unescape() with custom test strings that could uncover special
    # flaws.
    def test_extended(self):
        self.assertEqual(unescape("hello\\"), "hello")
        self.assertEqual(unescape("te\\st\\\\"), "test\\")
        self.assertEqual(unescape("\\\\\\"), "\\")


if __name__ == '__main__':
    unittest.main(verbosity=2)
