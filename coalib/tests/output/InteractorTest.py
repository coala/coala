import unittest
import sys

sys.path.insert(0, ".")
from coalib.output.Interactor import Interactor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.results.Result import Result


class InteractorTest(unittest.TestCase):
    def setUp(self):
        self.uut = Interactor(ConsolePrinter())

    def test_api(self):
        self.assertRaises(NotImplementedError,
                          self.uut.acquire_settings,
                          "anything")
        self.assertRaises(NotImplementedError, self.uut.begin_section, "name")
        self.assertRaises(NotImplementedError, self.uut.show_bears, {})
        self.assertRaises(NotImplementedError, self.uut.did_nothing)
        self.assertRaises(NotImplementedError, self.uut._print_actions, 5)
        self.assertRaises(NotImplementedError,
                          self.uut._print_action_failed,
                          "t",
                          Exception())


if __name__ == '__main__':
    unittest.main(verbosity=2)
