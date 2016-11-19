import re


def to_camelcase(string):
    """
    Converts the given string to camel-case.

    >>> to_camelcase('Hello_world')
    'helloWorld'
    >>> to_camelcase('__Init__file__')
    '__initFile__'
    >>> to_camelcase('')
    ''
    >>> to_camelcase('alreadyCamelCase')
    'alreadyCamelCase'
    >>> to_camelcase('   string')
    '___string'

    :param string: The string to convert.
    :return:       The camel-cased string.
    """
    string = re.sub('(\s)',
                    lambda match: '_',
                    string)
    string = re.sub('^(_*)(.)',
                    lambda match: match.group(1) + match.group(2).lower(),
                    string)
    return re.sub('(?<=[^_])_+([^_])',
                  lambda match: match.group(1).upper(),
                  string)


def to_pascalcase(string):
    """
    Converts the given to string pascal-case.

    >>> to_pascalcase('hello_world')
    'HelloWorld'
    >>> to_pascalcase('__init__file__')
    '__InitFile__'
    >>> to_pascalcase('')
    ''
    >>> to_pascalcase('AlreadyPascalCase')
    'AlreadyPascalCase'
    >>> to_pascalcase('   string')
    '___String'

    :param string: The string to convert.
    :return:       The pascal-cased string.
    """
    string = re.sub('(\s)',
                    lambda match: '_',
                    string)
    string = re.sub('^(_*)(.)',
                    lambda match: match.group(1) + match.group(2).upper(),
                    string)
    return re.sub('(?<=[^_])_+([^_])',
                  lambda match: match.group(1).upper(),
                  string)


def to_snakecase(string):
    """
    Converts the given string to snake-case.

    >>> to_snakecase('HelloWorld')
    'hello_world'
    >>> to_snakecase('__Init__File__')
    '__init_file__'
    >>> to_snakecase('')
    ''
    >>> to_snakecase('already_snake_case')
    'already_snake_case'
    >>> to_snakecase('   string  ')
    '___string__'
    >>> to_snakecase('ABCde.F.G..H..IH')
    'a_b_cde.f.g..h..i_h'

    :param string: The string to convert.
    :return:       The snake-cased string.
    """
    string = re.sub('(\s)',
                    lambda match: '_',
                    string)
    string = re.sub('^(_*)([^_])',
                    lambda match: match.group(1) + match.group(2).lower(),
                    string)
    string = re.sub('(\w*)([.]+)([A-Z])',
                    lambda match: (match.group(1) + match.group(2) +
                                   match.group(3).lower()),
                    string)
    string = re.sub('(?<=[^_])_+([^_])',
                    lambda match: '_' + match.group(1).lower(),
                    string)
    return re.sub('[A-Z]',
                  lambda match: '_' + match.group(0).lower(),
                  string)


def to_spacecase(string):
    """
    Converts the given string to space-case.

    >>> to_spacecase('helloWorld')
    'Hello World'
    >>> to_spacecase('__Init__File__')
    'Init File'
    >>> to_spacecase('')
    ''
    >>> to_spacecase('Already Space Case')
    'Already Space Case'
    >>> to_spacecase('  string  ')
    'String'

    :param string: The string to convert.
    :return:       The space-cased string.
    """
    string = re.sub('(_)',
                    ' ',
                    string)
    string = re.sub('^(\s*)(.)',
                    lambda match: match.group(2).upper(),
                    string)
    string = re.sub('(\s*)$',
                    '',
                    string)
    string = re.sub('(?<=[^\s])\s+([^\s])',
                    lambda match: ' ' + match.group(1).upper(),
                    string)
    return re.sub('(?<=[^\s])([A-Z])',
                  lambda match: ' ' + match.group(1),
                  string)
