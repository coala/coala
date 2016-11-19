from coala_utils.string_processing.StringConverter import StringConverter
from coala_utils.string_processing import (unescape, convert_to_raw,
                                           position_is_escaped,
                                           unescaped_rstrip)


class LineParser:

    def __init__(self,
                 key_value_delimiters=('=',),
                 comment_separators=('#',),
                 key_delimiters=(',', ' '),
                 section_name_surroundings=None,
                 section_override_delimiters=('.',)):
        """
        Creates a new line parser. Please note that no delimiter or separator
        may be an "o" or you may encounter undefined behaviour with the
        escapes.

        :param key_value_delimiters:        Delimiters that delimit a key from
                                            a value.
        :param comment_separators:          Used to initiate a comment.
        :param key_delimiters:              Delimiters between several keys.
        :param section_name_surroundings:   Dictionary, e.g. {"[", "]"} means a
                                            section name is surrounded by [].
                                            If None, {"[": "]"} is used as
                                            default.
        :param section_override_delimiters: Delimiter for a section override.
                                            E.g. "." would mean that
                                            section.key is a possible key that
                                            puts the key into the section
                                            "section" despite of the current
                                            section.
        """
        section_name_surroundings = (
            {'[': ']'} if section_name_surroundings is None
            else section_name_surroundings)

        self.key_value_delimiters = key_value_delimiters
        self.comment_separators = comment_separators
        self.key_delimiters = key_delimiters
        self.section_name_surroundings = section_name_surroundings
        self.section_override_delimiters = section_override_delimiters

    def parse(self, line):
        """
        Note that every value in the returned tuple *besides the value* is
        unescaped. This is so since the value is meant to be put into a Setting
        later thus the escapes may be needed there.

        :param line: The line to parse.
        :return:     section_name (empty string if it's no section name),
                     [(section_override, key), ...], value, comment
        """
        line, comment = self.__separate_by_first_occurrence(
            line,
            self.comment_separators)
        comment = unescape(comment)
        if line == '':
            return '', [], '', comment

        section_name = unescape(self.__get_section_name(line))
        if section_name != '':
            return section_name, [], '', comment

        # Escapes in value might be needed by the bears
        keys, value = self.__extract_keys_and_value(line)

        # Add all the delimiters that stored as tuples
        all_delimiters = self.key_value_delimiters
        all_delimiters += self.key_delimiters
        all_delimiters += self.comment_separators
        all_delimiters += self.section_override_delimiters
        all_delimiters = ''.join(all_delimiters)

        # Add all keys and values in section_name_surroundings, which is
        # stored as a dict
        all_delimiters += ''.join(self.section_name_surroundings.keys())
        all_delimiters += ''.join(self.section_name_surroundings.values())

        value = convert_to_raw(value, all_delimiters)

        key_tuples = []
        for key in keys:
            key = convert_to_raw(key, all_delimiters)
            section, key = self.__separate_by_first_occurrence(
                key,
                self.section_override_delimiters,
                True,
                True)
            key_tuples.append((unescape(section), unescape(key)))

        return '', key_tuples, value, comment

    @staticmethod
    def __separate_by_first_occurrence(string,
                                       delimiters,
                                       strip_delim=False,
                                       return_second_part_nonempty=False):
        """
        Separates a string by the first of all given delimiters. Any whitespace
        characters will be stripped away from the parts.

        :param string:                      The string to separate.
        :param delimiters:                  The delimiters.
        :param strip_delim:                 Strips the delimiter from the
                                            result if true.
        :param return_second_part_nonempty: If no delimiter is found and this
                                            is true the contents of the string
                                            will be returned in the second part
                                            of the tuple instead of the first
                                            one.
        :return:                            (first_part, second_part)
        """
        temp_string = string.replace('\\\\', 'oo')
        i = temp_string.find('\\')
        while i != -1:
            temp_string = temp_string[:i] + 'oo' + temp_string[i+2:]
            i = temp_string.find('\\', i+2)

        delim_pos = len(string)
        used_delim = ''
        for delim in delimiters:
            pos = temp_string.find(delim)
            if 0 <= pos < delim_pos:
                delim_pos = pos
                used_delim = delim

        if return_second_part_nonempty and delim_pos == len(string):
            return '', string.strip(' \n')

        first_part = string[:delim_pos]
        second_part = string[delim_pos + (
            len(used_delim) if strip_delim else 0):]

        if not position_is_escaped(second_part, len(second_part) - 1):
            first_part = unescaped_rstrip(first_part)
            second_part = unescaped_rstrip(second_part)

        return (first_part.lstrip().rstrip('\n'),
                second_part.lstrip().rstrip('\n'))

    def __get_section_name(self, line):
        for begin, end in self.section_name_surroundings.items():
            if (line[0:len(begin)] == begin and
                    line[len(line) - len(end):len(line)] == end):
                return line[len(begin):len(line) - len(end)].strip(' \n')

        return ''

    def __extract_keys_and_value(self, line):
        key_part, value = self.__separate_by_first_occurrence(
            line,
            self.key_value_delimiters,
            True,
            True)
        keys = list(StringConverter(
            key_part,
            list_delimiters=self.key_delimiters).__iter__(
            remove_backslashes=False))

        return keys, value
