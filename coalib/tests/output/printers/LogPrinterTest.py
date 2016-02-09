from datetime import datetime
import unittest
from pyprint.Printer import Printer
from pyprint.NullPrinter import NullPrinter

from coalib.misc import Constants
from coalib.processes.communication.LogMessage import LogMessage, LOG_LEVEL
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.StringPrinter import StringPrinter


class LogPrinterTest(unittest.TestCase):
    timestamp = datetime.today()
    log_message = LogMessage(LOG_LEVEL.ERROR,
                             Constants.COMPLEX_TEST_STRING,
                             timestamp=timestamp)

    def test_interface(self):
        uut = LogPrinter(Printer())
        self.assertRaises(NotImplementedError,
                          uut.log_message,
                          self.log_message)

    def test_get_printer(self):
        self.assertIs(LogPrinter(None).printer, None)
        printer = Printer()
        self.assertIs(LogPrinter(printer).printer, printer)

    def test_logging(self):
        uut = LogPrinter(StringPrinter(), timestamp_format="")
        uut.log_message(self.log_message, end="")
        self.assertEqual(uut.printer.string, str(self.log_message))

        uut = LogPrinter(StringPrinter(), log_level=LOG_LEVEL.DEBUG)
        uut.log_message(self.log_message, end="")
        self.assertEqual(
            uut.printer.string,
            "[ERROR][" + self.timestamp.strftime("%X") + "] " +
            Constants.COMPLEX_TEST_STRING)

        uut.printer.clear()
        uut.log(LOG_LEVEL.ERROR,
                Constants.COMPLEX_TEST_STRING,
                timestamp=self.timestamp,
                end="")
        self.assertEqual(
            uut.printer.string,
            "[ERROR][" + self.timestamp.strftime("%X") + "] " +
            Constants.COMPLEX_TEST_STRING)

        uut.printer.clear()
        uut.debug(Constants.COMPLEX_TEST_STRING,
                  "d",
                  timestamp=self.timestamp,
                  end="")
        self.assertEqual(
            uut.printer.string,
            "[DEBUG][" + self.timestamp.strftime("%X") + "] " +
            Constants.COMPLEX_TEST_STRING + " d")

        uut.printer.clear()
        uut.log_level = LOG_LEVEL.INFO
        uut.debug(Constants.COMPLEX_TEST_STRING,
                  timestamp=self.timestamp,
                  end="")
        self.assertEqual(uut.printer.string, "")

        uut.printer.clear()
        uut.info(Constants.COMPLEX_TEST_STRING,
                 "d",
                 timestamp=self.timestamp,
                 end="")
        self.assertEqual(
            uut.printer.string,
            "[INFO][" + self.timestamp.strftime("%X") + "] " +
            Constants.COMPLEX_TEST_STRING + " d")

        uut.log_level = LOG_LEVEL.WARNING
        uut.printer.clear()
        uut.debug(Constants.COMPLEX_TEST_STRING,
                  timestamp=self.timestamp,
                  end="")
        self.assertEqual(uut.printer.string, "")

        uut.printer.clear()
        uut.warn(Constants.COMPLEX_TEST_STRING,
                 "d",
                 timestamp=self.timestamp,
                 end="")
        self.assertEqual(
            uut.printer.string,
            "[WARNING][" + self.timestamp.strftime("%X") + "] " +
            Constants.COMPLEX_TEST_STRING + " d")

        uut.printer.clear()
        uut.err(Constants.COMPLEX_TEST_STRING,
                "d",
                timestamp=self.timestamp,
                end="")
        self.assertEqual(
            uut.printer.string,
            "[ERROR][" + self.timestamp.strftime("%X") + "] " +
            Constants.COMPLEX_TEST_STRING + " d")

        uut.log_level = LOG_LEVEL.DEBUG
        uut.printer.clear()
        uut.log_exception(
            "Something failed.",
            NotImplementedError(Constants.COMPLEX_TEST_STRING),
            timestamp=self.timestamp)
        self.assertTrue(uut.printer.string.startswith(
            "[ERROR][" + self.timestamp.strftime("%X") +
            "] Something failed.\n" +
            "[DEBUG][" + self.timestamp.strftime("%X") +
            "] Exception was:"))

        uut.log_level = LOG_LEVEL.INFO
        uut.printer.clear()
        logged = uut.log_exception(
            "Something failed.",
            NotImplementedError(Constants.COMPLEX_TEST_STRING),
            timestamp=self.timestamp,
            end="")
        self.assertTrue(uut.printer.string.startswith(
            "[ERROR][" + self.timestamp.strftime("%X") +
            "] Something failed."))

    def test_raises(self):
        uut = LogPrinter(NullPrinter())
        self.assertRaises(TypeError, uut.log, 5)
        self.assertRaises(TypeError, uut.log_exception, "message", 5)
        self.assertRaises(TypeError, uut.log_message, 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
