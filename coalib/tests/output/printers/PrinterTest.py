import sys

sys.path.insert(0, ".")
from coalib.output.printers.Printer import Printer
import unittest


class TestPrinter(Printer):
    def _print(self, output, somearg=""):
        return output + somearg


class PrinterTestCase(unittest.TestCase):
    def test_printer_interface(self):
        self.uut = Printer()
        self.assertRaises(NotImplementedError, self.uut.print, "test")
        self.uut.close()

    def test_printer_concatenation(self):
        self.uut = TestPrinter()
        self.assertEqual(self.uut.print("hello",
                                        "world",
                                        delimiter=" ",
                                        end="-",
                                        somearg="then"), "hello world-then")
        self.assertEqual(self.uut.print("",
                                        "world",
                                        delimiter=" ",
                                        end="-",
                                        somearg="then"), " world-then")
        self.assertEqual(self.uut.print("hello",
                                        "world",
                                        delimiter="",
                                        end="-",
                                        somearg="then"), "helloworld-then")
        self.assertEqual(self.uut.print(end=""), "")
        self.assertEqual(self.uut.print(NotImplementedError, end=""),
                         "<class 'NotImplementedError'>")
        self.assertEqual(
            self.uut.print("", "", delimiter=NotImplementedError, end=""),
            "<class 'NotImplementedError'>")
        self.assertEqual(self.uut.print("", end=NotImplementedError),
                         "<class 'NotImplementedError'>")
        self.uut.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
