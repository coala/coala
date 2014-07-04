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
from configparser import ConfigParser
from codeclib.fillib.settings.Settings import Settings
from codeclib.internal.parsing.Parser import Parser


class ConfParser(Parser):
    def __init__(self,
                 key_value_delimiters=['=', ':'],
                 comment_seperators=['#', ';', '//'],
                 key_delimiters=[',']):
        self.parsed = False
        self.key_value_delimiters = key_value_delimiters
        self.comment_seperators = comment_seperators
        self.key_delimiters = key_delimiters

    def parse(self, input_data):
        """
        :param input_data: the filename of the config file to read
        """
        raise NotImplementedError
        self.parsed = True

    def reparse(self, input_data):
        """
        :param input_data: the filename of the config file to read
        """
        raise NotImplementedError
        self.parsed = True

    def export_to_settings(self):
        assert self.parsed
        raise NotImplementedError

    def __parse_section(self, settings, lines, origin):
        for line in lines:
            keys, value, comment = self.__parse_line(line)
            if comment:
                settings.append(comment.strip(), '', origin)
            for key in keys:
                settings.append(key.strip(), value.strip(), origin)

    def __parse_line(self, line):
        line.strip(" \n")
        comment, rest = self.__extract_comment(line)
        keys, value = self.__extract_keys_and_value(rest)
        return keys, value, comment

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
