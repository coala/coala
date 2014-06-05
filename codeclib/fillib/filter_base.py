__author__ = 'lasse'

class FilterBase:
    def __init__(self):
        pass

    def tearUp(self):
        pass

    def tearDown(self):
        pass

    def run(self):
        raise NotImplementedError("This function has to be implemented for a runnable filter.")
