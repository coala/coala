import sys
from datetime import datetime
import unittest

sys.path.insert(0, ".")
from coalib.misc.StringConstants import StringConstants
from coalib.processes.communication.LogMessage import LogMessage, LOG_LEVEL
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.misc.i18n import _


class TestLogPrinter(LogPrinter):
    def _print(self, output, special_arg="test"):
        return output, special_arg


class LogPrinterTest(unittest.TestCase):
    timestamp = datetime.today()
    log_message = LogMessage(LOG_LEVEL.ERROR,
                             StringConstants.COMPLEX_TEST_STRING,
                             timestamp=timestamp)

    def test_interface(self):
        uut = LogPrinter()
        self.assertRaises(NotImplementedError,
                          uut.log_message,
                          self.log_message)

    def test_logging(self):
        uut = TestLogPrinter(timestamp_format="")
        self.assertEqual(
            (str(self.log_message), "special"),
            uut.log_message(self.log_message, end="", special_arg="special"))

        uut = TestLogPrinter(log_level=LOG_LEVEL.DEBUG)
        self.assertEqual(
            ("[" + _("ERROR") + "][" + self.timestamp.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.log_message(self.log_message, end=""))
        self.assertEqual(
            ("[" + _("ERROR") + "][" + self.timestamp.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.log(LOG_LEVEL.ERROR,
                    StringConstants.COMPLEX_TEST_STRING,
                    timestamp=self.timestamp,
                    end=""))

        self.assertEqual(
            ("[" + _("DEBUG") + "][" + self.timestamp.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING + " d", "test"),
            uut.debug(StringConstants.COMPLEX_TEST_STRING,
                      "d",
                      timestamp=self.timestamp,
                      end=""))
        uut.log_level = LOG_LEVEL.WARNING
        self.assertEqual(None, uut.debug(StringConstants.COMPLEX_TEST_STRING,
                                         timestamp=self.timestamp,
                                         end=""))
        self.assertEqual(
            ("[" + _("WARNING") + "][" + self.timestamp.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING + " d", "test"),
            uut.warn(StringConstants.COMPLEX_TEST_STRING,
                     "d",
                     timestamp=self.timestamp,
                     end=""))
        self.assertEqual(
            ("[" + _("ERROR") + "][" + self.timestamp.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING + " d", "test"),
            uut.err(StringConstants.COMPLEX_TEST_STRING,
                    "d",
                    timestamp=self.timestamp,
                    end=""))

        logged = uut.log_exception(
            "Something failed.",
            NotImplementedError(StringConstants.COMPLEX_TEST_STRING),
            timestamp=self.timestamp,
            end="")
        self.assertTrue(logged[0].startswith(
            "[" + _("ERROR") + "][" + self.timestamp.strftime("%X") +
            "] Something failed.\n\n" + _("Exception was:") + "\n"))

    def test_raises(self):
        uut = LogPrinter()
        self.assertRaises(TypeError, uut.log, 5)
        self.assertRaises(TypeError, uut.log_exception, "message", 5)
        self.assertRaises(TypeError, uut.log_message, 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
