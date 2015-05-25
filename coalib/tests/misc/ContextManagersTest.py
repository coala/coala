import unittest
import sys

sys.path.insert(0, ".")
from coalib.misc.ContextManagers import suppress_stdout, retrieve_stdout


class SuppressStdoutTest(unittest.TestCase):
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


class RetrieveStdoutTest(unittest.TestCase):
    def test_retrieve_stdout(self):
        with retrieve_stdout() as sio:
            print("test")
            self.assertEqual(sio.getvalue(), "test\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
