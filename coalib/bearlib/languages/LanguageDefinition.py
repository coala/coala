import os

from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coalib.misc import Constants
from coalib.parsing.ConfParser import ConfParser


LANGUAGE_DICT = {
    'c++': 'cpp',
    'python': 'python3',
    'javascript': 'js'
}


class LanguageDefinition(SectionCreatable):

    def __init__(self, language: str, coalang_dir=None):
        """
        Creates a new LanguageDefinition object from file.

        A Language Definition holds constants which may help parsing the
        language. If you want to write a bear you'll probably want to use those
        definitions to keep your bear independent of the semantics of each
        language.

        You can easily get your language definition by just creating it with
        the name of the language desired:

        >>> list(LanguageDefinition("cpp")['extensions'])
        ['.c', '.cpp', '.h', '.hpp']

        For some languages aliases exist, the name is case insensitive:

        >>> list(LanguageDefinition("C++")['extensions'])
        ['.c', '.cpp', '.h', '.hpp']

        If no language exists, you will get a ``FileNotFoundError``:

        >>> LanguageDefinition("BULLSHIT!")  # +ELLIPSIS
        Traceback (most recent call last):
         ...
        FileNotFoundError: ...

        :param language:           The actual language (e.g. C++).
        :param coalang_dir:        Path to directory with coalang language
                                   definition files. This replaces the default
                                   path if given.
        :raises FileNotFoundError: Raised when no definition is available for
                                   the given language.
        """
        SectionCreatable.__init__(self)
        self.language = language.lower()
        if self.language in LANGUAGE_DICT:
            self.language = LANGUAGE_DICT[self.language]

        coalang_file = os.path.join(
            coalang_dir or Constants.language_definitions,
            self.language + ".coalang")

        self.lang_dict = ConfParser().parse(coalang_file)["default"]

    def __getitem__(self, item):
        return self.lang_dict[item]

    def __contains__(self, item):
        return item in self.lang_dict
