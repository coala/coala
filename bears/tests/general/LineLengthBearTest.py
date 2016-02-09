from queue import Queue
import unittest

from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from bears.general.LineLengthBear import LineLengthBear


class LineLengthBearTest(LocalBearTestHelper):

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

    def test_ignore_regex(self):
        self.section['ignore_length_regex'] = 'http://'

        self.assertLineInvalid(self.uut, 'asdasd')
        self.assertLineValid(self.uut, 'http://a.domain.de')


if __name__ == '__main__':
    unittest.main(verbosity=2)
