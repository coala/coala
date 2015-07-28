from collections import OrderedDict
import os

from coalib.misc.Decorators import generate_repr
from coalib.misc.StringConverter import StringConverter


def path(obj, *args, **kwargs):
    return obj.__path__(*args, **kwargs)


def path_list(obj, *args, **kwargs):
    return obj.__path_list__(*args, **kwargs)


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
        value_type(StringConverter(value)) if value != "" else default
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
         value_type(StringConverter(value)) if value != "" else default)
        for key, value in OrderedDict(setting).items())


@generate_repr("key", "value", "origin", "from_cli")
class Setting(StringConverter):
    """
    A Setting consists mainly of a key and a value. It mainly offers many
    conversions into common data types.
    """

    def __init__(self,
                 key,
                 value,
                 origin="",
                 strip_whitespaces=True,
                 list_delimiters=(",", ";"),
                 from_cli=False):
        """
        Initializes a new Setting,

        :param key:               The key of the Setting
        :param value:             The value, if you apply conversions to this
                                  object these will be applied to this value.
        :param origin:            The originating file. This will be used for
                                  path conversions and the last part will be
                                  stripped of. If you want to specify a
                                  directory as origin be sure to end it with a
                                  directory seperator.
        :param strip_whitespaces: Whether to strip whitespaces from the value
                                  or not
        :param list_delimiters:   Delimiters for list conversion
        :param from_cli:          True if this setting was read by the
                                  CliParser.
        """
        if not isinstance(from_cli, bool):
            raise TypeError("from_cli needs to be a boolean value.")

        StringConverter.__init__(self,
                                 value,
                                 strip_whitespaces=strip_whitespaces,
                                 list_delimiters=list_delimiters)
        self.from_cli = from_cli
        self.key = key
        self.origin = str(origin)

    def __path__(self, origin=None):
        """
        Determines the path of this setting.

        Note: You can also use this function on strings, in that case the
        origin argument will be taken in every case.

        :param origin:      the origin file to take if no origin is specified
                            for the given setting. If you want to provide a
                            directory, make sure it ends with a directory
                            seperator.
        :return:            An absolute path.
        :raises ValueError: If no origin is specified in the setting nor the
                            given origin parameter.
        """
        strrep = str(self).strip()
        if os.path.isabs(strrep):
            return strrep

        if hasattr(self, "origin") and self.origin != "":
            origin = self.origin

        if origin is None:
            raise ValueError("Cannot determine path without origin.")

        return os.path.abspath(os.path.join(os.path.dirname(origin), strrep))

    def __path_list__(self):
        """
        Splits the value into a list and creates a path out of each item taking
        the origin of the setting into account.

        :return: A list of absolute paths.
        """
        return [Setting.__path__(elem, self.origin) for elem in self]

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        newkey = str(key)
        if newkey == "":
            raise ValueError("An empty key is not allowed for a setting.")

        self._key = newkey
