from collections import OrderedDict
from itertools import chain
from inspect import isclass, getmembers
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
        if not versions:
            return language()

        return language(*set(chain(*((language == v).versions
                                     for v in versions))))

    def __call__(cls, *args):
        if cls is Language:
            assert len(args) == 1
            arg = args[0]

            class SubLanguageMeta(type(cls)):
                # Override __getattr__ of the LanguageMeta to get a dict with
                # the attributes

                def __getattr__(self, item):
                    try:
                        return OrderedDict(
                            (version, self._attributes[item])
                            for version in self.versions)
                    except KeyError:
                        raise AttributeError

            class Sub(cls, metaclass=SubLanguageMeta):
                __qualname__ = arg.__qualname__
                versions = tuple(sorted(getattr(arg, 'versions', ())))
                aliases = tuple(sorted(getattr(arg, 'aliases', ())))
                _attributes = {name: member for name, member in getmembers(arg)
                               if not name.startswith('_')
                               and not name in ('versions', 'aliases')}

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
    ... class TrumpScript:
    ...     __qualname__ = "America is great."
    ...     aliases = 'ts',
    ...     versions = 2.7, 3.3, 3.4, 3.5, 3.6
    ...     comment_delimiter = '#'

    Now we can access the language globally:

    >>> Language.TrumpScript
    <class 'coalib.bearlib.languages.Language.America is great.'>

    As you see, you can use the `__qualname__` property. This will also affect
    the string representation and work as an implicit alias:

    >>> str(Language.TrumpScript(3.4))
    'America is great. 3.4'

    You can access a dictionary of the attribute values for every version from
    the class:

    >>> Language.TrumpScript.comment_delimiter
    OrderedDict([(2.7, '#'), (3.3, '#'), (3.4, '#'), (3.5, '#'), (3.6, '#')])

    Any nonexistent item will of course not be served:

    >>> Language.TrumpScript.unknown_delimiter
    Traceback (most recent call last):
     ...
    AttributeError

    The attributes are not accessible unless you have selected one - and only
    one - version of your language:

    >>> Language.TrumpScript(3.3, 3.4).comment_delimiter  # +ELLIPSIS
    Traceback (most recent call last):
     ...
    AttributeError: You have to specify ONE version ...
    >>> Language.TrumpScript(3.3).comment_delimiter
    '#'

    We can specify the version by instantiating the TrumpScript class now:

    >>> str(Language.TrumpScript(3.6))
    'America is great. 3.6'

    We can also parse any user given string to get the instance:

    >>> Language['trumpscript']
    America is great. 2.7, 3.3, 3.4, 3.5, 3.6
    >>> Language['ts 3.4, 3.6']
    America is great. 3.4, 3.6
    >>> Language['TS 3']
    America is great. 3.3, 3.4, 3.5, 3.6
    >>> Language['tS 1']
    Traceback (most recent call last):
     ...
    ValueError: No versions left

    Similarly we can get an instance via this syntax:

    >>> Language[Language.TrumpScript]
    America is great. 2.7, 3.3, 3.4, 3.5, 3.6
    >>> Language[Language.TrumpScript(3.6)]
    America is great. 3.6

    You can also define ranges of versions of languages:

    >>> (Language.TrumpScript > 3.3) <= 3.5
    America is great. 3.4, 3.5

    >>> Language.TrumpScript == 3
    America is great. 3.3, 3.4, 3.5, 3.6

    Those can be combined by the or operator:

    >>> (Language.TrumpScript == 3.6) | (Language.TrumpScript == 2)
    America is great. 2.7, 3.6

    The `__contains__` operator of the class is defined as well for strings
    and instances. This is case insensitive and aliases are allowed:

    >>> Language.TrumpScript(3.6) in Language.TrumpScript
    True
    >>> 'ts 3.6, 3.5' in Language.TrumpScript
    True
    >>> 'TrumpScript 2.6' in Language.TrumpScript
    False
    >>> 'TrumpScript' in Language.TrumpScript
    True

    This also works on instances:

    >>> 'ts 3.6, 3.5' in (Language.TrumpScript == 3)
    True
    >>> 'ts 3.6,3.5' in ((Language.TrumpScript == 2)
    ...                  | Language.TrumpScript(3.5))
    False
    >>> Language.TrumpScript(2.7, 3.5) in (Language.TrumpScript == 3)
    False
    >>> Language.TrumpScript(3.5) in (Language.TrumpScript == 3)
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

    def __getattr__(self, item):
        if len(self.versions) > 1:
            raise AttributeError('You have to specify ONE version of your '
                                 'language to retrieve attributes for it.')
        return self._attributes[item]

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

    def __contains__(self, item):
        item = Language[item]
        return (type(self) is type(item)
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


class Languages(tuple):
    """
    A ``tuple``-based container for :class:`coalib.bearlib.languages.Language`
    instances. It supports language identifiers in any format accepted by
    ``Language[...]``:

    >>> Languages(['C#', Language.Python == 3])
    (C# , Python 3.3, 3.4, 3.5, 3.6)

    It provides :meth:`.__contains__` for checking if a given language
    identifier is included:

    >>> 'Python 2.7, 3.5' in Languages([Language.Python()])
    True
    >>> 'Py 3.3' in Languages(['Python 2'])
    False
    >>> 'csharp' in Languages(['C#', Language.Python == 3])
    True
    """

    def __new__(cls, items):
        return tuple.__new__(cls, (Language[i] for i in items))

    def __contains__(self, item):
        return any(item in lang for lang in self)
