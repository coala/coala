import logging

from coala_utils.string_processing import escape

from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coalib.bearlib.languages import Language
from coalib.settings.Setting import Setting


class LanguageDefinition(SectionCreatable):
    """
    **This class is deprecated!** Use the `Language` class instead.

    A Language Definition holds constants which may help parsing the language.
    If you want to write a bear you'll probably want to use those definitions
    to keep your bear independent of the semantics of each language.

    You can easily get your language definition by just creating it with
    the name of the language desired:

    >>> list(LanguageDefinition("cpp")['extensions'])
    ['.c', '.cpp', '.h', '.hpp']

    For some languages aliases exist, the name is case insensitive; they will
    behave just like before and return settings:

    >>> dict(LanguageDefinition('C++')['comment_delimiter'])
    {'//': ''}
    >>> dict(LanguageDefinition('C++')['string_delimiters'])
    {'"': '"'}

    If no language exists, you will get a ``FileNotFoundError``:

    >>> LanguageDefinition("BULLSHIT!")
    Traceback (most recent call last):
     ...
    FileNotFoundError

    Custom coalangs are no longer supported. You can simply register your
    languages to the Languages decorator. When giving a custom coalang
    directory a warning will be emitted and it will attempt to load the given
    Language anyway through conventional means:

    >>> LanguageDefinition("custom", coalang_dir='somewhere')
    Traceback (most recent call last):
     ...
    FileNotFoundError

    If you need a custom language, just go like this:

    >>> @Language
    ... class MyLittlePony:
    ...     color = 'green'
    ...     legs = 5
    >>> int(LanguageDefinition('mylittlepony')['legs'])
    5

    But seriously, just use `Language` - and mind that it's already typed:

    >>> Language['mylittlepony'].get_default_version().legs
    5
    """

    def __init__(self, language: str, coalang_dir=None):
        """
        Creates a new LanguageDefinition object from file.

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
        value = getattr(self.lang, item)
        if isinstance(value, (list, tuple)):
            value = Setting(item, ', '.join(escape(val, ',') for val in value))
        elif isinstance(value, dict):
            value = Setting(item, ', '.join(
                escape(key, ':,') + ': ' + escape(val, ':,')
                for key, val in value.items()))
        else:
            value = Setting(item, str(value))
        return value

    def __contains__(self, item):
        return item in self.lang.attributes
