from queue import Queue
import sys
import unittest

sys.path.insert(0, ".")
from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.LanguageToolBear import LanguageToolBear
from coalib.settings.Section import Section


class SpaceConsistencyBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.section.append(Setting("use_spaces", "true"))
        self.uut = LanguageToolBear(self.section, Queue())

    def test_replacable(self):
        # Can be corrected
        self.assertLineInvalid(self.uut, "  ")

        # Can't be corrected by LT
        self.assertLineInvalid(self.uut, "asdgaasdfgahsadf")

        # Uses a subrules 1 and 2 for smart quotations
        self.assertLineInvalid(self.uut, '"quoted"')

        self.assertLineValid(self.uut, "A correct English sentence sounds "
                                       "nice in everyone's ears.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
