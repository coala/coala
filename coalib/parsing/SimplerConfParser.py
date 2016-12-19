import os
import re
import configparser
from collections import OrderedDict
from types import MappingProxyType

from coalib.misc import Constants
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class SimplerConfParser:

    def __init__(self,
                 # the rest is for temporary compatibility with ConfParser
                 key_value_define_delimiters=('=',),
                 key_value_append_delimiters=('+=',),
                 comment_seperators=('#',),
                 key_delimiters=(',', ' '),
                 section_name_surroundings=MappingProxyType({'[': ']'}),
                 remove_empty_iter_elements=True):
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

        if overwrite:
            self.__init_sections()

        raw = configparser.ConfigParser(comment_prefixes=None,
                                        allow_no_value=True)
        with open(input_data, 'r', encoding='utf-8') as _file:
            raw.read_file(_file)

        for name in raw.sections():
            section = self.sections.setdefault(
                name.lower(), Section(name, self.sections['default']))
            for keys, value in raw.items(name):
                if keys.startswith('#'):
                    self.__add_comment(section, comment=keys, origin=input_data)
                else:
                    comments = []
                    lines, value = value.split('\n'), ''
                    for line in lines:
                        if re.match(r'[^\\]#', line):
                            data, comment = re.split(r'[^\\]#', line, 1)
                            comments.append(comment)
                            value += '\n' + data.strip()
                        else:
                            value += '\n' + line
                    do_append_value = keys.endswith('+')
                    if do_append_value:
                        keys = keys.rstrip('+')
                    for key in map(str.strip, keys.split(',')):
                        section.add_or_create_setting(Setting(
                            key, value, to_append=do_append_value,
                            origin=input_data))
                    for comment in comments:
                        self.__add_comment(section, '#' + comment,
                                           origin=input_data)

        return self.sections

    def __add_comment(self, section, comment, origin):
        key = 'comment' + str(self.__rand_helper)
        self.__rand_helper += 1
        section.append(Setting(key, comment, origin))

    def __init_sections(self):
        self.sections = OrderedDict()
        self.sections['default'] = Section('Default')
        self.__rand_helper = 0
