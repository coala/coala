from itertools import chain


class LanguageUberMeta(type):
    """
    This class is used to hide the `all` attribute from the Language class.
    """
    all = []


class LanguageMeta(type, metaclass=LanguageUberMeta):
    """
    Metaclass for :class:`coalib.bearlib.languages.Language.Language`.

    Allows it being used as a decorator as well as implements the
    `__contains__` operation and stores all languages created with the
    decorator.
    """
    def __getattr__(cls, item):
        try:
            return next(lang for lang in type(cls).all if item in lang)
        except StopIteration:
            raise AttributeError

    def __call__(cls, arg):
        if cls is Language:
            class Sub(Language, arg):
                __qualname__ = arg.__qualname__

            Sub.__name__ = arg.__name__
            type(cls).all.append(Sub)
            return Sub

        return super().__call__(arg)

    def __contains__(cls, item):
        try:
            name, version = str(item).rsplit(maxsplit=1)
            version = float(version)
        except (ValueError, TypeError):
            version = None
            name = item

        return str(name).lower() in map(
            str.lower, chain(cls.aliases, [cls.__qualname__, cls.__name__])
        ) and (not version or version in cls.versions)


class Language(metaclass=LanguageMeta):
    """
    This class defines programming languages and their versions.

    You can define a new programming language as follows:

    >>> @Language
    ... class Python:
    ...     aliases = 'py',
    ...     versions = 2.7, 3.3, 3.4, 3.5, 3.6

    Now we can access the language globally:

    >>> Language.Python
    <class 'coalib.bearlib.languages.Language.Python'>

    We can specify the version by instantiating the Python class now:

    >>> str(Language.Python(3.6))
    'Python 3.6'

    You can simply define a qualname for your language, if it contains special
    characters:

    >>> @Language
    ... class CPP:
    ...     __qualname__ = 'C++'
    ...     aliases = 'CXX',
    ...     versions = 11, 14, 17

    The qualname will be used for the string representation:

    >>> str(CPP(11))
    'C++ 11'

    The `__contains__` operator of the class is defined as well for strings
    and instances. This is case insensitive and aliases are allowed:

    >>> Language.Python(3.6) in Language.Python
    True
    >>> 'pY 3.6' in Language.Python
    True
    >>> 'Python 2.6' in Language.Python
    False
    >>> 'Python' in Language.Python
    True

    Any undefined language will obviously not be available:

    >>> Language.Cobol
    Traceback (most recent call last):
     ...
    AttributeError
    """

    def __init__(self, version):
        assert version in type(self).versions
        self.version = version

    def __str__(self):
        return '{} {}'.format(type(self).__qualname__, self.version)
