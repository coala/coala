import unittest

from pyprint.NullPrinter import NullPrinter

from coalib.output.Interactions import fail_acquire_settings
from coalib.output.printers.LogPrinter import LogPrinter


class InteractionsTest(unittest.TestCase):

    def test_(self):
        log_printer = LogPrinter(NullPrinter())
        self.assertRaises(TypeError, fail_acquire_settings, log_printer, None)
        self.assertRaises(AssertionError,
                          fail_acquire_settings,
                          log_printer,
                          {'setting': ['description', 'bear']})
        self.assertEqual(fail_acquire_settings(log_printer, {}), None)
