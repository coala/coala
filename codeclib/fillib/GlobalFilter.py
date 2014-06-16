__author__ = 'lasse'

from codeclib.fillib import FilterBase

class GlobalFilter(FilterBase.FilterBase):

    @staticmethod
    def kind():
        return FilterBase.FILTER_KIND.GLOBAL

    def run(self, file_dict):
        """
        Checks the given files.

        :param file_dict: a dictionary of name: file
        :return: TODO ???
        """
        raise NotImplementedError("This function has to be implemented for a runnable filter.")
