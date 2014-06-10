__author__ = 'lasse'

from codeclib.fillib.results import LineResult
from codeclib.fillib.util.settings import Settings
from codeclib.fillib import LocalFilter


class KeywordFilter(LocalFilter.LocalFilter):

    def run(self, filename, file):
        results = []
        assert isinstance(self.settings, Settings)

        keywords = self.settings["keywords"].value

        for i in range(len(file)):
            for keyword in keywords:
                if file[i].find(keyword) > 0:
                    msg = "Keyword '" + keyword + "' found."
                    results.append(LineResult.LineResult(filename, "KeywordFilter", msg, i+1, file[i]))
        return results

    @staticmethod
    def get_needed_settings():
        """
        This method has to determine which settings are needed by this filter. The user will be prompted for needed
        settings that are not available in the settings file so don't include settings where a default value would do.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        return {"Keywords": "Keywords to raise warnings for in files"}

