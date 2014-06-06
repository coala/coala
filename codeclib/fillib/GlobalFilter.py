__author__ = 'lasse'

from codeclib.fillib import FilterBase

class GlobalFilter(FilterBase.FilterBase):
    def __init__(self, settings):
        FilterBase.__init__(settings)

    @staticmethod
    def kind():
        return FilterBase.FILTER_KIND.GLOBAL

    def run(self, file_dict):
        """
        Checks the given files.

        :param file_dict: an ordered dictionary that has the filename as key and the contents (string array) as value
        :return: TODO ???
        """
        raise NotImplementedError("This function has to be implemented for a runnable filter.")
