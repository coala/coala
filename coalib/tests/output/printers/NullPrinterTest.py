import unittest
import sys

sys.path.insert(0, ".")
from coalib.output.printers.NullPrinter import NullPrinter


class NullPrinterTest(unittest.TestCase):
    def test_non_printing(self):
        self.uut = NullPrinter()
        self.assertEqual(self.uut.print("anything"), None)
        self.assertEqual(self.uut.print("anything", color="red"), None)
        self.assertEqual(self.uut.debug("message"), None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
