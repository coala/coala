import unittest
import sys
from collections import OrderedDict

sys.path.insert(0, ".")
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.output.ConsoleInteractor import ConsoleInteractor
from coalib.misc.ContextManagers import retrieve_stdout
from coalib.output.ShowBears import show_bears
from bears.misc.KeywordBear import KeywordBear
from bears.misc.LineLengthBear import LineLengthBear
from coalib.bears.Bear import Bear


class SomeglobalBear(Bear):
    def run(self):
        """
        Some Description.
        """
        return None


class ShowBearsTest(unittest.TestCase):
    def setUp(self):
        self.log_printer = ConsolePrinter(print_colored=False)
        self.interactor = ConsoleInteractor(self.log_printer,
                                            print_colored=False)
        self.local_bears = OrderedDict([("default", [KeywordBear]),
                                        ("test", [LineLengthBear,
                                                  KeywordBear])])
        self.global_bears = OrderedDict([("default", [SomeglobalBear]),
                                         ("test", [SomeglobalBear])])

    def test_show_bears(self):
        with retrieve_stdout() as stdout:
            bears = {KeywordBear: ['default', 'test'],
                     LineLengthBear: ['test'],
                     SomeglobalBear: ['default', 'test']}
            self.interactor.show_bears(bears)
            expected_string = stdout.getvalue()
        self.maxDiff = None
        with retrieve_stdout() as stdout:
            show_bears(self.local_bears,
                       self.global_bears,
                       self.interactor.show_bears)
            self.assertEqual(expected_string, stdout.getvalue())


if __name__ == '__main__':
    unittest.main(verbosity=2)
