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
from coalib.misc.i18n import _
from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.misc.StringConstants import StringConstants
from coalib.processes.communication.LogMessage import LogMessage
import unittest


class LogMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = LogMessage(LOG_LEVEL.DEBUG, "test message")

    def test_construction(self):
        # take a look if defaults are good
        self.assertEqual(self.uut.log_level, LOG_LEVEL.DEBUG)
        self.assertEqual(self.uut.message, "test message")

        # see that arguments are processed right
        self.uut = LogMessage(LOG_LEVEL.WARNING, "   a msg  ")
        self.assertEqual(self.uut.log_level, LOG_LEVEL.WARNING)
        self.assertEqual(self.uut.message, "a msg")

        self.assertRaises(ValueError, LogMessage, LOG_LEVEL.DEBUG, "")

    def test_to_str(self):
        self.uut.message = StringConstants.COMPLEX_TEST_STRING
        self.uut.log_level = LOG_LEVEL.ERROR
        self.assertEqual(str(self.uut), "[{}] {}".format(_("ERROR"), StringConstants.COMPLEX_TEST_STRING))
        self.uut.log_level = LOG_LEVEL.WARNING
        self.assertEqual(str(self.uut), "[{}] {}".format(_("WARNING"), StringConstants.COMPLEX_TEST_STRING))
        self.uut.log_level = LOG_LEVEL.DEBUG
        self.assertEqual(str(self.uut), "[{}] {}".format(_("DEBUG"), StringConstants.COMPLEX_TEST_STRING))
        self.uut.log_level = 5
        self.assertEqual(str(self.uut), "[{}] {}".format(_("ERROR"), StringConstants.COMPLEX_TEST_STRING))


if __name__ == '__main__':
    unittest.main(verbosity=2)
