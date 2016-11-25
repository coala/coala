import queue
import unittest

from coala_utils.ContextManagers import retrieve_stdout
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.processes.LogPrinterThread import LogPrinterThread


class TestPrinter(LogPrinter):

    def __init__(self):
        LogPrinter.__init__(self, self)

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
