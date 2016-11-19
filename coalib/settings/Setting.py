import os
from collections import OrderedDict

from coala_utils.decorators import generate_repr
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
    Creates a function that converts a setting into a list of elements each
    converted with the given conversion function.

    :param conversion_func: The conversion function that converts a string into
                            your desired list item object.
    :return:                A conversion function.
    """
    return lambda setting: [
        conversion_func(StringConverter(elem)) for elem in setting]


def typed_dict(key_type, value_type, default):
    """
    Creates a function that converts a setting into a dict with the given
    types.

    :param key_type:   The type conversion function for the keys.
    :param value_type: The type conversion function for the values.
    :param default:    The default value to use if no one is given by the user.
    :return:           A conversion function.
    """
    return lambda setting: {
        key_type(StringConverter(key)):
        value_type(StringConverter(value)) if value != '' else default
        for key, value in dict(setting).items()}


def typed_ordered_dict(key_type, value_type, default):
    """
    Creates a function that converts a setting into an ordered dict with the
    given types.

    :param key_type:   The type conversion function for the keys.
    :param value_type: The type conversion function for the values.
    :param default:    The default value to use if no one is given by the user.
    :return:           A conversion function.
    """
    return lambda setting: OrderedDict(
        (key_type(StringConverter(key)),
         value_type(StringConverter(value)) if value != '' else default)
        for key, value in OrderedDict(setting).items())


@generate_repr('key', 'value', 'origin', 'from_cli')
class Setting(StringConverter):
    """
    A Setting consists mainly of a key and a value. It mainly offers many
    conversions into common data types.
    """

    def __init__(self,
                 key,
                 value,
                 origin='',
                 strip_whitespaces=True,
                 list_delimiters=(',', ';'),
                 from_cli=False,
                 remove_empty_iter_elements=True):
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
        """
        if not isinstance(from_cli, bool):
            raise TypeError('from_cli needs to be a boolean value.')

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

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        newkey = str(key)
        if newkey == '':
            raise ValueError('An empty key is not allowed for a setting.')

        self._key = newkey
