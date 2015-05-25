import unittest
import sys

sys.path.insert(0, ".")
from coalib.misc.ContextManagers import (suppress_stdout,
                                         retrieve_stdout,
                                         simulate_console_inputs)


class ContextManagersTest(unittest.TestCase):
    def test_suppress_stdout(self):
        def print_func():
            print("func")
            raise NotImplementedError

        def no_print_func():
            with suppress_stdout():
                print("func")
                raise NotImplementedError

        old_stdout = sys.stdout
        sys.stdout = False

        self.assertRaises(AttributeError, print_func)
        self.assertRaises(NotImplementedError, no_print_func)

        sys.stdout = old_stdout

    def test_retrieve_stdout(self):
        with retrieve_stdout() as sio:
            print("test")
            self.assertEqual(sio.getvalue(), "test\n")

    def test_simulate_console_inputs(self):
        with simulate_console_inputs(0, 1, 2) as generator:
            self.assertEqual(input(), 0)
            self.assertEqual(generator.last_input, 0)
            generator.inputs.append(3)
            self.assertEqual(input(), 1)
            self.assertEqual(input(), 2)
            self.assertEqual(input(), 3)
            self.assertEqual(generator.last_input, 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
