import unittest

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear
from coala_utils.ContextManagers import simulate_console_inputs
from coalib.output.ConsoleInteraction import acquire_settings
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.settings.Section import Section
from coalib.settings.SectionFilling import Setting, fill_section, fill_settings
from tests.TestUtilities import bear_test_module


class GlobalTestBear(GlobalBear):

    def __init__(self):
        GlobalBear.__init__(self, {}, Section('irrelevant'), None)

    @staticmethod
    def get_non_optional_settings():
        return {'global name': 'global help text',
                'key': 'this setting does exist'}


class LocalTestBear(LocalBear):

    def __init__(self):
        LocalBear.__init__(self, [], '', Section('irrelevant'), None)

    @staticmethod
    def get_non_optional_settings():
        return {'local name': 'local help text',
                'global name': 'this setting is needed by two bears'}


class SectionFillingTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = LogPrinter(ConsolePrinter())
        self.section = Section('test')
        self.section.append(Setting('key', 'val'))

    def test_fill_settings(self):
        sections = {'test': self.section}
        with simulate_console_inputs() as generator:
            fill_settings(sections,
                          acquire_settings,
                          self.log_printer)
            self.assertEqual(generator.last_input, -1)

        self.section.append(Setting('bears', 'SpaceConsistencyTestBear'))

        with simulate_console_inputs('True'), bear_test_module():
            local_bears, global_bears = fill_settings(sections,
                                                      acquire_settings,
                                                      self.log_printer)
            self.assertEqual(len(local_bears['test']), 1)
            self.assertEqual(len(global_bears['test']), 0)

        self.assertEqual(bool(self.section['use_spaces']), True)
        self.assertEqual(len(self.section.contents), 3)

    def test_fill_section(self):
        # Use the same value for both because order isn't predictable (uses
        # dict)
        with simulate_console_inputs(0, 0):
            new_section = fill_section(self.section,
                                       acquire_settings,
                                       self.log_printer,
                                       [LocalTestBear,
                                        GlobalTestBear])

        self.assertEqual(int(new_section['local name']), 0)
        self.assertEqual(int(new_section['global name']), 0)
        self.assertEqual(new_section['key'].value, 'val')
        self.assertEqual(len(new_section.contents), 3)

        # Shouldnt change anything the second time
        new_section = fill_section(self.section,
                                   acquire_settings,
                                   self.log_printer,
                                   [LocalTestBear, GlobalTestBear])

        self.assertTrue('local name' in new_section)
        self.assertTrue('global name' in new_section)
        self.assertEqual(new_section['key'].value, 'val')
        self.assertEqual(len(new_section.contents), 3)

    def test_dependency_resolving(self):
        sections = {'test': self.section}
        self.section['bears'] = 'DependentBear'
        with simulate_console_inputs('True'), bear_test_module():
            fill_settings(sections, acquire_settings, self.log_printer)

        self.assertEqual(bool(self.section['use_spaces']), True)
