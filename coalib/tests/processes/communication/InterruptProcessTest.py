import unittest
import sys
import time
import multiprocessing

sys.path.insert(0, ".")
from coalib.processes.communication.InterruptProcess import interrupt_processes
from coalib.misc.ContextManagers import retrieve_stdout

def runner(queue):
    try:
        while True:
            queue.put("Hello coala", timeout=0.1)
            time.sleep(0.9)
    finally:
        queue.put("End", timeout=0.1)


def runner2(queue):
    try:
        runner(queue)
    finally:
        queue.put("End2", timeout=0.1)


class InterruptProcessTest(unittest.TestCase):
    def test_interrupt_process(self):
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=runner, kwargs={'queue': queue})
        p.start()
        time.sleep(2)
        interrupt_processes(p.pid)
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("End", queue.get(timeout=0.1))
        p.terminate()
        p.join()

    def test_interrupt_process_with_nested_functions(self):
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=runner2, kwargs={'queue': queue})
        p.start()
        time.sleep(2)
        interrupt_processes(p.pid)
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("End", queue.get(timeout=0.1))
        self.assertEqual("End2", queue.get(timeout=0.1))
        p.terminate()
        p.join()


if __name__ == '__main__':
    unittest.main(verbosity=2)
