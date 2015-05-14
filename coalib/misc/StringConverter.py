import re
from coalib.misc.StringConstants import StringConstants
from coalib.parsing.StringProcessing import unescaped_split, unescape


class StringConverter:
    """
    Converts strings to other things as needed. If you need some kind of string
    conversion that is not implemented here, consider adding it so everyone
    gets something out of it.
    """

    def __init__(self,
                 value,
                 strip_whitespaces=True,
                 list_delimiters=None,
                 dict_delimiter=":"):
        if list_delimiters is None:
            list_delimiters = [",", ";"]

        if (
                not isinstance(list_delimiters, list) and
                not isinstance(list_delimiters, str)):
            raise TypeError("list_delimiters has to be a string or a list")
        if not isinstance(strip_whitespaces, bool):
            raise TypeError("strip_whitespaces has to be a bool parameter")

        self.__strip_whitespaces = strip_whitespaces
        self.__list_delimiters = list_delimiters
        self.__dict_delimiter = dict_delimiter

        self.__escaped_list = None
        self.__unescaped_list = None
        self.__dict = None
        self.value = value

    def __str__(self):
        return unescape(self.value)

    def __bool__(self):
        if str(self).lower() in StringConstants.TRUE_STRINGS:
            return True
        if str(self).lower() in StringConstants.FALSE_STRINGS:
            return False
        raise ValueError

    def __len__(self):
        return len(str(self))

    def __int__(self):
        return int(str(self))

    def __float__(self):
        return float(str(self))

    def __iter__(self, remove_backslashes=True):
        """
        Converts the value to a list using the delimiters given at construction
        time.

        Note that escaped values will be unescaped and escaped list delimiters
        will be allowed in values. If you need the escapes you should not
        use this routine.

        :param remove_backslashes: Whether or not to remove the backslashes
                                   after conversion.
        :return:                   An iterator over all values.
        """
        if remove_backslashes:
            return iter(self.__unescaped_list)
        else:
            return iter(self.__escaped_list)

    def __getitem__(self, item):
        return self.__dict.__getitem__(item)

    def keys(self):
        return self.__dict.keys()

    def __get_raw_list(self):
        pattern = ("(?:" +
                   "|".join(re.escape(v) for v in self.__list_delimiters) +
                   ")")

        return list(unescaped_split(pattern,
                                    self.value,
                                    use_regex=True))

    def __prepare_list(self):
        self.__escaped_list = self.__get_raw_list()
        self.__unescaped_list = [unescape(elem)
                                 for elem in self.__escaped_list]
        if self.__strip_whitespaces:
            self.__unescaped_list = [elem.strip()
                                     for elem in self.__unescaped_list]
            self.__escaped_list = [elem.strip()
                                   for elem in self.__escaped_list]

        # Need to do after stripping, cant use builtin functionality of split
        while "" in self.__unescaped_list:
            self.__unescaped_list.remove("")
        while "" in self.__escaped_list:
            self.__escaped_list.remove("")

    def __prepare_dict(self):
        self.__dict = {}
        for elem in self.__get_raw_list():
            key_val = [unescape(item)
                       for item in unescaped_split(self.__dict_delimiter,
                                                   elem,
                                                   max_split=1)]

            if self.__strip_whitespaces:
                key_val = [item.strip() for item in key_val]

            if not any(item != "" for item in key_val):
                continue

            if len(key_val) < 2:
                self.__dict[key_val[0]] = ""
            else:
                self.__dict[key_val[0]] = key_val[1]

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newval):
        self.__value = str(newval)
        if self.__strip_whitespaces:
            self.__value = self.__value.strip()

        self.__prepare_list()
        self.__prepare_dict()

    def __eq__(self, other):
        return isinstance(other, StringConverter) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)
