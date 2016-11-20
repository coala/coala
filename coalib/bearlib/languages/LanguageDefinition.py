import logging

from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coalib.bearlib.languages import Language


class LanguageDefinition(SectionCreatable):

    def __init__(self, language: str, coalang_dir=None):
        """
        Creates a new LanguageDefinition object from file.

        THIS FUNCTION IS DEPRECATED. Use the Language class instead.

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

        >>> LanguageDefinition("BULLSHIT!")
        Traceback (most recent call last):
         ...
        FileNotFoundError

        Custom coalangs are no longer supported. You can simply register your
        languages to the Languages decorator. When giving a custom coalang
        directory a warning will be emitted and it will attempt to load the
        given Language anyway through conventional means:

        >>> LanguageDefinition("custom", coalang_dir='somewhere')
        Traceback (most recent call last):
         ...
        FileNotFoundError

        :param language:           The actual language (e.g. C++).
        :param coalang_dir:        Path to directory with coalang language
                                   definition files. This replaces the default
                                   path if given.
        :raises FileNotFoundError: Raised when no definition is available for
                                   the given language.
        """
        logging.debug('LanguageDefinition has been deprecated! '
                      'Use `coalib.bearlib.languages.Language` instead.')
        if coalang_dir:
            logging.error(
                'LanguageDefinition has been deprecated. The `coalang_dir` '
                'functionality is not available anymore.')
        try:
            self.lang = Language[language].get_default_version()
        except AttributeError:
            raise FileNotFoundError

    def __getitem__(self, item):
        return getattr(self.lang, item)

    def __contains__(self, item):
        return item in self.lang.attributes
