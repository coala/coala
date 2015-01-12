"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from coalib.misc.StringConverter import StringConverter


class LineParser:
    def __init__(self,
                 key_value_delimiters=['=', ':'],
                 comment_seperators=['#', ';', '//'],
                 key_delimiters=[',', ' '],
                 section_name_surroundings={'[': "]"},
                 section_override_delimiters=["."]):
        """
        Creates a new line parser. Please note that no delimiter or seperator may be an "o" or you may encounter
        undefined behaviour with the escapes.

        :param key_value_delimiters: Delimiters that delimit a key from a value
        :param comment_seperators: Used to initiate a comment
        :param key_delimiters: Delimiters between several keys
        :param section_name_surroundings: Dictionary, e.g. {"[", "]"} means a section name is surrounded by [ and ].
        :param section_override_delimiters: Delimiter for a section override. E.g. "." would mean that section.key is a
        possible key that puts the key into the section "section" despite of the current section.
        :return:
        """
        self.key_value_delimiters = key_value_delimiters
        self.comment_seperators = comment_seperators
        self.key_delimiters = key_delimiters
        self.section_name_surroundings = section_name_surroundings
        self.section_override_delimiters = section_override_delimiters

    def parse(self, line):
        """
        Note that every value in the returned touple _besides the value_ is unescaped. This is so since the value is
        meant to be put into a Setting later thus the escapes may be needed there.

        :param line: the line to parse
        :return section_name (empty string if it's no section name), [(section_override, key), ...], value, comment
        """
        line, comment = self.__seperate_by_first_occurrence(line, self.comment_seperators)
        comment = self.remove_backslashes(comment)
        if line == "":
            return '', [], '', comment

        section_name = self.remove_backslashes(self.__get_section_name(line))
        if section_name != '':
            return section_name, [], '', comment

        keys, value = self.__extract_keys_and_value(line)  # Escapes in value might be needed by the bears

        key_touples = []
        for key in keys:
            section, key = self.__seperate_by_first_occurrence(key, self.section_override_delimiters, True, True)
            key_touples.append((self.remove_backslashes(section), self.remove_backslashes(key)))

        return '', key_touples, value, comment

    @staticmethod
    def remove_backslashes(string):
        i = string.find("\\")
        while i != -1:
            string = string[:i] + string[i+1:]
            i = string.find("\\", i+1)  # Dont check the next char

        return string

    @staticmethod
    def __seperate_by_first_occurrence(string, delimiters, strip_delim=False, return_second_part_nonempty=False):
        """
        Seperates a string by the first of all given delimiters. Any whitespace characters will be stripped away from
        the parts.

        :param string: The string to seperate.
        :param delimiters: The delimiters.
        :param strip_delim: Strips the delimiter from the result if true.
        :param return_second_part_nonempty: If no delimiter is found and this is true the contents of the string will be
        returned in the second part of the touple instead of the first one.
        :return: (first_part, second_part)
        """
        temp_string = string.replace("\\\\", "oo")
        i = temp_string.find("\\")
        while i != -1:
            temp_string = temp_string[:i] + "oo" + temp_string[i+2:]
            i = temp_string.find("\\", i+2)

        delim_pos = len(string)
        used_delim = ""
        for delim in delimiters:
            pos = temp_string.find(delim)
            if 0 <= pos < delim_pos:
                delim_pos = pos
                used_delim = delim

        if return_second_part_nonempty and delim_pos == len(string):
            return "", string.strip(" \n")

        return string[:delim_pos].strip(" \n"), \
               string[delim_pos + (len(used_delim) if strip_delim else 0):].strip(" \n")

    def __get_section_name(self, line):
        for begin, end in self.section_name_surroundings.items():
            if line[0:len(begin)] == begin and \
                            line[len(line) - len(end):len(line)] == end:
                return line[len(begin):len(line) - len(end)].lower().strip(" \n")

        return ''

    def __extract_keys_and_value(self, line):
        key_part, value = self.__seperate_by_first_occurrence(line, self.key_value_delimiters, True, True)
        keys = list(StringConverter(key_part, list_delimiters=self.key_delimiters).__iter__(remove_backslashes=False))

        return keys, value
