from collections import OrderedDict
import sys
import os

from coalib.parsing.LineParser import LineParser
from coalib.settings.Setting import Setting
from coalib.settings.Section import Section


class ConfParser:
    if sys.version_info < (3, 3):  # pragma: no cover
        FileNotFoundError = IOError
    else:
        FileNotFoundError = FileNotFoundError

    def __init__(self,
                 key_value_delimiters=('=',),
                 comment_seperators=('#', ';', '//'),
                 key_delimiters=(',', ' '),
                 section_name_surroundings=None):
        section_name_surroundings = section_name_surroundings or {"[": "]"}

        self.line_parser = LineParser(key_value_delimiters,
                                      comment_seperators,
                                      key_delimiters,
                                      section_name_surroundings)

        # Declare it
        self.sections = None
        self.__rand_helper = None
        self.__init_sections()

    def parse(self, input_data, overwrite=False):
        """
        Parses the input and adds the new data to the existing. If you want to
        catch the FileNotFoundError please take the FileNotFoundError member of
        this object for catching for backwards compatability to python 3.2.

        :param input_data: filename
        :param overwrite:  behaves like reparse if this is True
        :return:           the settings dictionary
        """
        if os.path.isdir(input_data):
            input_data = os.path.join(input_data, ".coafile")

        with open(input_data, "r", encoding='utf-8') as _file:
            lines = _file.readlines()

        if overwrite:
            self.__init_sections()

        self.__parse_lines(lines, input_data)

        return self.sections

    def get_section(self, name, create_if_not_exists=False):
        key = self.__refine_key(name)
        sec = self.sections.get(key, None)
        if sec is not None:
            return sec

        if not create_if_not_exists:
            raise IndexError

        retval = self.sections[key] = Section(str(name),
                                              self.sections["default"])
        return retval

    @staticmethod
    def __refine_key(key):
        return str(key).lower().strip()

    def __add_comment(self, section, comment, origin):
        key = "comment" + str(self.__rand_helper)
        self.__rand_helper += 1
        section.append(Setting(key, comment, origin))

    def __parse_lines(self, lines, origin):
        current_section_name = "default"
        current_section = self.get_section(current_section_name)
        current_keys = []

        for line in lines:
            section_name, keys, value, comment = self.line_parser.parse(line)

            if comment != "":
                self.__add_comment(current_section, comment, origin)

            if section_name != "":
                current_section_name = section_name
                current_section = self.get_section(current_section_name, True)
                current_keys = []
                continue

            if comment == "" and keys == [] and value == "":
                self.__add_comment(current_section, "", origin)
                continue

            if keys != []:
                current_keys = keys

            for section_override, key in current_keys:
                if key == "":
                    continue

                if section_override == "":
                    current_section.add_or_create_setting(
                        Setting(key, value, origin),
                        allow_appending=(keys == []))
                else:
                    self.get_section(
                        section_override,
                        True).add_or_create_setting(
                            Setting(key, value, origin),
                            allow_appending=(keys == []))

    def __init_sections(self):
        self.sections = OrderedDict()
        self.sections["default"] = Section("Default")
        self.__rand_helper = 0
