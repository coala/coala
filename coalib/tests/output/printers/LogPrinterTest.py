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


class LogPrinterTestCase(unittest.TestCase):
    log_message = LogMessage(LOG_LEVEL.ERROR,
                             StringConstants.COMPLEX_TEST_STRING)

    def test_interface(self):
        uut = LogPrinter()
        self.assertRaises(NotImplementedError,
                          uut.log_message,
                          self.log_message)
        uut.close()

    def test_logging(self):
        uut = TestLogPrinter(timestamp_format="")
        self.assertEqual(
            (str(self.log_message), "special"),
            uut.log_message(self.log_message, end="", special_arg="special"))

        uut = TestLogPrinter(log_level=LOG_LEVEL.DEBUG)
        ts = datetime.today()
        self.assertEqual(
            ("[" + _("ERROR") + "][" + ts.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.log_message(self.log_message, timestamp=ts, end=""))
        self.assertEqual(
            ("[" + _("ERROR") + "][" + ts.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.log(LOG_LEVEL.ERROR,
                    StringConstants.COMPLEX_TEST_STRING,
                    timestamp=ts,
                    end=""))

        self.assertEqual(
            ("[" + _("DEBUG") + "][" + ts.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.debug(StringConstants.COMPLEX_TEST_STRING,
                      timestamp=ts,
                      end=""))
        uut.log_level = LOG_LEVEL.WARNING
        self.assertEqual(None, uut.debug(StringConstants.COMPLEX_TEST_STRING,
                                         timestamp=ts,
                                         end=""))
        self.assertEqual(
            ("[" + _("WARNING") + "][" + ts.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.warn(StringConstants.COMPLEX_TEST_STRING,
                     timestamp=ts,
                     end=""))
        self.assertEqual(
            ("[" + _("ERROR") + "][" + ts.strftime("%X") + "] " +
             StringConstants.COMPLEX_TEST_STRING, "test"),
            uut.err(StringConstants.COMPLEX_TEST_STRING, timestamp=ts, end=""))

        logged = uut.log_exception(
            "Something failed.",
            NotImplementedError(StringConstants.COMPLEX_TEST_STRING),
            timestamp=ts,
            end="")
        self.assertTrue(logged[0].startswith(
            "[" + _("ERROR") + "][" + ts.strftime("%X") +
            "] Something failed.\n\n" + _("Exception was:") + "\n"))

        uut.close()

    def test_raises(self):
        uut = LogPrinter()
        self.assertRaises(TypeError, uut.log, 5)
        self.assertRaises(TypeError, uut.log_exception, "message", 5)
        self.assertRaises(TypeError, uut.log_message, 5)
        uut.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
