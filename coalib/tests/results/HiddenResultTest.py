import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.HiddenResult import HiddenResult


class ResultTest(unittest.TestCase):
    def test_wrong_types(self):
        uut = HiddenResult("any", "anything")
        self.assertEqual(uut.contents, "anything")


if __name__ == '__main__':
    unittest.main(verbosity=2)
