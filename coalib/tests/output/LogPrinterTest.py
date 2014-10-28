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
from datetime import datetime
import unittest
from coalib.misc.StringConstants import StringConstants
from coalib.processes.communication.LogMessage import LogMessage, LOG_LEVEL
from coalib.output.LogPrinter import LogPrinter
from coalib.misc.i18n import _


class TestLogPrinter(LogPrinter):
    def _print(self, output, special_arg="test"):
        return output, special_arg


class LogPrinterTestCase(unittest.TestCase):
    log_message = LogMessage(LOG_LEVEL.ERROR, StringConstants.COMPLEX_TEST_STRING)

    def test_interface(self):
        uut = LogPrinter()
        self.assertRaises(NotImplementedError, uut.log_message, self.log_message)

    def test_logging(self):
        uut = TestLogPrinter("")
        self.assertEqual((str(self.log_message), "special"),
                         uut.log_message(self.log_message, end="", special_arg="special"))

        uut = TestLogPrinter()
        ts = datetime.today()
        self.assertEqual(
            ("[" + _("ERROR") + "][" + ts.strftime("%X") + "] " + StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.log_message(self.log_message, timestamp=ts, end=""))
        self.assertEqual(
            ("[" + _("ERROR") + "][" + ts.strftime("%X") + "] " + StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.log(LOG_LEVEL.ERROR, StringConstants.COMPLEX_TEST_STRING, timestamp=ts, end=""))

        self.assertEqual(
            ("[" + _("DEBUG") + "][" + ts.strftime("%X") + "] " + StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.debug(StringConstants.COMPLEX_TEST_STRING, timestamp=ts, end=""))
        self.assertEqual(
            ("[" + _("WARNING") + "][" + ts.strftime("%X") + "] " + StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.warn(StringConstants.COMPLEX_TEST_STRING, timestamp=ts, end=""))
        self.assertEqual(
            ("[" + _("ERROR") + "][" + ts.strftime("%X") + "] " + StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.err(StringConstants.COMPLEX_TEST_STRING, timestamp=ts, end=""))

        self.assertEqual(("[" + _("ERROR") + "][" + ts.strftime("%X") + "] Something failed.\n\n" +
                          _("Exception was:") + "\n" + StringConstants.COMPLEX_TEST_STRING, "test"),
                         uut.log_exception("Something failed.",
                                           NotImplementedError(StringConstants.COMPLEX_TEST_STRING),
                                           timestamp=ts,
                                           end=""))

    def test_raises(self):
        uut = LogPrinter()
        self.assertRaises(TypeError, uut.log, 5)
        self.assertRaises(TypeError, uut.log_exception, "message", 5)
        self.assertRaises(TypeError, uut.log_message, 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
