import unittest

from coalib.tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)
from coalib.parsing.StringProcessing import escape


class EscapeTest(StringProcessingTestBase):
    # Test escape() using a single character to escape and default parameters.

    def test_normal_behaviour(self):
        expected_results = [
            r"out1 \'escaped-escape:        \\ \' out2",
            r"out1 \'escaped-quote:         \\' \' out2",
            r"out1 \'escaped-anything:      \X \' out2",
            r"out1 \'two escaped escapes: \\\\ \' out2",
            r"out1 \'escaped-quote at end:   \\'\' out2",
            r"out1 \'escaped-escape at end:  \\\' out2",
            r"out1           \'str1\' out2 \'str2\' out2",
            r"out1 \\'        \'str1\' out2 \'str2\' out2",
            r"out1 \\\\'      \'str1\' out2 \'str2\' out2",
            r"out1 \\        \'str1\' out2 \'str2\' out2",
            r"out1 \\\\      \'str1\' out2 \'str2\' out2",
            r"out1         \\\'str1\' out2 \'str2\' out2",
            r"out1       \\\\\'str1\' out2 \'str2\' out2",
            r"out1           \'str1\'\'str2\'\'str3\' out2",
            r"",
            r"out1 out2 out3",
            self.bs,
            2 * self.bs]

        self.assertResultsEqual(
            escape,
            {(test_string, "'"): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)})

    # Tests escape() with more than one char to escape and an escape sequence
    # that consists of more than one char.
    def test_advanced(self):
        expected_results = [
            r"out()1 'e()scaped-e()scape:        \\ ' out2",
            r"out()1 'e()scaped-quote:         \' ' out2",
            r"out()1 'e()scaped-anything:      \X ' out2",
            r"out()1 'two e()scaped e()scape()s: \\\\ ' out2",
            r"out()1 'e()scaped-quote at end:   \'' out2",
            r"out()1 'e()scaped-e()scape at end:  \\' out2",
            r"out()1           '()str()1' out2 '()str2' out2",
            r"out()1 \'        '()str()1' out2 '()str2' out2",
            r"out()1 \\\'      '()str()1' out2 '()str2' out2",
            r"out()1 \\        '()str()1' out2 '()str2' out2",
            r"out()1 \\\\      '()str()1' out2 '()str2' out2",
            r"out()1         \\'()str()1' out2 '()str2' out2",
            r"out()1       \\\\'()str()1' out2 '()str2' out2",
            r"out()1           '()str()1''()str2''()str()()3' out2",
            r"",
            r"out()1 out2 out()()3",
            self.bs,
            2 * self.bs]

        self.assertResultsEqual(
            escape,
            {(test_string, "1s33", "()"): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)})

    # Tests the realistic case when needing to escape spaces inside a shell
    # with carets.
    def test_windows_shell_space_escape(self):
        expected_results = [
            r"out1^ 'escaped-escape:^ ^ ^ ^ ^ ^ ^ ^ \\^ '^ out2",
            r"out1^ 'escaped-quote:^ ^ ^ ^ ^ ^ ^ ^ ^ \'^ '^ out2",
            r"out1^ 'escaped-anything:^ ^ ^ ^ ^ ^ \X^ '^ out2",
            r"out1^ 'two^ escaped^ escapes:^ \\\\^ '^ out2",
            r"out1^ 'escaped-quote^ at^ end:^ ^ ^ \''^ out2",
            r"out1^ 'escaped-escape^ at^ end:^ ^ \\'^ out2",
            r"out1^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 'str1'^ out2^ 'str2'^ out2",
            r"out1^ \'^ ^ ^ ^ ^ ^ ^ ^ 'str1'^ out2^ 'str2'^ out2",
            r"out1^ \\\'^ ^ ^ ^ ^ ^ 'str1'^ out2^ 'str2'^ out2",
            r"out1^ \\^ ^ ^ ^ ^ ^ ^ ^ 'str1'^ out2^ 'str2'^ out2",
            r"out1^ \\\\^ ^ ^ ^ ^ ^ 'str1'^ out2^ 'str2'^ out2",
            r"out1^ ^ ^ ^ ^ ^ ^ ^ ^ \\'str1'^ out2^ 'str2'^ out2",
            r"out1^ ^ ^ ^ ^ ^ ^ \\\\'str1'^ out2^ 'str2'^ out2",
            r"out1^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 'str1''str2''str3'^ out2",
            r"",
            r"out1^ out2^ out3",
            self.bs,
            2 * self.bs]

        self.assertResultsEqual(
            escape,
            {(test_string, " ", "^"): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)})

    # Tests using iterators instead of strings for the chars to escape. This
    # allows to escape complete strings and not only chars.
    def test_iterators_not_strings(self):
        expected_results = [
            r"\out1 'escaped-escape:        \\ ' out2",
            r"\out1 'escaped-quote:         \' ' out2",
            r"\out1 'escaped-anything:      \X ' out2",
            r"\out1 'two escaped escapes: \\\\ ' out2",
            r"\out1 'escaped-quote at end:   \'' out2",
            r"\out1 'escaped-escape at end:  \\' out2",
            r"\out1           'str1' out2 '\str2' out2",
            r"\out1 \'        'str1' out2 '\str2' out2",
            r"\out1 \\\'      'str1' out2 '\str2' out2",
            r"\out1 \\        'str1' out2 '\str2' out2",
            r"\out1 \\\\      'str1' out2 '\str2' out2",
            r"\out1         \\'str1' out2 '\str2' out2",
            r"\out1       \\\\'str1' out2 '\str2' out2",
            r"\out1           'str1''\str2''str3' out2",
            r"",
            r"\out1 out2 out3",
            self.bs,
            2 * self.bs]

        self.assertResultsEqual(
            escape,
            {(test_string, ("out1", "str2")): result
             for test_string, result in zip(self.test_strings,
                                            expected_results)})


if __name__ == '__main__':
    unittest.main(verbosity=2)
