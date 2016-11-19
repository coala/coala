import unittest
from unittest import mock
import logging

from pyprint.NullPrinter import NullPrinter
from pyprint.Printer import Printer

from coalib.misc import Constants
from coalib.output.printers.LogPrinter import LogPrinter, LogPrinterMixin
from coalib.processes.communication.LogMessage import LOG_LEVEL, LogMessage


class LogPrinterMixinTest(unittest.TestCase):

    def test_log_message(self):
        uut = LogPrinterMixin()
        self.assertRaises(NotImplementedError, uut.log_message, None)


class LogPrinterTest(unittest.TestCase):
    log_message = LogMessage(LOG_LEVEL.ERROR,
                             Constants.COMPLEX_TEST_STRING)

    def test_get_printer(self):
        self.assertIs(LogPrinter(None).printer, None)
        printer = Printer()
        self.assertIs(LogPrinter(printer).printer, printer)

    def test_logging(self):
        uut = LogPrinter(timestamp_format='')
        uut.logger = mock.MagicMock()
        uut.log_message(self.log_message)

        msg = Constants.COMPLEX_TEST_STRING
        uut.logger.log.assert_called_with(logging.ERROR, msg)

        uut = LogPrinter(log_level=LOG_LEVEL.DEBUG)
        uut.logger = mock.MagicMock()

        uut.log(LOG_LEVEL.ERROR, Constants.COMPLEX_TEST_STRING)
        uut.logger.log.assert_called_with(logging.ERROR, msg)

        uut.debug(Constants.COMPLEX_TEST_STRING, 'd')
        uut.logger.log.assert_called_with(logging.DEBUG, msg + ' d')

        uut.log_level = LOG_LEVEL.DEBUG
        uut.log_exception('Something failed.', NotImplementedError(msg))
        uut.logger.log.assert_any_call(logging.ERROR, 'Something failed.')
        uut.logger.log.assert_called_with(
            logging.INFO,
            'Exception was:\n{exception}: {msg}'.format(
                exception='NotImplementedError',
                msg=msg))

    def test_raises(self):
        uut = LogPrinter(NullPrinter())
        self.assertRaises(TypeError, uut.log, 5)
        self.assertRaises(TypeError, uut.log_exception, 'message', 5)
        self.assertRaises(TypeError, uut.log_message, 5)

    def test_log_level(self):
        uut = LogPrinter()
        self.assertEqual(uut.log_level, logging.DEBUG)
        uut.log_level = logging.INFO
        self.assertEqual(uut.log_level, logging.INFO)

    def test_get_state(self):
        uut = LogPrinter()
        self.assertNotIn('logger', uut.__getstate__())

    def test_set_state(self):
        uut = LogPrinter()
        state = uut.__getstate__()
        uut.__setstate__(state)
        self.assertIs(uut.logger, logging.getLogger())

    def test_no_printer(self):
        uut = LogPrinter()
        self.assertIs(uut.logger, logging.getLogger())
