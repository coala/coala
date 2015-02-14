import unittest
import sys

sys.path.insert(0, ".")
from coalib.output.Interactor import Interactor
from coalib.results.Result import Result


class InteractorTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = Interactor()

    def test_api(self):
        self.assertRaises(NotImplementedError, self.uut.acquire_settings, "anything")
        self.assertRaises(NotImplementedError, self.uut.print_result, Result("message", "origin"), {})
        self.assertRaises(NotImplementedError,
                          self.uut.print_result,
                          Result("origin", "line", "message", "file", line_nr=1),
                          {})
        self.assertRaises(NotImplementedError, self.uut.begin_section, "name")
        self.assertRaises(NotImplementedError, self.uut.did_nothing)
        self.assertRaises(TypeError, self.uut.print_results, 5, {})
        self.assertRaises(TypeError, self.uut.print_results, [], 5)
        self.assertRaises(NotImplementedError, self.uut.print_results, [Result("message", "origin")], {})
        self.assertRaises(NotImplementedError, self.uut._print_actions, 5)

        self.uut.print_results([], {})
        self.uut.print_results(["illegal value"], {})

        self.assertEqual(self.uut.get_metadata().non_optional_params, {})
        self.assertEqual(self.uut.get_metadata().optional_params, {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
