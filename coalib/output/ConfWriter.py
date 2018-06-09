from itertools import chain
import os
from types import MappingProxyType

from pyprint.ClosableObject import ClosableObject

from coala_utils.string_processing import escape
from coalib.settings.Section import Section


class ConfWriter(ClosableObject):

    def __init__(self,
                 file_name,
                 key_value_delimiters=('=',),
                 comment_separators=('#',),
                 key_delimiters=(',', ' '),
                 section_name_surroundings=MappingProxyType({'[': ']'}),
                 section_override_delimiters=('.',),
                 unsavable_keys=('save',),
                 key_value_append_delimiters=('+=',)):
        ClosableObject.__init__(self)

        self.__file_name = file_name
        if (os.path.isdir(self.__file_name)):
            self.__file_name = os.path.join(self.__file_name, '.coafile')

        self.__file = open(self.__file_name, 'w')
        self.__key_value_delimiters = key_value_delimiters
        self.__key_value_append_delimiters = key_value_append_delimiters
        self.__comment_separators = comment_separators
        self.__key_delimiters = key_delimiters
        self.__section_name_surroundings = section_name_surroundings
        self.__section_override_delimiters = section_override_delimiters
        self.__unsavable_keys = unsavable_keys
        self.__closed = False

        self.__key_delimiter = self.__key_delimiters[0]
        self.__key_value_delimiter = key_value_delimiters[0]
        self.__key_value_append_delimiter = key_value_append_delimiters[0]
        (self.__section_name_surrounding_beg,
         self.__section_name_surrounding_end) = (
            tuple(self.__section_name_surroundings.items())[0])

    def _close(self):
        self.__file.close()

    def write_sections(self, sections):
        assert not self.__closed

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
                    self.__write_key_val(keys, val, section.defaults)
                    keys = [setting.key]
                    val = str(setting)
        except StopIteration:
            self.__write_key_val(keys, val, section.defaults)

    def __write_section_name(self, name):
        assert not self.__closed

        self.__file.write(self.__section_name_surrounding_beg + name +
                          self.__section_name_surrounding_end + '\n')

    def __write_key_val(self, keys, val, defaults):
        assert not self.__closed

        if keys == []:
            return

        if all(self.is_comment(key) for key in keys):
            self.__file.write(val + '\n')
            return

        # Add escape characters as appropriate
        keys = [escape(key, chain(['\\'],
                                  self.__key_value_delimiters,
                                  self.__comment_separators,
                                  self.__key_delimiters,
                                  self.__section_override_delimiters))
                for key in keys]
        val = escape(val, chain(['\\'], self.__comment_separators))

        append_keys = []
        other_keys = []
        for key in keys:
            if (defaults and
                    (key in defaults and
                     val.startswith(str(defaults[key])+','))):
                append_keys.append(key)
            else:
                other_keys.append(key)
        self.__write_keys_val_to_file(append_keys, other_keys, val, defaults)

    def __write_keys_val_to_file(self, append_keys, other_keys, val, defaults):
        """
        This method helps in grouping keys with common appendable values and
        writing all keys to the file.

        :param append_keys: The keys that have to be written with an append
                            delimiter.
        :param other_keys:  The keys that have to be written with a normal
                            delimiter.
        :param val:         The value to be written for the keys.
        :param defaults:    The defaults of the section the keys and value are
                            to be written to.
        """
        if append_keys:
            append_keys = sorted(append_keys,
                                 key=lambda key: len(defaults[str(key)]),
                                 reverse=True)
            write_keys = []
            def_val = None
            for key in append_keys:
                if str(defaults[key]) == def_val:
                    write_keys.append(key)
                    continue
                else:
                    if write_keys:
                        append_val = self.__get_append_val(val, def_val)
                        self.__write_value(
                            write_keys,
                            append_val,
                            self.__key_value_append_delimiter)
                    write_keys = [key]
                    def_val = str(defaults[key])
            append_val = self.__get_append_val(val, def_val)
            self.__write_value(write_keys,
                               append_val,
                               self.__key_value_append_delimiter)

        if other_keys:
            self.__write_value(other_keys,
                               val,
                               self.__key_value_delimiter)

    def __get_append_val(self, val, def_val):
        def_val_list = def_val.split(self.__key_delimiter)
        append_val = (self.__key_delimiter + ' ').join(
            [v.strip() for v in val.split(
                self.__key_delimiter)
             if v not in def_val_list])
        return append_val

    def __write_value(self, keys, val, delimiter):
        self.__file.write((self.__key_delimiter + ' ').join(keys) +
                          ' ' + delimiter + ' ' +
                          val + '\n')

    @staticmethod
    def is_comment(key):
        return key.lower().startswith('comment')
