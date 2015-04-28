import sys
import tempfile
import os
import unittest

sys.path.insert(0, ".")
from coalib.output.printers.FilePrinter import FilePrinter


class FilePrinterTest(unittest.TestCase):
    def setUp(self):
        handle, self.filename = tempfile.mkstemp()
        os.close(handle)  # We don't need the handle provided by mkstemp
        self.uut = FilePrinter(self.filename)

    def tearDown(self):
        self.uut.close()
        os.remove(self.filename)

    def test_construction(self):
        self.assertRaises(TypeError, FilePrinter, 5)

    def test_printing(self):
        self.uut.print("Test value")
        self.uut.close()

        self.uut = FilePrinter(self.filename)
        self.uut.print("Test value2")
        self.uut.close()

        with open(self.filename) as file:
            lines = file.readlines()

        self.assertEqual(lines,
                         ["Test value\n",
                          "Test value2\n"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
