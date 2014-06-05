__author__ = 'lasse'

from codeclib.fillib.results import LineResult
from codeclib.fillib.util.settings import Settings
from codeclib.fillib.filter_base import FilterBase

class KeywordFilter(FilterBase):
    def run(self, filename, file, settings):
        results = []
        assert isinstance(settings, Settings)

        keywords = settings.get("Keywords")
        for i, line in enumerate(file):
            for keyword in keywords:
                if line.find(keyword) > 0:
                    msg = "Keyword " + keyword + " found."
                    results.append(LineResult(filename, i, msg, line))

        return results
