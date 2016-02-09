import unittest
from queue import Queue

from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.general.KeywordBear import KeywordBear
from coalib.settings.Section import Section


class SpaceConsistencyBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.section.append(Setting("cs_keywords", "FIXME, ERROR"))
        self.section.append(Setting("ci_keywords", "todo, warning"))
        self.uut = KeywordBear(self.section, Queue())

    def test_run(self):
        self.assertLinesValid(self.uut, [
            "test line fix me",
            "to do",
            "error fixme"
        ])
        self.assertLineInvalid(self.uut, "test line FIXME")
        self.assertLineInvalid(self.uut, "test line todo")
        self.assertLineInvalid(self.uut, "test line warNING")
        self.assertLineInvalid(self.uut, "test line ERROR")


if __name__ == '__main__':
    unittest.main(verbosity=2)
