import multiprocessing

from coalib.bears.Bear import Bear
from coalib.settings.Section import Section


class TestBear(Bear):

    def __init__(self):
        Bear.__init__(self, Section('settings'), multiprocessing.Queue())

    @staticmethod
    def kind():
        return 'kind'

    def origin(self):
        return __file__


class NoKind():

    def __init__(self):
        pass

    @staticmethod
    def kind():
        raise NotImplementedError
