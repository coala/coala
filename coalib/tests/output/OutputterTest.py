import unittest
import sys

sys.path.insert(0, ".")
from coalib.output.Outputter import Outputter, Result, LineResult


class OutputterTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = Outputter()

    def test_api(self):
        self.assertRaises(NotImplementedError, self.uut.acquire_settings, "anything")
        self.assertRaises(NotImplementedError, self.uut.print_result, Result("message", "origin"))
        self.assertRaises(NotImplementedError,
                          self.uut.print_result,
                          LineResult("origin", 1, "line", "message", "file"))
        self.assertRaises(TypeError, self.uut.print_result, "anything")

        self.assertRaises(TypeError, self.uut.print_results, 5, {})
        self.assertRaises(TypeError, self.uut.print_results, [], 5)
        self.assertRaises(TypeError, self.uut.print_results, ["test"], {})
        self.assertRaises(NotImplementedError, self.uut.print_results, [Result("message", "origin")], {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
