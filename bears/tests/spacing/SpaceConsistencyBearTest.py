from queue import Queue
import sys

sys.path.insert(0, ".")
import unittest
from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.spacing.SpaceConsistencyBear import (SpaceConsistencyBear,
                                                SpacingHelper)
from coalib.settings.Section import Section


class SpaceConsistencyBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.section.append(Setting("use_spaces", "true"))
        self.uut = SpaceConsistencyBear(self.section, Queue())

    def test_needed_settings(self):
        needed_settings = self.uut.get_non_optional_settings()
        self.assertEqual(len(needed_settings),
                         1 + len(SpacingHelper.get_non_optional_settings()))
        self.assertIn("use_spaces", needed_settings)

    def test_data_sets_spaces(self):
        self.assertLineValid(self.uut, "    t")
        self.assertLineInvalid(self.uut, "t \n")
        self.assertLineInvalid(self.uut, "\tt\n")

    def test_data_sets_tabs(self):
        self.section = Section("test section")
        self.section.append(Setting("use_spaces", "false"))
        self.section.append(Setting("allow_trailing_whitespace", "true"))
        self.uut = SpaceConsistencyBear(self.section, Queue())

        self.assertLineInvalid(self.uut, "    t")
        self.assertLineValid(self.uut, "t \n")
        self.assertLineValid(self.uut, "\tt\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
