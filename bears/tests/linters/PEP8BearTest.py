from queue import Queue
import sys
import unittest

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.PEP8Bear import PEP8Bear
from coalib.settings.Section import Section


class PEP8BearTest(LocalBearTestHelper):
    def setUp(self):
        self.uut = PEP8Bear(Section('name'), Queue())

    def test_valid(self):
        self.assertLinesValid(self.uut, ["import sys"])
        self.assertLinesValid(self.uut, ["a = 1 + 1"])

    def test_invalid(self):
        self.assertLinesInvalid(self.uut, [""])
        self.assertLinesInvalid(self.uut, ["a=1+1"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
