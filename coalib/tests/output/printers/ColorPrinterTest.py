import sys

sys.path.insert(0, ".")
from coalib.output.printers.ColorPrinter import ColorPrinter
import unittest


class TestColorPrinter(ColorPrinter):
    def __init__(self, *args):
        ColorPrinter.__init__(self, *args)
        self.string = ""

    def _print_colored(self, output, color=None, **kwargs):
        self.string += "HIT"

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

    def test_force_colored(self):
        uut = TestColorPrinter(True)
        uut.print("test", color="red")
        self.assertEqual(uut.string, "HIT")

    def test_force_uncolored(self):
        uut = TestColorPrinter(False)
        with self.assertRaises(NotImplementedError):
            uut.print("test", color="green")

    def test_system_supported(self):
        uut = TestColorPrinter(None)
        # This print should not throw because by default color is every time
        # supported, so it will print colored.
        uut.print("test", color="blue")
        self.assertEqual(uut.string, "HIT")

if __name__ == '__main__':
    unittest.main(verbosity=2)
