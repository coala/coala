from bear1 import TestBear as ImportedTestBear
import inspect

class SubTestBear(ImportedTestBear):
    def __init__(self):
        ImportedTestBear.__init__(self)

    @staticmethod
    def kind():
        return "kind"

    def origin(self):
        return inspect.getfile(inspect.currentframe())
