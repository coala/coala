import sys
import time

sys.path.insert(0, ".")
import unittest
import multiprocessing

from coalib.processes.Barrier import Barrier


def proc_one(queue, barrier):
    queue.put(1)
    time.sleep(0.1)
    barrier.wait()
    queue.put(2)

def proc_two(queue, barrier):
    queue.put(1)
    barrier.wait()
    queue.put(2)


class BarrierTestCase(unittest.TestCase):
    def test_barrier(self):
        uut = Barrier(parties=2)
        queue = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=proc_one, args=(queue, uut)),
                     multiprocessing.Process(target=proc_two, args=(queue, uut))]
        for proc in processes:
            proc.start()
        for proc in processes:
            proc.join()

        # Order will be wrong (1 2 1 2) if barrier doesn't work
        self.assertEqual(queue.get(), 1)
        self.assertEqual(queue.get(), 1)
        self.assertEqual(queue.get(), 2)
        self.assertEqual(queue.get(), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
