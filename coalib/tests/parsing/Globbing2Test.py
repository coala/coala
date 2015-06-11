import unittest
import sys

sys.path.insert(0, ".")
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
