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

from coalib.output.ConsolePrinter import ConsolePrinter
from coalib.analysers.GlobalBear import GlobalBear
from coalib.analysers.LocalBear import LocalBear
from coalib.settings.SettingsFiller import SettingsFiller, Outputter, Settings, Setting, LogPrinter

import builtins
_input = builtins.__dict__["input"]
builtins.__dict__["input"] = lambda x: x
from coalib.output.ConsoleOutputter import ConsoleOutputter


class GlobalTestBear(GlobalBear):
    def __init__(self):
        GlobalBear.__init__(self, {}, Settings("irrelevant"), None)

    @staticmethod
    def get_needed_settings():
        return {"global name": "global help text",
                "key": "this setting does exist"}


class LocalTestBear(LocalBear):
    def __init__(self):
        LocalBear.__init__(self, [], "", Settings("irrelevant"), None)

    @staticmethod
    def get_needed_settings():
        return {"local name": "local help text",
                "global name": "this setting is needed by two analyzers"}


class SettingsTestCase(unittest.TestCase):
    def setUp(self):
        settings = Settings("test")
        settings.append(Setting("key", "val"))
        self.uut = SettingsFiller(settings, ConsoleOutputter(), ConsolePrinter())

    def test_raises(self):
        # Construction
        self.assertRaises(TypeError, SettingsFiller, 0               , Outputter(), LogPrinter())
        self.assertRaises(TypeError, SettingsFiller, Settings("test"), 0          , LogPrinter())
        self.assertRaises(TypeError, SettingsFiller, Settings("test"), Outputter(), 0           )

        # Fill Settings
        self.assertRaises(TypeError, self.uut.fill_settings, 0)

    def test_fill_settings(self):
        new_settings = self.uut.fill_settings([LocalTestBear, GlobalTestBear,
                                               "an inappropriate string object here"])

        self.assertTrue("local name" in new_settings)
        self.assertTrue("global name" in new_settings)
        self.assertEqual(new_settings["key"].value, "val")
        self.assertEqual(len(new_settings.contents), 3)

        # Shouldnt change anything the second time
        new_settings = self.uut.fill_settings([LocalTestBear, GlobalTestBear])

        self.assertTrue("local name" in new_settings)
        self.assertTrue("global name" in new_settings)
        self.assertEqual(new_settings["key"].value, "val")
        self.assertEqual(len(new_settings.contents), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)

builtins.__dict__["input"] = _input
