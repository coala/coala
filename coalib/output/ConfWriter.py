from itertools import chain

from pyprint.ClosableObject import ClosableObject

from coalib.parsing.StringProcessing import escape
from coalib.settings.Section import Section


class ConfWriter(ClosableObject):

    def __init__(self,
                 file_name,
                 key_value_delimiters=('=',),
                 comment_seperators=('#',),
                 key_delimiters=(',', ' '),
                 section_name_surroundings=None,
                 section_override_delimiters=(".",),
                 unsavable_keys=("save",)):
        section_name_surroundings = section_name_surroundings or {"[": "]"}
        ClosableObject.__init__(self)
        self.__file_name = file_name
        self.__file = open(self.__file_name, "w")
        self.__key_value_delimiters = key_value_delimiters
        self.__comment_seperators = comment_seperators
        self.__key_delimiters = key_delimiters
        self.__section_name_surroundings = section_name_surroundings
        self.__section_override_delimiters = section_override_delimiters
        self.__unsavable_keys = unsavable_keys
        self.__wrote_newline = True
        self.__closed = False

        self.__key_delimiter = self.__key_delimiters[0]
        self.__key_value_delimiter = self.__key_value_delimiters[0]
        (self.__section_name_surrounding_beg,
         self.__section_name_surrounding_end) = (
            tuple(self.__section_name_surroundings.items())[0])

    def _close(self):
        self.__file.close()

    def write_sections(self, sections):
        assert not self.__closed

        self.__wrote_newline = True
        for section in sections:
            self.write_section(sections[section])

    def write_section(self, section):
        assert not self.__closed

        if not isinstance(section, Section):
            raise TypeError

        self.__write_section_name(section.name)

        keys = []
        val = None
        section_iter = section.__iter__(ignore_defaults=True)
        try:
            while True:
                setting = section[next(section_iter)]
                if (str(setting) == val and
                    not self.is_comment(setting.key) and
                    (
                        (setting.key not in self.__unsavable_keys) or
                        (not setting.from_cli))):
                    keys.append(setting.key)
                elif ((setting.key not in self.__unsavable_keys) or
                      (not setting.from_cli)):
                    self.__write_key_val(keys, val)
                    keys = [setting.key]
                    val = str(setting)
        except StopIteration:
            self.__write_key_val(keys, val)

    def __write_section_name(self, name):
        assert not self.__closed

        if not self.__wrote_newline:
            self.__file.write("\n")

        self.__file.write(self.__section_name_surrounding_beg + name +
                          self.__section_name_surrounding_end + '\n')
        self.__wrote_newline = False

    def __write_key_val(self, keys, val):
        assert not self.__closed

        if keys == []:
            return

        if all(self.is_comment(key) for key in keys):
            self.__file.write(val + "\n")
            self.__wrote_newline = val == ""
            return

        # Add escape characters as appropriate
        keys = [escape(key, chain(['\\'],
                                  self.__key_value_delimiters,
                                  self.__comment_seperators,
                                  self.__key_delimiters,
                                  self.__section_override_delimiters))
                for key in keys]
        val = escape(val, chain(['\\'], self.__comment_seperators))

        self.__file.write((self.__key_delimiter + " ").join(keys) + " " +
                          self.__key_value_delimiter + " " + val + "\n")
        self.__wrote_newline = False

    @staticmethod
    def is_comment(key):
        return key.lower().startswith("comment")
