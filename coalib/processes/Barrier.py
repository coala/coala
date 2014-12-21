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


# we measure only python 3.4 coverage
if sys.version_info < (3, 3):  # pragma: no cover
    class Barrier:
        def __init__(self, parties):
            self.parties = parties
            self.__count = multiprocessing.Value('i', 0)
            self.__barrier = multiprocessing.Semaphore(0)

        def wait(self):
            with self.__count.get_lock():
                self.__count.value += 1

                # The last process releases the previous ones and so forth
                if self.__count.value == self.parties:
                    self.__barrier.release()

            self.__barrier.acquire()
            self.__barrier.release()
else:
    from multiprocessing import Barrier
