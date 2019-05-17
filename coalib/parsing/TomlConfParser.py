import logging

import toml
import os

from coalib.misc import Constants
from collections import OrderedDict

from coalib.results.SourcePosition import SourcePosition
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class TomlConfParser:

    def __init__(self, remove_empty_iter_elements=True):

        self.sections = None
        self.data = None
        self.__init_sections()
        self.__remove_empty_iter_elements = remove_empty_iter_elements

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
            input_data = os.path.join(input_data, Constants.local_coafile_toml)

        if overwrite:
            self.__init_sections()

        self.data = toml.load(input_data, OrderedDict)

        for item in self.data.items():
            self.generate_section(item, input_data)

        return self.sections

    def get_section(self, name, create_if_not_exists=False):
        """
        Returns or creates a section with given name

        :param name: The name of the section
        :param create_if_not_exists: create a section if it does not exist
        :return: Section of given name
        """
        key = self.__refine_key(name)
        sec = self.sections.get(key, None)
        if sec is not None:
            return sec

        if not create_if_not_exists:
            raise IndexError

        retval = self.sections[key] = Section(str(name))
        return retval

    @staticmethod
    def __refine_key(key):
        return str(key).lower().strip()

    def generate_section(self, item, origin):
        """
        Generates section

        :param item: Configuration group
        :param origin: The file from which the configuration originated
        """

        section_name = item[0]
        section_content = item[1]
        appends = []

        if not isinstance(section_content, OrderedDict):
            logging.warning('A setting does not have a section.'
                            'This is a deprecated feature please '
                            'put this setting in a section defined'
                            ' with `[<your-section-name]` in a '
                            'configuration file.')
            self.create_setting(self.get_section('default', True),
                                section_name,
                                section_content,
                                origin,
                                False
                                )
            return

        if 'appends' in section_content.keys():
            appends.append(section_content.get('appends'))
            del section_content['appends']

        current_section = self.get_section(section_name, True)
        for content_key, content_value in section_content.items():
            key = content_key
            value = content_value
            to_append = False
            if isinstance(content_value, OrderedDict):
                self.generate_aspects(content_key, content_value,
                                      current_section, appends,
                                      origin)
                continue

            if not isinstance(value, str):
                value = self.format_value(value)

            if key in appends:
                to_append = True

            self.create_setting(current_section, key, value, origin, to_append)

    def __init_sections(self):
        self.sections = OrderedDict()
        self.sections['default'] = Section('Default')

    def create_setting(self, current_section, key, value, origin, to_append):
        current_section.add_or_create_setting(
            Setting(key,
                    value,
                    SourcePosition(
                        str(origin)),
                    to_append=to_append,
                    # Start ignoring PEP8Bear, PycodestyleBear*
                    # they fail to resolve this
                    remove_empty_iter_elements=
                    self.__remove_empty_iter_elements),
            # Stop ignoring
            allow_appending=(key == []))

    def generate_aspects(self, content_key, content_value,
                         current_section, appends, origin):
        """
        Generates aspects related settings

        :param origin: The origin of the settings
        :param appends: The list containing the settings to be appended
        :param content_key: Aspect group name
        :param content_value: Aspect group value
        :param current_section: The section the aspects belong to
        """

        base_key = content_key
        for k, v in content_value.items():
            key = base_key + ':' + k
            if isinstance(v, OrderedDict):
                self.generate_aspects(key, v, current_section, appends,
                                      origin)
                continue

            if not isinstance(v, str):
                v = self.format_value(v)

            to_append = False

            if base_key + '.' + k in appends:
                to_append = True

            self.create_setting(current_section, key, v, origin, to_append)

    @staticmethod
    def format_value(value):
        if isinstance(value, list):
            return ', '.join(value)
        elif isinstance(value, (int, bool)):
            return str(value)
        else:
            return value
