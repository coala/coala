from queue import Queue
import sys

sys.path.insert(0, ".")
import unittest
from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from bears.misc.LineLengthBear import LineLengthBear


class SpaceConsistencyBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.section.append(Setting("max_line_length", "4"))
        self.uut = LineLengthBear(self.section, Queue())

    def test_run(self):
        self.assertLinesValid(self.uut, [
            "test\n",
            "too\n",
            "er\n",
            "e\n",
            "\n"
        ])
        self.assertLineInvalid(self.uut, "testa\n")
        self.assertLineInvalid(self.uut, "test line\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
