import os
from collections import Iterable, OrderedDict

from coala_utils.decorators import (
    enforce_signature,
    generate_repr,
)
from coala_utils.string_processing.StringConverter import StringConverter
from coalib.parsing.Globbing import glob_escape


def path(obj, *args, **kwargs):
    return obj.__path__(*args, **kwargs)


def path_list(obj, *args, **kwargs):
    return obj.__path_list__(*args, **kwargs)


def url(obj, *args, **kwargs):
    return obj.__url__(*args, **kwargs)


def glob(obj, *args, **kwargs):
    """
    Creates a path in which all special glob characters in all the
    parent directories in the given setting are properly escaped.

    :param obj: The ``Setting`` object from which the key is obtained.
    :return:    Returns a path in which special glob characters are escaped.
    """
    return obj.__glob__(*args, **kwargs)


def glob_list(obj, *args, **kwargs):
    """
    Creates a list of paths in which all special glob characters in all the
    parent directories of all paths in the given setting are properly escaped.

    :param obj: The ``Setting`` object from which the key is obtained.
    :return:    Returns a list of paths in which special glob characters are
                escaped.
    """
    return obj.__glob_list__(*args, **kwargs)


def typed_list(conversion_func):
    """
    Creates a class that converts a setting into a list of elements each
    converted with the given conversion function.

    :param conversion_func: The conversion function that converts a string into
                            your desired list item object.
    :return:                An instance of the created conversion class.
    """

    class Converter:

        def __call__(self, setting):
            return [conversion_func(StringConverter(elem))
                    for elem in setting]

        def __repr__(self):
            return 'typed_list(%s)' % conversion_func.__name__

    return Converter()


def typed_dict(key_type, value_type, default):
    """
    Creates a class that converts a setting into a dict with the given types.

    :param key_type:   The type conversion function for the keys.
    :param value_type: The type conversion function for the values.
    :param default:    The default value to use if no one is given by the user.
    :return:           An instance of the created conversion class.
    """

    class Converter:

        def __call__(self, setting):
            return {key_type(StringConverter(key)):
                    value_type(StringConverter(value))
                    if value != '' else default
                    for key, value in dict(setting).items()}

        def __repr__(self):
            return 'typed_dict(%s, %s, default=%s)' % (
                key_type.__name__, value_type.__name__, default)

    return Converter()


def typed_ordered_dict(key_type, value_type, default):
    """
    Creates a class that converts a setting into an ordered dict with the
    given types.

    :param key_type:   The type conversion function for the keys.
    :param value_type: The type conversion function for the values.
    :param default:    The default value to use if no one is given by the user.
    :return:           An instance of the created conversion class.
    """

    class Converter:

        def __call__(self, setting):
            return OrderedDict((key_type(StringConverter(key)),
                                value_type(StringConverter(value))
                                if value != '' else default)
                               for key, value in OrderedDict(setting).items())

        def __repr__(self):
            return 'typed_ordered_dict(%s, %s, default=%s)' % (
                key_type.__name__, value_type.__name__, default)

    return Converter()


@generate_repr('key', 'value', 'origin', 'from_cli', 'to_append')
class Setting(StringConverter):
    """
    A Setting consists mainly of a key and a value. It mainly offers many
    conversions into common data types.
    """

    @enforce_signature
    def __init__(self,
                 key,
                 value,
                 origin: str='',
                 strip_whitespaces: bool=True,
                 list_delimiters: Iterable=(',', ';'),
                 from_cli: bool=False,
                 remove_empty_iter_elements: bool=True,
                 to_append: bool=False):
        """
        Initializes a new Setting,

        :param key:                        The key of the Setting.
        :param value:                      The value, if you apply conversions
                                           to this object these will be applied
                                           to this value.
        :param origin:                     The originating file. This will be
                                           used for path conversions and the
                                           last part will be stripped of. If
                                           you want to specify a directory as
                                           origin be sure to end it with a
                                           directory separator.
        :param strip_whitespaces:          Whether to strip whitespaces from
                                           the value or not
        :param list_delimiters:            Delimiters for list conversion
        :param from_cli:                   True if this setting was read by the
                                           CliParser.
        :param remove_empty_iter_elements: Whether to remove empty elements in
                                           iterable values.
        :param to_append:                  The boolean value if setting value
                                           needs to be appended to a setting in
                                           the defaults of a section.
        """
        self.to_append = to_append

        StringConverter.__init__(
            self,
            value,
            strip_whitespaces=strip_whitespaces,
            list_delimiters=list_delimiters,
            remove_empty_iter_elements=remove_empty_iter_elements)

        self.from_cli = from_cli
        self.key = key
        self.origin = str(origin)

    def __path__(self, origin=None, glob_escape_origin=False):
        """
        Determines the path of this setting.

        Note: You can also use this function on strings, in that case the
        origin argument will be taken in every case.

        :param origin:             The origin file to take if no origin is
                                   specified for the given setting. If you
                                   want to provide a directory, make sure it
                                   ends with a directory separator.
        :param glob_escape_origin: When this is set to true, the origin of
                                   this setting will be escaped with
                                   ``glob_escape``.
        :return:                   An absolute path.
        :raises ValueError:        If no origin is specified in the setting
                                   nor the given origin parameter.
        """
        strrep = str(self).strip()
        if os.path.isabs(strrep):
            return strrep

        if hasattr(self, 'origin') and self.origin != '':
            origin = self.origin

        if origin is None:
            raise ValueError('Cannot determine path without origin.')

        # We need to get full path before escaping since the full path
        # may introduce unintended glob characters
        origin = os.path.abspath(os.path.dirname(origin))

        if glob_escape_origin:
            origin = glob_escape(origin)

        return os.path.normpath(os.path.join(origin, strrep))

    def __glob__(self, origin=None):
        """
        Determines the path of this setting with proper escaping of its
        parent directories.

        :param origin:      The origin file to take if no origin is specified
                            for the given setting. If you want to provide a
                            directory, make sure it ends with a directory
                            separator.
        :return:            An absolute path in which the parent directories
                            are escaped.
        :raises ValueError: If no origin is specified in the setting nor the
                            given origin parameter.
        """
        return Setting.__path__(self, origin, glob_escape_origin=True)

    def __path_list__(self):
        """
        Splits the value into a list and creates a path out of each item taking
        the origin of the setting into account.

        :return: A list of absolute paths.
        """
        return [Setting.__path__(elem, self.origin) for elem in self]

    def __glob_list__(self):
        """
        Splits the value into a list and creates a path out of each item in
        which the special glob characters in origin are escaped.

        :return: A list of absolute paths in which the special characters in
                 the parent directories of the setting are escaped.
        """
        return [Setting.__glob__(elem, self.origin) for elem in self]

    def __iter__(self, remove_backslashes=True):
        if self.to_append:
            raise ValueError('Iteration on this object is invalid because the '
                             'value is incomplete. Please access the value of '
                             'the setting in a section to iterate through it.')
        return StringConverter.__iter__(self, remove_backslashes)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        newkey = str(key)
        if newkey == '':
            raise ValueError('An empty key is not allowed for a setting.')

        self._key = newkey

    @StringConverter.value.getter
    def value(self):
        if self.to_append:
            raise ValueError('This property is invalid because the value is '
                             'incomplete. Please access the value of the '
                             'setting in a section to get the complete value.')
        return self._value
