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

import unittest
import sys

sys.path.insert(0, ".")

from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear
from coalib.settings.SectionFiller import SectionFiller, Section, Setting

import builtins

_input = builtins.__dict__["input"]
builtins.__dict__["input"] = lambda x: x


class GlobalTestBear(GlobalBear):
    def __init__(self):
        GlobalBear.__init__(self, {}, Section("irrelevant"), None)

    @staticmethod
    def get_non_optional_settings():
        return {"global name": "global help text",
                "key": "this setting does exist"}


class LocalTestBear(LocalBear):
    def __init__(self):
        LocalBear.__init__(self, [], "", Section("irrelevant"), None)

    @staticmethod
    def get_non_optional_settings():
        return {"local name": "local help text",
                "global name": "this setting is needed by two bears"}


class SectionFillerTestCase(unittest.TestCase):
    def setUp(self):
        section = Section("test")
        section.append(Setting("key", "val"))
        self.uut = SectionFiller(section)

    def test_raises(self):
        # Construction
        self.assertRaises(TypeError, SectionFiller, 0)

        # Fill section
        self.assertRaises(TypeError, self.uut.fill_section, 0)

    def test_fill_section(self):
        new_section = self.uut.fill_section([LocalTestBear, GlobalTestBear,
                                            "an inappropriate string object here"])

        self.assertTrue("local name" in new_section)
        self.assertTrue("global name" in new_section)
        self.assertEqual(new_section["key"].value, "val")
        self.assertEqual(len(new_section.contents), 3)

        # Shouldnt change anything the second time
        new_section = self.uut.fill_section([LocalTestBear, GlobalTestBear])

        self.assertTrue("local name" in new_section)
        self.assertTrue("global name" in new_section)
        self.assertEqual(new_section["key"].value, "val")
        self.assertEqual(len(new_section.contents), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)

builtins.__dict__["input"] = _input
