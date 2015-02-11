from coalib.bears.Bear import Bear
import inspect
import multiprocessing
from coalib.settings.Section import Section

class TestBear(Bear):
    def __init__(self):
        Bear.__init__(self, Section("settings"), multiprocessing.Queue())

    @staticmethod
    def kind():
        return "kind"

    def origin(self):
        return inspect.getfile(inspect.currentframe())


class NoKind():
    def __init__(self):
        pass

    @staticmethod
    def kind():
        raise NotImplementedError
