import os

from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coalib.misc.Constants import Constants
from coalib.parsing.ConfParser import ConfParser


class LanguageDefinition(SectionCreatable):
    def __init__(self, language_family: str, language: str):
        """
        Creates a new LanguageDefinition object from file.

        A Language Definition holds constants which may help parsing the
        language. If you want to write a bear you'll probably want to use those
        definitions to keep your bear independent of the semantics of each
        language.

        :param language_family:               The language family. E.g. C for
                                              C++ and C and C# and so on.
        :param language:                      The actual language (e.g. C++).
        :raises ConfParser.FileNotFoundError: If no definition is available
                                              for the given family.
        :raises KeyError:                     If no definition is available
                                              for the given language.
        """
        SectionCreatable.__init__(self)
        self.language = language.lower()
        filename = os.path.join(Constants.language_definitions,
                                language_family.lower() + ".coalang")
        self.lang_dict = ConfParser().parse(filename)[language.lower()]

    def __getitem__(self, item):
        return self.lang_dict[item]
