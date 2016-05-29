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

    :param string: The string to convert.
    :return:       The camel-cased string.
    """
    string = re.sub("^(_*)(.)",
                    lambda match: match.group(1) + match.group(2).lower(),
                    string)
    return re.sub("(?<=[^_])_+([^_])",
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

    :param string: The string to convert.
    :return:       The pascal-cased string.
    """
    string = re.sub("^(_*)(.)",
                    lambda match: match.group(1) + match.group(2).upper(),
                    string)
    return re.sub("(?<=[^_])_+([^_])",
                  lambda match: match.group(1).upper(),
                  string)


def to_snakecase(string):
    """
    Converts the given to string to snake-case.

    >>> to_snakecase('HelloWorld')
    'hello_world'
    >>> to_snakecase('__Init__File__')
    '__init_file__'
    >>> to_snakecase('')
    ''
    >>> to_snakecase('already_snake_case')
    'already_snake_case'

    :param string: The string to convert.
    :return:       The snake-cased string.
    """
    string = re.sub("^(_*)([^_])",
                    lambda match: match.group(1) + match.group(2).lower(),
                    string)
    string = re.sub("(?<=[^_])_+([^_])",
                    lambda match: "_" + match.group(1).lower(),
                    string)
    return re.sub("[A-Z]",
                  lambda match: "_" + match.group(0).lower(),
                  string)
