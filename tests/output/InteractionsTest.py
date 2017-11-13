import unittest

from pyprint.NullPrinter import NullPrinter
from testfixtures import LogCapture

from coalib.output.Interactions import fail_acquire_settings
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.settings.Section import Section


class InteractionsTest(unittest.TestCase):

    def test_(self):
        log_printer = LogPrinter(NullPrinter())
        self.assertRaises(TypeError, fail_acquire_settings, log_printer, None)
        self.assertRaises(AssertionError,
                          fail_acquire_settings,
                          log_printer,
                          {'setting': ['description', 'bear']})
        self.assertEqual(fail_acquire_settings(log_printer, {}), None)

    def test_section_deprecation(self):
        section = Section('')
        log_printer = LogPrinter(NullPrinter())
        with LogCapture() as capture:
            fail_acquire_settings(log_printer, {}, section)
            capture.check(
                ('root',
                 'WARNING',
                 'fail_acquire_settings: section parameter '
                 'is deprecated.')
            )
