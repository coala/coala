from queue import Queue
import sys
import unittest

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.Matlab.MatlabIndentationBear import MatlabIndentationBear
from coalib.settings.Section import Section


class MatlabIndentationBearTest(LocalBearTestHelper):
    def setUp(self):
        self.uut = MatlabIndentationBear(Section('name'), Queue())

    def test_valid(self):
        self.assertLinesValid(self.uut, ["if a ~= b\n", "  a\n", "endif\n"])
        self.assertLinesValid(self.uut, ["if a ~= b\n",
                                         "  a\n",
                                         "  \n",
                                         "else\n",
                                         "  a\n",
                                         "endif\n"])

    def test_invalid(self):
        self.assertLinesInvalid(self.uut, ["  A"])
        self.assertLinesInvalid(self.uut, ["if a ~= b\n", "a\n", "endif\n"])
        self.assertLinesInvalid(self.uut, ["if a ~= b\n", " a\n", "endif\n"])
        self.assertLinesInvalid(self.uut, ["if a ~= b\n",
                                           "  a\n",
                                           "  else\n",
                                           "  a\n",
                                           "endif\n"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
