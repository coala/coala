from collections import OrderedDict
from itertools import chain
from inspect import isclass, getmembers
import operator
import re
from operator import itemgetter

from packaging.version import Version
from packaging.specifiers import Specifier, InvalidSpecifier

from coalib.settings.Annotations import typechain


class LanguageUberMeta(type):
    """
    This class is used to hide the `all` attribute from the Language class.
    """
    all = []


convert_int_float_str = typechain(int, float, str)


def parse_lang_str(string):
    """
    Prarses any given language `string` into name and a list of
    ``packaging.specifier.Specifier`` instances according to the given
    versions and preceding operators (ignores any whitespace).

    >>> parse_lang_str("Python")
    ('Python', [])
    >>> parse_lang_str("Python == 3.3")
    ('Python', [<Specifier('==3.3')>])
    >>> parse_lang_str("Python < 3.6, >= 3.3.1")
    ('Python', [<Specifier('<3.6')>, <Specifier('>=3.3.1')>])

    Versions without preceding operators are turned into specifiers matching
    all sub-versions:

    >>> parse_lang_str("Objective C < 3.6, 3")
    ('Objective C', [<Specifier('<3.6')>, <Specifier('~=3.0')>])

    The specifiers can also be separated from the language name with comma:

    >>> parse_lang_str("Cobol, stupid!")  # +ELLIPSIS
    Traceback (most recent call last):
     ...
    packaging.specifiers.InvalidSpecifier: Invalid specifier: 'stupid!'

    And language names can contain any amount of white space in between:

    >>> parse_lang_str("Cobol seems at least stupid ;)")  # +ELLIPSIS
    ('Cobol seems at least stupid ;)', [])
    """
    name, *specs = re.split(r'\s*,\s*', str(string).strip())
    specifiers = []
    for spec in specs:
        if spec[0].isdigit():
            spec = '~=' + spec + '.0'
        specifiers.append(Specifier(spec))
    name, *specs = name.rsplit(maxsplit=2)
    if len(specs) == 2:
        try:
            specifiers.insert(0, Specifier(''.join(specs)))
        except InvalidSpecifier:
            name += ' ' + specs.pop(0)
    if len(specs) == 1:
        spec = specs[0]
        if spec[0].isdigit():
            spec = '~=' + spec + '.0'
        try:
            specifiers.insert(0, Specifier(spec))
        except InvalidSpecifier:
            name += ' ' + spec
    return name, specifiers


def parse_spec(string):
    """
    Parse a version spec `string` into a ``packaging.specifier.Specifier``
    instance.

    >>> parse_spec('>= 3.3')
    <Specifier('>=3.3')>

    Versions without preceding operators are turned into specifiers matching
    all sub-versions:

    >>> parse_spec('3')
    <Specifier('~=3.0')>
    """
    if string[0].isdigit():
        string = '~=' + string + '.0'
    return Specifier(string)


