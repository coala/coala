import os

from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coalib.misc import Constants
from coalib.parsing.ConfParser import ConfParser


class LanguageDefinition(SectionCreatable):

    def __init__(self, language: str, coalang_path=None):
        """
        Creates a new LanguageDefinition object from file.

        A Language Definition holds constants which may help parsing the
        language. If you want to write a bear you'll probably want to use those
        definitions to keep your bear independent of the semantics of each
        language.

        :param language:           The actual language (e.g. C++).
        :coalang_path:             Path to coalang definition for language.
        :raises FileNotFoundError: Raised when no definition is available for
                                   the given family.
        :raises KeyError:          Raised when no definition is available for
                                   the given language.
        """
        SectionCreatable.__init__(self)
        self.language = language.lower()

        if not coalang_path:
            filename = os.path.join(Constants.language_definitions,
                                    language.lower() + ".coalang")
        else:
            filename = coalang_path

        self.lang_dict = ConfParser().parse(filename)["default"]

    def __getitem__(self, item):
        return self.lang_dict[item]

    def __contains__(self, item):
        return item in self.lang_dict
