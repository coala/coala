from itertools import chain
from inspect import isclass
import operator
import re

from coalib.misc.Annotations import typechain


class LanguageUberMeta(type):
    """
    This class is used to hide the `all` attribute from the Language class.
    """
    all = []


convert_int_float = typechain(int, float)


def parse_lang_str(string):
    """
    Prarses any given language string into name and a list of float versions:

    >>> parse_lang_str("Python")
    ('Python', [])
    >>> parse_lang_str("Python 3.3")
    ('Python', [3.3])
    >>> parse_lang_str("Python 3.6, 3.3")
    ('Python', [3.6, 3.3])
    >>> parse_lang_str("Objective C 3.6, 3.3")
    ('Objective C', [3.6, 3.3])
    >>> parse_lang_str("Cobol, stupid!")  # +ELLIPSIS
    Traceback (most recent call last):
     ...
    ValueError: Couldn't convert value 'stupid!' ...
    """
    name, *str_versions = re.split(r',\s*', str(string))
    versions = list(map(convert_int_float, str_versions))
    try:
        name, version = name.rsplit(maxsplit=1)
        version = convert_int_float(version)
    except (ValueError, TypeError):
        pass
    else:
        versions.insert(0, version)

    return name, versions


class LanguageMeta(type, metaclass=LanguageUberMeta):
    """
    Metaclass for :class:`coalib.bearlib.languages.Language.Language`.

    Allows it being used as a decorator as well as implements the
    `__contains__` operation and stores all languages created with the
    decorator.

    The operators are defined on the class as well, so you can do the
    following:

    >>> @Language
    ... class SomeLang:
    ...     versions = 2.7, 3.3, 3.4, 3.5, 3.6
    >>> Language.SomeLang > 3.4
    SomeLang 3.5, 3.6
    >>> Language.SomeLang < 3.4
    SomeLang 2.7, 3.3
    >>> Language.SomeLang >= 3.4
    SomeLang 3.4, 3.5, 3.6
    >>> Language.SomeLang <= 3.4
    SomeLang 2.7, 3.3, 3.4
    >>> Language.SomeLang == 3.4
    SomeLang 3.4
    >>> Language.SomeLang != 3.4
    SomeLang 2.7, 3.3, 3.5, 3.6
    >>> Language.SomeLang == 1.0
    Traceback (most recent call last):
     ...
    ValueError: No versions left
    """
    def __getattr__(cls, item):
        try:
            return next(lang for lang in type(cls).all if item in lang)
        except StopIteration:
            raise AttributeError

    def __getitem__(cls, item):
        if isinstance(item, cls):
            return item
        if isclass(item) and issubclass(item, cls):
            return item()

        name, versions = parse_lang_str(item)

        language = getattr(cls, name)
        result = None
        for version in versions:
            if result:
                result |= language == version
            else:
                result = language == version

        return result

    def __call__(cls, *args):
        if cls is Language:
            assert len(args) == 1
            arg = args[0]

            class Sub(Language, arg):
                __qualname__ = arg.__qualname__
                versions = tuple(sorted(getattr(arg, 'versions', ())))
                aliases = tuple(sorted(getattr(arg, 'aliases', ())))

            Sub.__name__ = arg.__name__
            type(cls).all.append(Sub)
            return Sub

        return super().__call__(*args)

    def __contains__(cls, item):
        name, versions = parse_lang_str(item)

        return str(name).lower() in map(
            str.lower, chain(cls.aliases, [cls.__qualname__, cls.__name__])
        ) and (not versions or all(version in cls.versions
                                   for version in versions))

    def __gt__(cls, other):
        return cls() > other

    def __lt__(cls, other):
        return cls() < other

    def __ge__(cls, other):
        return cls() >= other

    def __le__(cls, other):
        return cls() <= other

    def __eq__(cls, other):
        return cls() == other

    def __ne__(cls, other):
        return cls() != other


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

    We can also parse any user given string to get the instance:

    >>> Language['PY 3.4, 3.6']
    Python 3.4, 3.6
    >>> Language['PY 3']
    Python 3.3, 3.4, 3.5, 3.6
    >>> Language['PY 1']
    Traceback (most recent call last):
     ...
    ValueError: No versions left

    Similarly we can get an instance via this syntax:

    >>> Language[Language.Python]
    Python 2.7, 3.3, 3.4, 3.5, 3.6
    >>> Language[Language.Python(3.6)]
    Python 3.6

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

    You can also define ranges of versions of languages:

    >>> (Language.Python > 3.3) <= 3.5
    Python 3.4, 3.5

    >>> Language.Python == 3
    Python 3.3, 3.4, 3.5, 3.6

    Those can be combined by the or operator:

    >>> (Language.Python == 3.6) | (Language.Python == 2)
    Python 2.7, 3.6

    The `__contains__` operator of the class is defined as well for strings
    and instances. This is case insensitive and aliases are allowed:

    >>> Language.Python(3.6) in Language.Python
    True
    >>> 'pY 3.6, 3.5' in Language.Python
    True
    >>> 'Python 2.6' in Language.Python
    False
    >>> 'Python' in Language.Python
    True

    This also works on instances:

    >>> 'pY 3.6, 3.5' in (Language.Python == 3)
    True
    >>> 'pY 3.6, 3.5' in ((Language.Python == 2) | (Language.Python == 3.5))
    False
    >>> Language.Python(2.7, 3.5) in (Language.Python == 3)
    False
    >>> Language.Python(3.5) in (Language.Python == 3)
    True

    Any undefined language will obviously not be available:

    >>> Language.Cobol
    Traceback (most recent call last):
     ...
    AttributeError
    """

    def __init__(self, *versions):
        assert all(version in type(self).versions for version in versions)
        if not versions:
            self.versions = type(self).versions
        else:
            self.versions = tuple(sorted(versions))

    def __str__(self):
        return '{} {}'.format(type(self).__qualname__,
                              ', '.join(map(str, self.versions)))

    def __repr__(self):
        return str(self)

    def __gt__(self, other):
        return limit_versions(self, other, operator.gt)

    def __lt__(self, other):
        return limit_versions(self, other, operator.lt)

    def __ge__(self, other):
        return limit_versions(self, other, operator.ge)

    def __le__(self, other):
        return limit_versions(self, other, operator.le)

    def __eq__(self, other):
        return limit_versions(self, other, operator.eq)

    def __ne__(self, other):
        return limit_versions(self, other, operator.ne)

    def __or__(self, other):
        return type(self)(*chain(self.versions, other.versions))

    def __ior__(self, other):
        self.versions = self.versions + other.versions
        return self

    def __contains__(self, item):
        item = Language[item]
        return (type(self) == type(item)
                and set(item.versions).issubset(set(self.versions)))


def limit_versions(language, limit, operator):
    """
    Limits given languages with the given operator:

    :param language:
        A `Language` instance.
    :param limit:
        A number to limit the versions.
    :param operator:
        The operator to use for the limiting.
    :return:
        A new `Language` instance with limited versions.
    :raises ValueError:
        If no version is left anymore.
    """
    if isinstance(limit, int):
        versions = [version for version in language.versions
                    if operator(int(version), limit)]
    else:

        versions = [version for version in language.versions
                    if operator(version, limit)]
    if not versions:
        raise ValueError('No versions left')
    return type(language)(*versions)
