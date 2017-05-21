import queue
import unittest

from testfixtures import LogCapture

from coala_utils.ContextManagers import retrieve_stdout
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.processes.communication.LogMessage import LogMessage
from coalib.processes.LogPrinterThread import LogPrinterThread


class TestPrinter():

    def log_message(self, log_message, timestamp=None, **kwargs):
        print(log_message)


class LogPrinterThreadTest(unittest.TestCase):

    def test_run(self):
        log_printer = TestPrinter()
        log_queue = queue.Queue()
        self.uut = LogPrinterThread(log_queue, log_printer)
        log_queue.put(item='Sample message 1')
        log_queue.put(item='Sample message 2')
        log_queue.put(item='Sample message 3')
        self.assertEqual(self.uut.message_queue.qsize(), 3)
        with retrieve_stdout() as stdout:
            self.uut.start()
            while self.uut.message_queue.qsize() > 0:
                continue
            self.uut.running = False
            self.uut.join()
            self.assertEqual(stdout.getvalue(),
                             'Sample message 1\nSample message 2\nSample '
                             'message 3\n')

    def test_log_message(self):
        log_queue = queue.Queue()
        self.uut = LogPrinterThread(log_queue)
        log_queue.put(LogMessage(LOG_LEVEL.DEBUG, 'Sample message 1'))
        log_queue.put(LogMessage(LOG_LEVEL.DEBUG, 'Sample message 2'))
        log_queue.put(LogMessage(LOG_LEVEL.DEBUG, 'Sample message 3'))
        self.assertEqual(self.uut.message_queue.qsize(), 3)
        with LogCapture() as capture:
            self.uut.start()
            while self.uut.message_queue.qsize() > 0:
                continue
            self.uut.running = False
            self.uut.join()
        capture.check(
            ('root', 'DEBUG', 'Sample message 1'),
            ('root', 'DEBUG', 'Sample message 2'),
            ('root', 'DEBUG', 'Sample message 3'))

    def test_log_str(self):
        log_queue = queue.Queue()
        self.uut = LogPrinterThread(log_queue)
        log_queue.put('Sample message 1')
        log_queue.put('Sample message 2')
        log_queue.put('Sample message 3')
        self.assertEqual(self.uut.message_queue.qsize(), 3)
        with LogCapture() as capture:
            self.uut.start()
            while self.uut.message_queue.qsize() > 0:
                continue
            self.uut.running = False
            self.uut.join()
        capture.check(
            ('root', 'INFO', 'Sample message 1'),
            ('root', 'INFO', 'Sample message 2'),
            ('root', 'INFO', 'Sample message 3'))
