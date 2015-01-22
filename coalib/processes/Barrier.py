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
