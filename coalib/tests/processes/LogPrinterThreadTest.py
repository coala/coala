import unittest
import queue
import sys

sys.path.insert(0, ".")
from coalib.processes.LogPrinterThread import LogPrinterThread
from coalib.output.printers.NullPrinter import NullPrinter


class LogPrinterThreadTest(unittest.TestCase):
    def setUp(self):
        log_printer = NullPrinter()
        log_queue = queue.Queue()
        self.uut = LogPrinterThread(log_queue, log_printer)
        log_queue.put(item="Sample message 1")
        log_queue.put(item="Sample message 2")
        log_queue.put(item="Sample message 3")

    def test_size(self):
        self.assertEqual(self.uut.message_queue.qsize(), 3)

    def test_run(self):
        self.uut.start()
        while self.uut.message_queue.qsize() > 0:
            continue
        self.uut.running = False
        self.uut.join()
        self.assertEqual(self.uut.message_queue.qsize(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
