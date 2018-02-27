import unittest

from testfixtures import LogCapture

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.processes.DebugProcessing import Queue
from coalib.processes.communication.LogMessage import LogMessage


class DebugProcessingTest(unittest.TestCase):

    def test_queue_put(self):
        log_queue = Queue()
        log_message_item = LogMessage(LOG_LEVEL.INFO, 'Sample message')
        with LogCapture() as capture:
            log_queue.put(log_message_item)
            capture.check(
                ('root', 'INFO', 'Sample message'),
            )
