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
import os
import tempfile

sys.path.insert(0, ".")
from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.processes.communication.LogMessage import LogMessage
from coalib.output.ConsolePrinter import ConsolePrinter
import unittest


class ConsolePrinterTestCase(unittest.TestCase):
    def test_printing(self):
        self.outputfile = os.path.join(tempfile.gettempdir(), "ConsolePrinterTestFile")
        with open(self.outputfile, "w") as self.handle:
            self.uut = ConsolePrinter(output=self.handle)

            self.uut.print("\ntest", "message", color="green")
            self.uut.print("\ntest", "message", color="greeeeen")
            self.uut.print("\ntest", "message")

        with open(self.outputfile, "r") as self.handle:
            self.assertEqual(self.handle.readlines(),
                             ['\033[0;32m\n',
                              'test message\n',
                              '\033[0m\n',
                              'test message\n',
                              '\n',
                              'test message\n'])

        os.remove(self.outputfile)


if __name__ == '__main__':
    unittest.main(verbosity=2)
