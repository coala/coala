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
sys.path.append(".")
from coalib.misc.i18n import _
from coalib.processes.communication.LOG_LEVEL import LOG_LEVEL
from coalib.processes.communication.LogMessage import LogMessage
import unittest


class LogMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = LogMessage()

    def test_construction(self):
        # take a look if defaults are good
        self.assertEqual(self.uut.log_level, LOG_LEVEL.DEBUG)
        self.assertEqual(self.uut.message, "")

        # see that arguments are processed right
        self.uut = LogMessage(LOG_LEVEL.WARNING, "a msg")
        self.assertEqual(self.uut.log_level, LOG_LEVEL.WARNING)
        self.assertEqual(self.uut.message, "a msg")

    def test_to_str(self):
        self.uut.message = "test message änd umlauts!"
        self.uut.log_level = LOG_LEVEL.ERROR
        self.assertEqual(str(self.uut), "[{}] test message änd umlauts!".format(_("ERROR")))
        self.uut.log_level = LOG_LEVEL.WARNING
        self.assertEqual(str(self.uut), "[{}] test message änd umlauts!".format(_("WARNING")))
        self.uut.log_level = LOG_LEVEL.DEBUG
        self.assertEqual(str(self.uut), "[{}] test message änd umlauts!".format(_("DEBUG")))


if __name__ == '__main__':
    unittest.main(verbosity=2)
