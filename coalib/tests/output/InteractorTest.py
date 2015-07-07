import unittest
import sys

sys.path.insert(0, ".")
from coalib.output.Interactor import Interactor
from coalib.output.printers.ConsolePrinter import ConsolePrinter


class InteractorTest(unittest.TestCase):
    def setUp(self):
        self.uut = Interactor(ConsolePrinter())


if __name__ == '__main__':
    unittest.main(verbosity=2)