class LanguageMeta(type, metaclass=LanguageUberMeta):
    """
    Metaclass for :class:`coalib.bearlib.languages.Language.Language`.

    Allows it being used as a decorator as well as implements the
    :meth:`.__contains__` operation and stores all languages created with the
    decorator.
    """

    def __new__(mcs, clsname, bases, clsattrs):
        for base in bases:
            if issubclass(base, Language) and base is not Language:
                for name, obj in base._attributes.items():
                    clsattrs.setdefault(name, obj)

        return type.__new__(mcs, clsname, bases, clsattrs)

    def __init__(cls, clsname, bases, clsattrs):
        cls.versions = tuple(sorted(
            Version(str(v)) for v in getattr(cls, 'versions', ())))

        super().__init__(clsname, bases, clsattrs)

    def __hash__(cls):
        """
        >>> isinstance(hash(Language), int)
        True
        """
        return type.__hash__(cls)

    def __dir__(cls):
        return super().__dir__() + [lang.__name__ for lang in type(cls).all]

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

        name, specifiers = parse_lang_str(item)

        language = getattr(cls, name)
        if not specifiers:
            return language()

        return language(*{v for spec in specifiers
                          for v in language[spec].versions})

    def __call__(cls, *args):
        if cls is Language:
            assert len(args) == 1
            arg = args[0]
            assert isclass(arg), \
                'This decorator is made for classes. Did you mean to use ' \
                '`Language[%s]`?' % (repr(arg[0]),)

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

                # Override __getitem__ of LanguageMeta to support only
                # version specifiers

                def __getitem__(cls, item):
                    specifiers = [parse_spec(spec) for spec
                                  in re.split(r'\s*,\s*', str(item).strip())]

                    versions = [v for v in cls.versions
                                if any(v in spec for spec in specifiers)]
                    if not versions:
                        raise ValueError('No versions left')
                    return cls(*versions)

            forbidden_attributes = list(
                chain(map(itemgetter(0), getmembers(Language)),
                      ('versions', 'aliases')))

            class Sub(cls, metaclass=SubLanguageMeta):
                __qualname__ = arg.__qualname__
                versions = tuple(sorted(getattr(arg, 'versions', ())))
                aliases = tuple(sorted(getattr(arg, 'aliases', ())))
                _attributes = {name: member for name, member in getmembers(arg)
                               if not name.startswith('_')
                               and name not in forbidden_attributes}

            Sub.__name__ = arg.__name__
            type(cls).all.append(Sub)
            return Sub

        return super().__call__(*args)

    def __contains__(cls, item):
        name, specifiers = parse_lang_str(item)
        return str(name).lower() in map(
            str.lower, chain(cls.aliases, [cls.__qualname__, cls.__name__])
        ) and (not specifiers or all(any(v in spec for v in cls.versions)
                                     for spec in specifiers))


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
    ...     string_delimiter = {"'": "'"}

    From a bear, you can simply parse the user given language string to get
    the instance of the Language you desire:

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

    All given versions will be stored as a sorted tuple of
    ``packaging.version.Version`` instances:

    >>> Language.TrumpScript(3.4, 3.3).versions
    (<Version('3.3')>, <Version('3.4')>)

    You can also limit versions of a Language Instance using operators
    like this:

    >>> Language['trumpscript ~= 3.0']
    America is great. 3.3, 3.4, 3.5, 3.6
    >>> Language['trumpscript < 3']
    America is great. 2.7
    >>> Language['trumpscript > 3.5']
    America is great. 3.6
    >>> Language['trumpscript >= 3.5']
    America is great. 3.5, 3.6
    >>> Language['trumpscript <= 3.4']
    America is great. 2.7, 3.3, 3.4
    >>> Language['trumpscript != 3.6']
    America is great. 2.7, 3.3, 3.4, 3.5

    The attributes are not accessible unless you have selected one - and only
    one - version of your language:

    >>> Language.TrumpScript(3.3, 3.4).comment_delimiter
    Traceback (most recent call last):
     ...
    AttributeError: You have to specify ONE version ...
    >>> Language.TrumpScript(3.3).comment_delimiter
    '#'

    If you don't know which version is the right one, just use this:

    >>> Language.TrumpScript().get_default_version()
    America is great. 3.6

    To see which attributes are available, use the ``attributes`` property:

    >>> Language.TrumpScript(3.3).attributes
    ['comment_delimiter', 'string_delimiter']

    You can access a dictionary of the attribute values for every version from
    the class:

    >>> Language.TrumpScript.comment_delimiter
    OrderedDict([(<Version('2.7')>, '#'), (<Version('3.3')>, '#'), \
(<Version('3.4')>, '#'), (<Version('3.5')>, '#'), (<Version('3.6')>, '#')])

    Any nonexistent item will of course not be served:

    >>> Language.TrumpScript.unknown_delimiter
    Traceback (most recent call last):
     ...
    AttributeError

    **You now know the most important parts for writing a bear using languages.
    Read ahead if you want to know more about working with multiple versions of
    programming languages as well as derivative languages!**

    We can define derivative languages as follows:

    >>> @Language
    ... class TrumpScriptDerivative(Language.TrumpScript):
    ...     __qualname__ = 'Shorter'
    ...     comment_delimiter = '//'
    ...     keywords = None

    >>> Language.TrumpScriptDerivative()
    Shorter 2.7, 3.3, 3.4, 3.5, 3.6

    >>> Language.TrumpScriptDerivative().get_default_version().attributes
    ['comment_delimiter', 'keywords', 'string_delimiter']
    >>> Language.TrumpScriptDerivative().get_default_version().keywords
    >>> Language.TrumpScriptDerivative().get_default_version().comment_delimiter
    '//'
    >>> Language.TrumpScriptDerivative().get_default_version().string_delimiter
    {"'": "'"}

    We can get an instance via this syntax as well:

    >>> Language[Language.TrumpScript]
    America is great. 2.7, 3.3, 3.4, 3.5, 3.6
    >>> Language[Language.TrumpScript(3.6)]
    America is great. 3.6

    As you see, you can use the `__qualname__` property. This will also affect
    the string representation and work as an implicit alias:

    >>> str(Language.TrumpScript(3.4))
    'America is great. 3.4'

    We can specify the version by instantiating the TrumpScript class now:

    >>> str(Language.TrumpScript(3.6))
    'America is great. 3.6'

    The or operator can be used to return a Language instance with combined
    versions. Respectively, the and operator can be used to return an instance
    with the common versions. Both operators work with str, int, float and
    Language instances:

    >>> Language.TrumpScript(3.6) | 'ts 3.4, 3.5'
    America is great. 3.4, 3.5, 3.6

    >>> Language.TrumpScript(3.6) | 3.5
    America is great. 3.5, 3.6

    >>> Language.TrumpScript(3.6) | 2
    America is great. 2.7, 3.6

    >>> Language.TrumpScript(3.6) | Language.TrumpScript(2.7)
    America is great. 2.7, 3.6

    >>> Language.TrumpScript(2.7, 3.3) & 'ts 3.3, 3.5'
    America is great. 3.3

    >>> Language.TrumpScript() & 3
    America is great. 3.3, 3.4, 3.5, 3.6

    >>> Language.TrumpScript(2.7, 3.3) & 3.5


    >>> Language.TrumpScript(2.7, 3.3) & Language.TrumpScript(2.7, 3.3, 3.4)
    America is great. 2.7, 3.3


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

    >>> 'ts 3.6, 3.5' in (Language.TrumpScript() & 3)
    True
    >>> 'ts 3.6, 3.5' in ((Language.TrumpScript() & 2)
    ...                  | Language.TrumpScript(3.5))
    False
    >>> Language.TrumpScript(2.7, 3.5) in (Language.TrumpScript() & 3)
    False
    >>> Language.TrumpScript(3.5) in (Language.TrumpScript() & 3)
    True

    Comparison between Language instances can be achieved only for instances of
    the same class:

    >>> Language['TrumpScript'] == Language['Python']
    Traceback (most recent call last):
    ...
    TypeError: Language object is not compatible with type of given comparable,\
 <class 'coalib.bearlib.languages.Language.America is great.'>\
 != <class 'coalib.bearlib.languages.Language.Python'>

    Equality can be achieved for Languages with multiple versions:

    >>> Language.TrumpScript(2.7, 3.3) == Language.TrumpScript(2.7, 3.3, 3.4)
    False

    For using gt, lt, ge or le operators you should specify one version:

    >>> Language.TrumpScript(2.7) < Language.TrumpScript(3.4)
    True
    >>> Language.TrumpScript(2.7) > Language.TrumpScript(3.3, 3.4)
    False
    >>> Language.TrumpScript(3.4) <= Language.TrumpScript(3.4)
    True
    >>> Language.TrumpScript(3.6) >= Language.TrumpScript(3.4, 3.5)
    True
    >>> Language.TrumpScript(2.7, 3.3) < Language.TrumpScript(2.7, 3.3, 3.4)
    Traceback (most recent call last):
     ...
    TypeError: You have to specify ONE version

    Any undefined language will obviously not be available:

    >>> Language.Cobol
    Traceback (most recent call last):
     ...
    AttributeError
    """

    def __init__(self, *versions):
        versions = [Version(str(v)) for v in versions]
        assert all(version in type(self).versions for version in versions)
        if not versions:
            self.versions = type(self).versions
        else:
            self.versions = tuple(sorted(versions))

    def __getattr__(self, item):
        if len(self.versions) > 1:
            raise AttributeError('You have to specify ONE version of your '
                                 'language to retrieve attributes for it.')
        try:
            return self._attributes[item]
        except KeyError:
            if len(self.attributes) == 0:
                message = 'There are no available attributes for this language.'
            else:
                message = ('This is not a valid attribute! '
                           '\nThe following attributes are available:')
                message += '\n'.join(self.attributes)
            raise AttributeError(message)

    def __str__(self):
        result = type(self).__qualname__
        if self.versions:
            result += ' ' + ', '.join(map(str, self.versions))
        return result

    def __repr__(self):
        return str(self)

    def __gt__(self, other):
        return compare(self, other, operator.gt)

    def __lt__(self, other):
        return compare(self, other, operator.lt)

    def __ge__(self, other):
        return compare(self, other, operator.ge)

    def __le__(self, other):
        return compare(self, other, operator.le)

    def __eq__(self, other):
        return compare(self, other, operator.eq)

    def __ne__(self, other):
        return compare(self, other, operator.ne)

    def __or__(self, other):
        language = prepare_instance(self, other)
        assert_type_equals(self, language)
        return type(self)(*chain(self.versions, language.versions))

    def __and__(self, other):
        language = prepare_instance(self, other)
        assert_type_equals(self, language)
        common_versions = set(self.versions).intersection(language.versions)
        if common_versions:
            return type(self)(*tuple(common_versions))
        else:
            return None

    def __contains__(self, item):
        item = Language[item]
        return (type(self) is type(item)
                and set(item.versions).issubset(set(self.versions)))

    @property
    def attributes(self):
        """
        Retrieves the names of all attributes that are available for this
        language.
        """
        return sorted(self._attributes.keys())

    def get_default_version(self):
        """
        Retrieves the latest version the user would want to choose from the
        given versions in self.

        (At a later point this might also retrieve a default version
        specifiable by the language definition, so keep using this!)
        """
        return type(self)(self.versions[-1]) if self.versions else type(self)()


def prepare_instance(language_, item):
    """
    It creates a new `Language` instance depending on the type of item. It is
    used in __and__ , __or__ methods to avoid duplicate code.

    :param item:
        Item to use to create the new instance.
    :return:
        A `Language` instance.
    """
    if isinstance(item, float):
        language = type(language_)((item))
    elif isinstance(item, int):
        language = Language[type(language_).__name__ + ' ' + str(item)]
    elif isinstance(item, str):
        language = Language[item]
    else:
        language = item
    return language


def assert_type_equals(language, comparable):
    """
    Checks if the given instances are of the same Language class and raises an
    error otherwise.

    :param language:
        A `Language` instance.
    :param comparable:
        Another `Language` instance.
    :return:
        True
    :raises TypeError:
        If Language instances are not of the same class
    """
    if type(language) is not type(comparable):
        raise TypeError('Language object is not compatible with type of given '
                        'comparable, {} != {}'
                        .format(type(language), type(comparable)))


def compare_versions(language, versions, operator_):
    """
    Compares the version of a Language instance to the given set of versions
    using gt, lt, ge or le operator. Comparison can be achieved if only the
    given instance has a specified version. Otherwise, comparison of sets of
    versions doesn't make sense and raises an error.

    :param language:
        A `Language` instance
    :param versions:
        A tuple of versions to be compared to instance's version.
    :param operator_:
        The operator to use for the comparison.
    :return:
        True/False
    :raises TypeError:
        If Language instance has zero or more than one version
    """
    if len(language.versions) != 1:
        raise TypeError('You have to specify ONE version')
    elif operator_ in [operator.ge, operator.le]:
        return language.versions[0] in versions or all(
            operator_(Version(str(language.versions[0])),
                      Version(str(version))) for version in versions)
    else:
        return all(operator_(Version(str(language.versions[0])),
                             Version(str(version))) for version in versions)


def compare(language, comparable, operator_):
    """
    Compares a Language instance to another depending on the given operator:

    >>> Language['C'] == Language["C"]
    True
    >>> Language['py 2'] != Language['py 3']
    True
    >>> Language['Python 2.7'] < Language['Python 3.4']
    True
    >>> Language['Python 2.7'] > Language['py 3']
    False
    >>> Language['Python'] < Language['py 3']
    Traceback (most recent call last):
    ...
    TypeError: You have to specify ONE version

    :param language:
        A `Language` instance.
    :param comparable:
        An instance to be compared to `language`.
    :param operator_:
        The operator to use for the comparison.
    :return:
        True/False
    :raises TypeError:
        If Language instances are not of the same type.
    """
    assert_type_equals(language, comparable)
    if operator_ in [operator.eq, operator.ne]:
        if len(language.versions) != len(comparable.versions):
            return operator_(len(language.versions), len(comparable.versions))
        return all(list(operator_(Version(str(version[0])),
                                  Version(str(version[1]))) for version
                        in zip(language.versions, comparable.versions)
                        if not(version[0] is None or version[1] is None)))
    else:
        return compare_versions(language, comparable.versions, operator_)


class Languages(tuple):
    """
    A ``tuple``-based container for :class:`coalib.bearlib.languages.Language`
    instances. It supports language identifiers in any format accepted by
    ``Language[...]``:

    >>> Languages(['C#', Language["py 3"]])
    (C#, Python 3.3, 3.4, 3.5, 3.6)
    >>> Languages(['C#', Language.Python['3.6']])
    (C#, Python 3.6)
    >>> Languages(['C#', 'Python 2.7'])
    (C#, Python 2.7)

    It provides :meth:`.__contains__` for checking if a given language
    identifier is included:

    >>> 'Python 2.7, 3.5' in Languages([Language.Python()])
    True
    >>> 'Py 3.3' in Languages(['Python 2'])
    False
    >>> 'csharp' in Languages(['C#', Language.Python(3.6)])
    True
    """

    def __new__(cls, items):
        return tuple.__new__(cls, (Language[i] for i in items))

    def __contains__(self, item):
        return any(item in lang for lang in self)
