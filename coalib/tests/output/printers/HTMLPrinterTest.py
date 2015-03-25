import sys
import tempfile
import os
import unittest

sys.path.insert(0, ".")
from coalib.output.printers.HTMLPrinter import HTMLPrinter


class HTMLPrinterTestCase(unittest.TestCase):
    def setUp(self):
        handle, self.filename = tempfile.mkstemp()
        os.close(handle)  # We don't need the handle provided by mkstemp
        self.uut = HTMLPrinter(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_construction(self):
        self.assertRaises(TypeError, HTMLPrinter, 5)

    def test_printing(self):
        self.uut = HTMLPrinter(self.filename)

        with open(self.filename) as file:
            lines = file.readlines()

        self.assertEqual(lines,
                         ['<!DOCTYPE html>\n',
                          '<html>\n',
                          '</html>\n'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
