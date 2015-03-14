from coalib.misc.StringConstants import StringConstants


class StringConverter:
    """
    Converts strings to other things as needed. If you need some kind of string
    conversion that is not implemented here, consider adding it so everyone
    gets something out of it.
    """

    def __init__(self,
                 value,
                 strip_whitespaces=True,
                 list_delimiters=[",", ";"]):
        if (
                not isinstance(list_delimiters, list) and
                not isinstance(list_delimiters, str)):
            raise TypeError("list_delimiters has to be a string or a list")
        if not isinstance(strip_whitespaces, bool):
            raise TypeError("strip_whitespaces has to be a bool parameter")

        self.__strip_whitespaces = strip_whitespaces
        self.__list_delimiters = list_delimiters

        self.value = value
        self.__list = None
        self.__recreate_list = True

    def __str__(self):
        return self.value

    def __bool__(self):
        if self.value.lower() in StringConstants.TRUE_STRINGS:
            return True
        if self.value.lower() in StringConstants.FALSE_STRINGS:
            return False
        raise ValueError

    def __len__(self):
        return len(self.value)

    def __int__(self):
        return int(self.value)

    def __iter__(self, remove_backslashes=True):
        """
        Converts the value to a list using the delimiters given at construction
        time.

        Note that escaped values will be unescaped and escaped list delimiters
        will be allowed in values. If you need the escapes you should not
        use this routine.

        :return: A list with unescaped values.
        """
        self.__prepare_list(remove_backslashes)

        return iter(self.__list)

    def __appendelem(self, lst, elem):
        if elem != "":
            if self.__strip_whitespaces:
                lst.append(elem.strip())
            else:
                lst.append(elem)

    def __is_delimiter(self, value):
        """
        Determines if the value begins with a valid delimiter.

        :param value: The value to check
        :return:      The length of the matched delimiter or False if it doesnt
                      begin with one.
        """
        for delim in self.__list_delimiters:
            if value.startswith(delim):
                return len(delim)

        return False

    def __prepare_list(self, remove_backslashes):
        if not self.__recreate_list:
            return

        self.__list = []
        thiselem = ""
        backslash = False
        iterator = enumerate(self.value)
        for i, char in iterator:
            if backslash:
                thiselem += char
                backslash = False
                continue

            if char == "\\":
                if not remove_backslashes:
                    thiselem += char
                backslash = True
                continue

            delim_len = self.__is_delimiter(self.value[i:])
            if delim_len is not False:
                self.__appendelem(self.__list, thiselem)
                thiselem = ""
                [next(iterator) for j in range(delim_len - 1)]
                continue

            thiselem += char

        self.__appendelem(self.__list, thiselem)

        self.__recreate_list = False

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newval):
        self.__value = str(newval)
        if self.__strip_whitespaces:
            self.__value = self.__value.strip()

        self.__recreate_list = True

    def __eq__(self, other):
        return isinstance(other, StringConverter) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)
