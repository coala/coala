import sys

sys.path.insert(0, ".")
from coalib.output.printers.ColorPrinter import ColorPrinter
import unittest


class ColorPrinterTest(unittest.TestCase):
    def test_printer_interface(self):
        self.uut = ColorPrinter()
        self.assertRaises(NotImplementedError, self.uut.print, "test")
        self.assertRaises(NotImplementedError,
                          self.uut.print,
                          "test",
                          color='green')


if __name__ == '__main__':
    unittest.main(verbosity=2)
