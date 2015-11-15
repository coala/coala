from queue import Queue
import sys
import unittest

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.reSTLintBear import reSTLintBear
from coalib.settings.Section import Section


class reSTLintBearTest(LocalBearTestHelper):
    def setUp(self):
        self.uut = reSTLintBear(Section('name'), Queue())

    def test_valid(self):
        self.assertLinesValid(self.uut, ["test\n====\n"])

    def test_invalid(self):
        self.assertLinesInvalid(self.uut, ["test\n==\n"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
