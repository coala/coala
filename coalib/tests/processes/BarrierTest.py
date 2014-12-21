"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

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
