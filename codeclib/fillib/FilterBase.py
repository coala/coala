__author__ = 'lasse'


class FILTER_KIND:
    UNKNOWN = 0
    LOCAL   = 1
    GLOBAL  = 2


class FilterBase(object):
    def __init__(self, settings):
        self.settings = settings

    def tear_up(self):
        pass

    def tear_down(self):
        pass

    @staticmethod
    def kind():
        """
        :return: The kind of the filter
        """
        return FILTER_KIND.UNKNOWN

    @staticmethod
    def get_needed_settings():
        """
        This method has to determine which settings are needed by this filter. The user will be prompted for needed
        settings that are not available in the settings file so don't include settings where a default value would do.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        return {}
