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
