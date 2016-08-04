import os
from collections import OrderedDict
from types import MappingProxyType

from coalib.misc import Constants
from coalib.parsing.LineParser import LineParser
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class ConfParser:

    def __init__(self,
                 key_value_delimiters=('=',),
                 comment_seperators=('#',),
                 key_delimiters=(',', ' '),
                 section_name_surroundings=MappingProxyType({"[": "]"}),
                 remove_empty_iter_elements=True):
        self.line_parser = LineParser(key_value_delimiters,
                                      comment_seperators,
                                      key_delimiters,
                                      section_name_surroundings)

        self.__remove_empty_iter_elements = remove_empty_iter_elements

        # Declare it
        self.sections = None
        self.__rand_helper = None
        self.__init_sections()

    def parse(self, input_data, overwrite=False):
        """
        Parses the input and adds the new data to the existing.

        :param input_data: The filename to parse from.
        :param overwrite:  If True, wipes all existing Settings inside this
                           instance and adds only the newly parsed ones. If
                           False, adds the newly parsed data to the existing
                           one (and overwrites already existing keys with the
                           newly parsed values).
        :return:           A dictionary with (lowercase) section names as keys
                           and their Setting objects as values.
        """
        if os.path.isdir(input_data):
            input_data = os.path.join(input_data, Constants.default_coafile)

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
        section.append(Setting(
            key,
            comment,
            origin,
            remove_empty_iter_elements=self.__remove_empty_iter_elements))

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
                        Setting(key,
                                value,
                                origin,
                                # Ignore PEP8Bear, it fails to format that
                                remove_empty_iter_elements=
                                self.__remove_empty_iter_elements),
                        allow_appending=(keys == []))
                else:
                    self.get_section(
                        section_override,
                        True).add_or_create_setting(
                            Setting(key,
                                    value,
                                    origin,
                                    # Ignore PEP8Bear, it fails to format that
                                    remove_empty_iter_elements=
                                    self.__remove_empty_iter_elements),
                            allow_appending=(keys == []))

    def __init_sections(self):
        self.sections = OrderedDict()
        self.sections["default"] = Section("Default")
        self.__rand_helper = 0
