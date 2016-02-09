from shutil import which
from unittest.case import skipIf

from coalib.output.printers.EspeakPrinter import EspeakPrinter
import unittest


@skipIf(which('espeak') is None, 'eSpeak is not installed.')
class EspeakPrinterTest(unittest.TestCase):

    def test_voice_printer(self):
        self.uut = EspeakPrinter()
        self.uut.print("The", "espeak", "printer", "works!")
        self.uut.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
