import unittest
import sys

sys.path.insert(0, ".")
from coalib.parsing.Globbing2 import _position_is_bracketed


class PositionIsBracketedTest(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main(verbosity=2)
