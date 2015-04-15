import unittest
import sys

sys.path.insert(0, ".")
from coalib.output.NullInteractor import NullInteractor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.results.Result import Result


class NullInteractorTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = NullInteractor(ConsolePrinter())

    def test_api(self):
        self.uut.print_result(Result("message", "origin"), {})
        self.uut.print_results([], {})
        self.uut.did_nothing()
        self.uut.begin_section("name")
        self.uut.acquire_settings([])


if __name__ == '__main__':
    unittest.main(verbosity=2)
