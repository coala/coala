import os
import unittest
import sys

sys.path.insert(0, ".")
from coalib.parsing.Globbing2 import fnmatch
from coalib.parsing.Globbing2 import _iter_alternatives
from coalib.parsing.Globbing2 import _iter_choices
from coalib.parsing.Globbing2 import _position_is_bracketed


class GlobbingHelperFunctionsTest(unittest.TestCase):
    def test_positions(self):
        # pattern: [bracketed values]
        pattern_positions_dict = {
            "[]": [],
            "[a]": [1],
            "[][]": [1, 2],
            "[]]]": [1],
            "[[[]": [1, 2],
            "[[[][]]]": [1, 2, 5],
            "][": [],
            "][][": [],
            "[!]": [],
            "[!c]": [1, 2]
            }
        for pattern, bracketed_positions in pattern_positions_dict.items():
            for pos in range(len(pattern)):
                if pos in bracketed_positions:
                    self.assertTrue(_position_is_bracketed(pattern, pos))
                else:
                    self.assertFalse(_position_is_bracketed(pattern, pos))

    def test_choices(self):
        # pattern: [choices]
        pattern_choices_dict = {
            "": [""],
            "a": ["a"],
            "a|b": ["a", "b"],
            "a|b|c": ["a", "b", "c"],
            "a|b[|]c": ["a", "b[|]c"],
            "a|[b|c]": ["a", "[b|c]"],
            "a[|b|c]": ["a[|b|c]"],
            "[a|b|c]": ["[a|b|c]"],
            "[a]|[b]|[c]": ["[a]", "[b]", "[c]"],
            "[[a]|[b]|[c]": ["[[a]", "[b]", "[c]"]
            }
        for pattern, choices in pattern_choices_dict.items():
            self.assertEqual(list(_iter_choices(pattern)), choices)

    def test_alternatives(self):
        # patterm: [alternatives]
        pattern_alternatives_dict = {
            "": [""],
            "(ab)": ["ab"],
            "a|b": ["a|b"],
            "()": [""],
            "(|)": [""],
            "(a|b)": ["a", "b"],
            "(a|b|c)": ["a", "b", "c"],
            "a(b|c)": ["ab", "ac"],
            "(a|b)(c|d)": ["ac", "ad", "bc", "bd"],
            "(a|b(c|d)": ["(a|bc", "(a|bd"],
            "(a[|]b)": ["a[|]b"],
            "[(]a|b)": ["[(]a|b)"],
            }
        for pattern, alternatives in pattern_alternatives_dict.items():
            self.assertEqual(sorted(list(_iter_alternatives(pattern))),
                             sorted(alternatives))


class FnmatchTest(unittest.TestCase):
    def _test_fnmatch(self, pattern, matches, non_matches):
        for match in matches:
            self.assertTrue(fnmatch(match, pattern))
        for non_match in non_matches:
            self.assertFalse(fnmatch(non_match, pattern))

    def test_circumflex_in_set(self):
        pattern = "[^abc]"
        matches = ["^", "a", "b", "c"]
        non_matches = ["d", "e", "f", "g"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_negative_set(self):
        pattern = "[!ab]"
        matches = ["c", "d"]
        non_matches = ["a", "b"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_escaped_bracket(self):
        pattern = "[]ab]"
        matches = ["]", "a", "b"]
        non_matches = ["[]ab]", "ab]"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_empty_set(self):
        pattern = "a[]b"
        matches = ["a[]b"]
        non_matches = ["a", "b", "[", "]", "ab"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_home_dir(self):
        pattern = os.path.join("~", "a", "b")
        matches = [os.path.expanduser(os.path.join("~", "a", "b"))]
        non_matches = [os.path.join("~", "a", "b")]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_alternatives(self):
        pattern = "(a|b)"
        matches = ["a", "b"]
        non_matches = ["(a|b)", "a|b"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_set_precedence(self):
        pattern = "(a|[b)]"
        matches = ["(a|b", "(a|)"]
        non_matches = ["a]", "[b]"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_questionmark(self):
        pattern = "a?b"
        matches = ["axb", "ayb"]
        non_matches = ["ab", "aXXb"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_asterisk(self):
        pattern = "a*b"
        matches = ["axb", "ayb"]
        non_matches = ["aXbX", os.path.join("a", "b")]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_double_asterisk(self):
        pattern = "a**b"
        matches = ["axb", "ayb", os.path.join("a", "b")]
        non_matches = ["aXbX"]
        self._test_fnmatch(pattern, matches, non_matches)

if __name__ == '__main__':
    unittest.main(verbosity=2)
