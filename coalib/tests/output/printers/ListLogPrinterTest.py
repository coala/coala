from datetime import datetime
import unittest

from coalib.output.printers.ListLogPrinter import ListLogPrinter
from coalib.processes.communication.LogMessage import LogMessage
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL


class ListLogPrinterTest(unittest.TestCase):

    def test_logging(self):
        uut = ListLogPrinter()
        ts = datetime.today()
        ts_str = ts.strftime("%X")

        uut.log_level = LOG_LEVEL.INFO
        uut.warn("Test value", timestamp=ts)
        uut.print("Test 2", timestamp=ts)  # Should go to INFO
        uut.debug("Test 2", timestamp=ts)  # Should not be logged

        self.assertEqual(uut.logs,
                         [LogMessage(LOG_LEVEL.WARNING,
                                     "Test value",
                                     timestamp=ts),
                          LogMessage(LOG_LEVEL.INFO,
                                     "Test 2",
                                     timestamp=ts)])

        self.assertRaises(TypeError, uut.log_message, "message")
if __name__ == '__main__':
    unittest.main(verbosity=2)
