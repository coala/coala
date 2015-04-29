import sys
import unittest
sys.path.insert(0, ".")

from coalib.output.printers.ColoredLogPrinter import ColoredLogPrinter


class ColoredLogTestPrinter(ColoredLogPrinter):
    def _print_colored(self, output, color=None, **kwargs):
        pass

    def _print_uncolored(self, output, **kwargs):
        pass


class ColoredLogPrinterTest(unittest.TestCase):
    def test_printer_interface(self):
        self.uut = ColoredLogPrinter()
        self.assertRaises(NotImplementedError, self.uut.warn, "test")

        self.uut = ColoredLogTestPrinter()
        self.uut.warn("test")


if __name__ == '__main__':
    unittest.main(verbosity=2)
