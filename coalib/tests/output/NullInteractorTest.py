import unittest
import sys

sys.path.insert(0, ".")
from coalib.output.NullInteractor import NullInteractor
from coalib.results.Result import Result


class NullInteractorTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = NullInteractor()

    def test_api(self):
        self.uut.acquire_settings([])
        self.uut.print_result(Result("message", "origin"), {})
        self.uut.did_nothing()
        self.uut.begin_section("name")
        self.assertEqual(self.uut._print_actions([]), (None, None))


if __name__ == '__main__':
    unittest.main(verbosity=2)
