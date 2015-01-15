"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from queue import Queue
import sys

sys.path.insert(0, ".")
import unittest
from coalib.bears.results.LineResult import LineResult
from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.spacing.SpaceConsistencyBear import SpaceConsistencyBear, SpacingHelper
from coalib.settings.Section import Section
from coalib.misc.i18n import _


class SpaceConsistencyBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.section.append(Setting("UseSpaces", "true"))
        self.uut = SpaceConsistencyBear(self.section, Queue())

    def test_needed_settings(self):
        needed_settings = self.uut.get_non_optional_settings()
        self.assertEqual(len(needed_settings), 1 + len(SpacingHelper.get_non_optional_settings()))
        self.assertIn("UseSpaces", needed_settings)

    def test_data_sets_spaces(self):
        self.assertLineValid(self.uut, "    t")

        self.assertLineYieldsResult(self.uut,
                                    "t \n",
                                    LineResult("SpaceConsistencyBear",
                                               1,
                                               "t \n",
                                               _("Line has trailing whitespace characters"),
                                               "file"),
                                    "file")

        self.assertLineYieldsResult(self.uut,
                                    "\tt\n",
                                    LineResult("SpaceConsistencyBear",
                                               1,
                                               "\tt\n",
                                               _("Line contains one or more tabs"),
                                               "file"),
                                    "file")

    def test_data_sets_tabs(self):
        self.section = Section("test section")
        self.section.append(Setting("UseSpaces", "false"))
        self.section.append(Setting("allowtrailingspaces", "true"))
        self.uut = SpaceConsistencyBear(self.section, Queue())

        self.assertLineYieldsResult(self.uut,
                                    "    t",
                                    LineResult("SpaceConsistencyBear",
                                               1,
                                               "    t\n",
                                               _("Line contains with tab replaceable spaces"),
                                               "file"),
                                    "file")

        self.assertLineValid(self.uut, "t \n")

        self.assertLineValid(self.uut, "\tt\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
