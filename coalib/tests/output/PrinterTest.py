"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import sys
sys.path.insert(0, ".")
from coalib.output.Printer import Printer
import unittest


class TestPrinter(Printer):
    def _print(self, output, somearg=""):
        return output+somearg


class PrinterTestCase(unittest.TestCase):
    def test_printer_interface(self):
        self.uut = Printer()
        self.assertRaises(NotImplementedError, self.uut.print, "test")

    def test_printer_concatenation(self):
        self.uut = TestPrinter()
        self.assertEqual(self.uut.print("hello", "world", delimiter=" ", end="-", somearg="then"), "hello world-then")
        self.assertEqual(self.uut.print("", "world", delimiter=" ", end="-", somearg="then"), " world-then")
        self.assertEqual(self.uut.print("hello", "world", delimiter="", end="-", somearg="then"), "helloworld-then")
        self.assertEqual(self.uut.print(end=""), "")
        self.assertEqual(self.uut.print(NotImplementedError, end=""), "<class 'NotImplementedError'>")


if __name__ == '__main__':
    unittest.main(verbosity=2)
