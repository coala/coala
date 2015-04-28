import unittest
import sys

sys.path.insert(0, ".")

from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear
from coalib.settings.SectionFiller import SectionFiller, Section, Setting
from coalib.output.ConsoleInteractor import ConsoleInteractor
from coalib.output.printers.ConsolePrinter import ConsolePrinter

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


class SectionFillerTest(unittest.TestCase):
    def setUp(self):
        self.log_printer = ConsolePrinter()
        self.interactor = ConsoleInteractor(self.log_printer)
        section = Section("test")
        section.append(Setting("key", "val"))
        self.uut = SectionFiller(section,
                                 self.interactor,
                                 self.log_printer)

    def test_raises(self):
        # Construction
        self.assertRaises(TypeError,
                          SectionFiller,
                          0,
                          self.interactor,
                          self.log_printer)

        # Fill section
        self.assertRaises(TypeError, self.uut.fill_section, 0)

    def test_fill_section(self):
        new_section = self.uut.fill_section([LocalTestBear, GlobalTestBear,
                                            "an inappropriate string object "
                                            "here"])

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
