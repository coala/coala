from bear1 import TestBear as ImportedTestBear


class SubTestBear(ImportedTestBear):

    def __init__(self):
        ImportedTestBear.__init__(self)

    @staticmethod
    def kind():
        return 'kind'

    def origin(self):
        return __file__
