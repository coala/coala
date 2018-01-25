import queue
import unittest

from testfixtures import LogCapture

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.processes.LogPrinterThread import LogPrinterThread
from coalib.processes.communication.LogMessage import LogMessage


class LogPrinterThreadTest(unittest.TestCase):

    def test_run(self):
        log_queue = queue.Queue()
        self.uut = LogPrinterThread(log_queue)
        log_queue.put(item='Sample message 1')
        log_queue.put(item='Sample message 2')
        log_queue.put(item='Sample message 3')
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
            ('root', 'INFO', 'Sample message 3')
        )

    def test_run_log_message_instance(self):
        log_queue = queue.Queue()
        log_message_item = LogMessage(LOG_LEVEL.INFO, 'Sample message')
        log_queue.put(log_message_item)
        self.uut = LogPrinterThread(log_queue)
        with LogCapture() as capture:
            self.uut.start()
            capture.check(
                ('root', 'INFO', 'Sample message'),
            )
