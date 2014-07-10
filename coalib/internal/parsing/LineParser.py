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


class LineParser:
    def __init__(self,
                 key_value_delimiters=['=', ':'],
                 comment_seperators=['#', ';', '//'],
                 key_delimiters=[',',' '],
                 section_name_surroundings={'[': "]"}):
        self.key_value_delimiters = key_value_delimiters
        self.comment_seperators = comment_seperators
        self.key_delimiters = key_delimiters
        self.section_name_surroundings = section_name_surroundings

    def parse(self, line):
        """
        :param line: the line to parse
        :return section_name (empty string if it's no section name), keys, value, comment
        """
        line, comment = self.__extract_comment(line)
        if line == "":
            return '', [], '', comment

        section_name = self.__get_section_name(line)
        if section_name != '':
            return section_name, [], '', comment

        keys, value = self.__extract_keys_and_value(line)

        return '', keys, value, comment

    def __get_section_name(self, line):
        for begin, end in self.section_name_surroundings.items():
            if line[0:len(begin)] == begin and \
               line[len(line)-len(end):len(line)] == end:
                return line[len(begin):len(line)-len(end)].lower().strip(" \n")

        return ''

    def __extract_comment(self, line):
        comment_begin = len(line)
        for seperator in self.comment_seperators:
            pos = line.find(seperator)
            if 0 <= pos < comment_begin:
                comment_begin = pos

        return line[:comment_begin].strip(" \n"), line[comment_begin:].strip(" \n")

    def __extract_keys_and_value(self, line):
        value_begin = len(line)
        value_delimiter = ''
        for delimiter in self.key_value_delimiters:
            pos = line.find(delimiter)
            if 0 < pos < value_begin:
                value_begin = pos
                value_delimiter = delimiter

        tmp_keys = [line[:value_begin]]
        for delim in self.key_delimiters:
            new = []
            for key in tmp_keys:
                new += key.split(delim)
            tmp_keys = new

        keys=[]
        for i, key in enumerate(tmp_keys):
            if key.strip(" \n") != "":
                keys.append(key.strip(" \n"))

        return keys, line[value_begin+len(value_delimiter):].strip(" \n")
