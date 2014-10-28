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
import multiprocessing

import sys

sys.path.insert(0, ".")
from coalib.processes.ProcessSpawner import Process, ProcessSpawner
import unittest


class TestProcess(Process):
    def __init__(self, state, queue):
        self.state = state
        self.queue = queue

    def run(self, arg, ignored=0, kwarg=0):
        self.state += kwarg + arg
        if hasattr(self.queue, "get"):
            self.queue.get()
        exit(self.state)


class ProcessSpawnerTestCase(unittest.TestCase):
    def test_raises(self):
        self.assertRaises(TypeError, ProcessSpawner, "wrong type", 0)
        self.assertRaises(TypeError, ProcessSpawner, TestProcess(1, 1), "wrong type")

    def test_run(self):
        # To hold processes so that they are all reliably active to test num_active_processes
        queue = multiprocessing.Queue()

        proc = TestProcess(1, queue)
        uut = ProcessSpawner(proc, 2)
        self.assertEqual(uut.num_active_processes(), 0)

        uut.run(2, kwarg=1)
        self.assertEqual(uut.num_active_processes(), 2)
        queue.put(1)
        queue.put(1)
        self.assertRaises(RuntimeError, uut.run)
        retvals = uut.join()

        self.assertEqual(uut.num_active_processes(), 0)
        self.assertEqual(retvals, [4, 4])

    def test_auto_job_count(self):
        try:
            job_count = multiprocessing.cpu_count()
        # cpu_count is not implemented for some CPU architectures/OSes
        except NotImplementedError:  # pragma: no cover
            job_count = 2
        uut = ProcessSpawner(TestProcess(1, 1))
        self.assertEqual(uut.num_active_processes(), 0)
        self.assertEqual(len(uut.run_blocking(2, kwarg=1)), job_count)


if __name__ == '__main__':
    unittest.main(verbosity=2)
