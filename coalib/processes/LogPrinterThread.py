import logging
import queue
import threading

from coalib.processes.communication.LogMessage import LogMessage


class LogPrinterThread(threading.Thread):
    """
    This is the Thread object that outputs all log messages it gets from
    its message_queue. Setting obj.running = False will stop within the next
    0.1 seconds.
    """

    def __init__(self, message_queue, log_printer=None):
        threading.Thread.__init__(self)
        self.running = True
        self.message_queue = message_queue

    def run(self):
        while self.running:
            try:
                elem = self.message_queue.get(timeout=0.1)
                if isinstance(elem, LogMessage):
                    logging.log(elem.log_level, elem.message)
                else:
                    logging.info(elem)
            except queue.Empty:
                pass
