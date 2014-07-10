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
from argparse import _MutuallyExclusiveGroup
import sys
sys.path.append(".")
import unittest
from coalib.internal.process_managing.Process import Process
from coalib.internal.process_managing.ProcessManager import ProcessManager
import multiprocessing


class TestProcess(Process):
    def __init__(self, state):
        self.state = state

    def run(self):
        self.state += 1
        sys.exit(self.state)


class ProcessManagerTestCase(unittest.TestCase):
    def test_run_and_join(self):
        proc = TestProcess(1)
        uut = ProcessManager(proc, 2)
        uut.run()
        retvals = uut.join()
        self.assertEqual(retvals, [2, 2])


if __name__ == '__main__':
    unittest.main()
