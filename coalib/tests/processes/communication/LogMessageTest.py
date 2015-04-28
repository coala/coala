import sys

sys.path.insert(0, ".")
from coalib.misc.i18n import _
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.misc.StringConstants import StringConstants
from coalib.processes.communication.LogMessage import LogMessage
import unittest


class LogMessageTest(unittest.TestCase):
    def setUp(self):
        self.uut = LogMessage(LOG_LEVEL.DEBUG, "test", "message")

    def test_construction(self):
        # take a look if defaults are good
        self.assertEqual(self.uut.log_level, LOG_LEVEL.DEBUG)
        self.assertEqual(self.uut.message, "test message")

        # see that arguments are processed right
        self.uut = LogMessage(LOG_LEVEL.WARNING, "   a msg  ")
        self.assertEqual(self.uut.log_level, LOG_LEVEL.WARNING)
        self.assertEqual(self.uut.message, "   a msg")

        self.assertRaises(ValueError, LogMessage, LOG_LEVEL.DEBUG, "")
        self.assertRaises(ValueError, LogMessage, 5, "test")

    def test_to_str(self):
        self.uut.message = StringConstants.COMPLEX_TEST_STRING
        self.uut.log_level = LOG_LEVEL.ERROR
        self.assertEqual(str(self.uut),
                         "[{}] {}".format(_("ERROR"),
                                          StringConstants.COMPLEX_TEST_STRING))
        self.uut.log_level = LOG_LEVEL.WARNING
        self.assertEqual(str(self.uut),
                         "[{}] {}".format(_("WARNING"),
                                          StringConstants.COMPLEX_TEST_STRING))
        self.uut.log_level = LOG_LEVEL.DEBUG
        self.assertEqual(str(self.uut),
                         "[{}] {}".format(_("DEBUG"),
                                          StringConstants.COMPLEX_TEST_STRING))
        self.uut.log_level = 5
        self.assertEqual(str(self.uut),
                         "[{}] {}".format(_("ERROR"),
                                          StringConstants.COMPLEX_TEST_STRING))

    def test_equals(self):
        self.assertEqual(LogMessage(LOG_LEVEL.DEBUG, "test message"),
                         LogMessage(LOG_LEVEL.DEBUG, "test message"))
        self.assertNotEqual(LogMessage(LOG_LEVEL.DEBUG, "test message"),
                            LogMessage(LOG_LEVEL.WARNING, "test message"))
        self.assertNotEqual(LogMessage(LOG_LEVEL.DEBUG, "test message"),
                            LogMessage(LOG_LEVEL.DEBUG, "test"))
        self.assertNotEqual(LogMessage(LOG_LEVEL.DEBUG, "test message"), 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
