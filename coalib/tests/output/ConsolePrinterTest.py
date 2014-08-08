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
from coalib.output.ConsolePrinter import ConsolePrinter
import unittest


class ConsolePrinterTestCase(unittest.TestCase):
    def test_printer_interface(self):
        uut = ConsolePrinter()
        uut.print("\ntest", "message", color="green")
        uut.print("\ntest", "message", color="greeeeen")
        uut.print("\ntest", "message")


if __name__ == '__main__':
    unittest.main(verbosity=2)
