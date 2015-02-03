import sys
import tempfile
import os
import unittest

sys.path.insert(0, ".")
from coalib.output.printers.FilePrinter import FilePrinter


class FilePrinterTestCase(unittest.TestCase):
    def setUp(self):
        handle, self.filename = tempfile.mkstemp()
        os.close(handle)  # We don't need the handle provided by mkstemp
        self.uut = FilePrinter(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_construction(self):
        self.assertRaises(TypeError, FilePrinter, 5)

    def test_printing(self):
        self.uut.print("Test value")
        del self.uut
        self.uut = FilePrinter(self.filename)
        self.uut.print("Test value2")
        del self.uut

        with open(self.filename) as file:
            lines = file.readlines()

        self.assertEqual(lines,
                         ["Test value\n",
                          "Test value2\n"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
