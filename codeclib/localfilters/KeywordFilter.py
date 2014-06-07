__author__ = 'lasse'

from codeclib.fillib.results import LineResult
from codeclib.fillib.util.settings import Settings
from codeclib.fillib import LocalFilter


class KeywordFilter(LocalFilter.LocalFilter):
    def run(self, filename, file):
        results = []
        assert isinstance(self.settings, Settings)

        keywords = self.settings.get("Keywords")
        for i, line in enumerate(file):
            for keyword in keywords:
                if line.find(keyword) > 0:
                    msg = "Keyword " + keyword + " found."
       #             results.append(LineResult(filename, i, msg, line))

        return results

    @staticmethod
    def get_needed_settings():
        """
        This method has to determine which settings are needed by this filter. The user will be prompted for needed
        settings that are not available in the settings file so don't include settings where a default value would do.

        :return: the list of setting keys needed for this filter
        """
        return (["Keywords"])

