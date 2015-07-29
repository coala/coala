import sys
import unittest

sys.path.insert(0, ".")
from coalib.output.Interactions import fail_acquire_settings
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.NullPrinter import NullPrinter


class InteractionsTest(unittest.TestCase):
    def test_(self):
        log_printer = LogPrinter(NullPrinter())
        self.assertRaises(TypeError, fail_acquire_settings, log_printer, None)
        self.assertRaises(AssertionError,
                          fail_acquire_settings,
                          log_printer,
                          {"setting": ["description", "bear"]})
        self.assertEqual(fail_acquire_settings(log_printer, {}), None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
