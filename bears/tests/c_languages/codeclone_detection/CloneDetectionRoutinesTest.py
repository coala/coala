import unittest

from bears.c_languages.codeclone_detection.CloneDetectionRoutines import (
    relative_difference)


class CloneDetectionRoutinesTest(unittest.TestCase):

    def test_relative_difference(self):
        # This test is needed because our exclusion heuristic is grown so
        # good that during our "real code" tests some corner cases just
        # don't happen anymore. For simplicity we're whitebox-testing this
        # function, its whole purpose of life is to return 1 if it should
        # normalize with a zero (second parameter).

        self.assertEqual(relative_difference(0, 1), 0)
        self.assertEqual(relative_difference(1, 1), 1)
        self.assertEqual(relative_difference(0, 0), 1)
        self.assertEqual(relative_difference(1, 0), 1)
        self.assertEqual(relative_difference(0.5, 2), 0.25)


if __name__ == '__main__':
    unittest.main(verbosity=2)
