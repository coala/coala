__author__ = 'lasse'


class FilterBase:
    def __init__(self, settings):
        self.settings = settings

    def tear_up(self):
        pass

    def tear_down(self):
        pass

    @staticmethod
    def get_needed_settings():
        """
        This method has to determine which settings are needed by this filter. The user will be prompted for needed
        settings that are not available in the settings file so don't include settings where a default value would do.

        :return: the list of setting keys needed for this filter
        """
        return []
