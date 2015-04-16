import re
from coalib.misc.StringConstants import StringConstants
from coalib.parsing import StringProcessing


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

    def __prepare_list(self, remove_backslashes):
        def unescape(string):
            i = string.find("\\")
            while i != -1:
                string = string[:i] + string[i+1:]
                i = string.find("\\", i+1)  # Dont check the next char

            return string

        if not self.__recreate_list:
            return

        pattern = ("(?:" +
                   "|".join(re.escape(v) for v in self.__list_delimiters) +
                   ")")

        self.__list = list(StringProcessing.unescaped_split(
            pattern,
            self.value,
            use_regex=True))

        if remove_backslashes:
            self.__list = [unescape(elem) for elem in self.__list]
        if self.__strip_whitespaces:
            self.__list = [elem.strip() for elem in self.__list]

        # Need to do after stripping, cant use builtin functionality of split
        while "" in self.__list:
            self.__list.remove("")

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
