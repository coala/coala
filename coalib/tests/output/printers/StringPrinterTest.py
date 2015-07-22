import sys
import unittest

sys.path.insert(0, ".")
from coalib.misc.Constants import Constants
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.printers.StringPrinter import StringPrinter


class StringPrinterTest(unittest.TestCase):
    def test_construction(self):
        uut = StringPrinter()
        self.assertEqual(uut.string, "")

    def test_printing(self):
        uut = StringPrinter()
        self.assertEqual(uut.string, "")

        uut.print("ABC")
        self.assertEqual(uut.string, "ABC\n")

        uut.print("XYZ")
        self.assertEqual(uut.string, "ABC\nXYZ\n")

        uut.print("\nHello World.")
        self.assertEqual(uut.string, "ABC\nXYZ\n\nHello World.\n")

    def test_clear(self):
        uut = StringPrinter()
        self.assertEqual(uut.string, "")

        uut.clear()
        self.assertEqual(uut.string, "")

        uut.print("1")
        self.assertEqual(uut.string, "1\n")
        uut.clear()
        self.assertEqual(uut.string, "")

        uut.print(1000 * "#")
        self.assertEqual(uut.string, 1000 * "#" + "\n")
        uut.clear()
        self.assertEqual(uut.string, "")

    def test_logging(self):
        uut = StringPrinter()
        uut.log(LOG_LEVEL.ERROR, "Log message")
        self.assertIn("Log message", uut.string)

        uut.log(LOG_LEVEL.WARNING, "My custom log message.")
        self.assertIn("Log message", uut.string)
        self.assertIn("My custom log message.", uut.string)

        uut.clear()
        uut.log(LOG_LEVEL.WARNING, "1-1-2-3-5-8-13-21-34-55")
        self.assertNotIn("Log message", uut.string)
        self.assertNotIn("My custom log message.", uut.string)
        self.assertIn("1-1-2-3-5-8-13-21-34-55", uut.string)

    def test_logging_with_complex_string(self):
        uut = StringPrinter()
        self.assertNotIn(Constants.COMPLEX_TEST_STRING, uut.string)
        uut.log(LOG_LEVEL.ERROR, Constants.COMPLEX_TEST_STRING)
        self.assertIn(Constants.COMPLEX_TEST_STRING, uut.string)


if __name__ == '__main__':
    unittest.main(verbosity=2)
