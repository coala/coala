import queue
import unittest

from testfixtures import LogCapture

from coalib.processes.LogPrinterThread import LogPrinterThread


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
