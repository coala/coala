from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.misc.i18n import _
from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition


class SimpleAnnotationBear(LocalBear):
    def run(self,
            filename,
            file,
            language_family: str,
            language: str):
        '''
        TODO
        '''
        definition = LanguageDefinition(language_family, language)
        for line_number, line in enumerate(file, start):
            pass
