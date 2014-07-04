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

# noinspection PyUnresolvedReferences
from codeclib.fillib.misc import i18n
from codeclib.fillib.settings.Settings import Settings
from codeclib.internal.parsing.Parser import Parser


class ConfParser(Parser):
    def __init__(self,
                 key_value_delimiters=['=', ':'],
                 comment_seperators=['#', ';', '//'],
                 key_delimiters=[','],
                 section_name_surroundings={'[':"]"}):
        self.parsed = False
        self.key_value_delimiters = key_value_delimiters
        self.comment_seperators = comment_seperators
        self.key_delimiters = key_delimiters
        self.section_name_surroundings = section_name_surroundings
        self.sections = {}

    def parse(self, input_data, overwrite=False):
        """
        :param input_data: the filename of the config file to read
        :return a non empty string containing an error message on failure
        """
        try:
            f = open(input_data, "r")
            lines = f.readlines()
            name = "default"
            while True:
                if not overwrite:
                    settings = self.sections.get(name.lower(), Settings(name))
                else:
                    settings = Settings(name.lower())
                i, name = self.__parse_section(settings, lines)
                lines = lines[i:]
                self.sections[name.lower()] = settings
            f.close()
            self.parsed = True
            return ''
        except IOError:
            return _("Failed reading file. Please make sure to provide a file that is existent and "
                     "you have the permission to read it.")

    def reparse(self, input_data):
        """
        :param input_data: the filename of the config file to read
        :return a non empty string containing an error message on failure
        """
        return self.parse(input_data, True)

    def export_to_settings(self):
        assert self.parsed
        raise NotImplementedError

    def __line_is_section_name(self, line):
        for begin, end in self.section_name_surroundings.items():
            if line[0:len(begin)] == begin and line[len(line)-len(end):len(line)] == end:
                return True, line[len(begin):-len(end)]
        return False, ''

    def __parse_section(self, settings, lines, origin):
        """
        :param settings: the object to store the settings into
        :param lines: the lines to parse
        :param origin: origin for the settings
        :return: -1, '' if all lines are parsed, if not index of line which is the next section plus name of section
        """
        for i, line in enumerate(lines):
            line = line.strip(" \n")
            # extract comments
            comment, rest = self.__extract_comment(line)
            if comment:
                settings.append(comment.strip(), '', origin)

            # is it the next section?
            is_name, name = self.__line_is_section_name(rest)
            if is_name:
                return i, name

            # extract values
            keys, value = self.__extract_keys_and_value(rest)
            for key in keys:
                settings.append(key.strip(), value.strip(), origin)

        return -1, ''

    def __extract_comment(self, line):
        comment_begin = len(line)
        for seperator in self.comment_seperators:
            pos = line.find(seperator)
            if 0 < pos < comment_begin:
                comment_begin = pos

        return line[comment_begin:], line[:comment_begin]

    def __extract_keys_and_value(self, line):
        value_begin = len(line)
        value_delimiter = ''
        for delimiter in self.key_value_delimiters:
            pos = line.find(delimiter)
            if 0 < pos < value_begin:
                value_begin = pos
                value_delimiter = delimiter

        keys = line[:value_begin].strip().split(self.key_delimiters)
        return keys, line[value_begin+len(value_delimiter):]
