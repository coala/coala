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
        self.log_printer = log_printer

    def run(self):
        while self.running:
            try:
                elem = self.message_queue.get(timeout=0.1)
                if self.log_printer is not None and (
                        self.log_printer.log_message):
                    self.log_printer.log_message(elem)
                elif isinstance(elem, LogMessage):
                    logging.log(elem.log_level, elem.message)
                else:
                    # Using logging.info as default log_level
                    logging.info(elem)
            except queue.Empty:
                pass
