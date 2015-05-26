import sys

sys.path.insert(0, ".")
from coalib.output.printers.ColorPrinter import ColorPrinter
import unittest


class TestColorPrinter(ColorPrinter):
    def _print_colored(self, output, color=None, **kwargs):
        pass

    def _print_uncolored(self, output, **kwargs):
        raise NotImplementedError


class ColorPrinterTest(unittest.TestCase):
    def test_printer_interface(self):
        self.uut = ColorPrinter()
        self.assertRaises(NotImplementedError, self.uut.print, "test")
        self.assertRaises(NotImplementedError,
                          self.uut.print,
                          "test",
                          color='green')

    def test_force_uncolored(self):
        uut = TestColorPrinter(False)
        with self.assertRaises(NotImplementedError):
            uut.print("test", color="green")

        uut = TestColorPrinter()
        # Doesn't raise
        uut.print("test", color="green")


if __name__ == '__main__':
    unittest.main(verbosity=2)
