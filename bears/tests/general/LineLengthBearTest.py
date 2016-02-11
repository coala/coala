from queue import Queue

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
        self.check_validity(self.uut, [
            "test\n",
            "too\n",
            "er\n",
            "e\n",
            "\n"
        ])
        self.check_validity(self.uut, "testa\n", valid=False)
        self.check_validity(self.uut, "test line\n", valid=False)

    def test_ignore_regex(self):
        self.section['ignore_length_regex'] = 'http://'

        self.check_validity(self.uut, 'asdasd', valid=False)
        self.check_validity(self.uut, 'http://a.domain.de')
