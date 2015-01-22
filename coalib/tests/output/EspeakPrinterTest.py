import sys

sys.path.insert(0, ".")
from coalib.output.EspeakPrinter import EspeakPrinter
import unittest


class EspeakPrinterTestCase(unittest.TestCase):
    def test_voice_printer(self):
        self.uut = EspeakPrinter()
        self.uut.print("The", "espeak", "printer", "works!")


if __name__ == '__main__':
    unittest.main(verbosity=2)
