import os
import sys

import tomlkit.container
import tomlkit.items
from coalib.misc import Constants
from tomlkit.exceptions import TOMLKitError
from tomlkit.items import Table, Item

from coalib.results.SourcePosition import SourcePosition
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from collections import Iterable, OrderedDict
import logging


class TomlSetting(Setting):
    """
    A subclass of a setting but has an additional parameter
    called the original value. This class is required to
    infer comments and original data-type of a settings value.
    """

    def __init__(self, key,
                 value,
                 original_value,
                 origin: (str, SourcePosition) = '',
                 strip_whitespaces: bool = True,
                 list_delimiters: Iterable = (',', ';'),
                 from_cli: bool = False,
                 remove_empty_iter_elements: bool = True,
                 to_append: bool = False,
                 ):
        self.original_value = original_value
        super(TomlSetting, self).__init__(
            key,
            value,
            origin,
            strip_whitespaces,
            list_delimiters,
            from_cli,
            remove_empty_iter_elements,
            to_append)


class TomlConfParser:
    """

    The parser that generates sections from data in
    TOML config files. Each TOML table is converted
    into a section and the all the sections are returned
    as a ordered dictionary of sections.

    """

    def __init__(self, remove_empty_iter_elements=True):

        self.sections = None
        self.data = None
        self.__rand_helper = None
        self.__init_sections()
        self.__remove_empty_iter_elements = remove_empty_iter_elements
        self.logger = logging.getLogger()

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

        try:
            with open(input_data, 'r') as file:
                self.data = tomlkit.parse(file.read())
        except TOMLKitError as e:
            self.logger.error('An error occurred during parsing', e)
            sys.exit()

        self.data = self.data.body

        for item in self.data:
            self.generate_section(item, input_data)
        return self.sections

    def get_section(self, name, create_if_not_exists=False):
        """
        Returns section with the given name if it exists,
        otherwise creates a new section with the given name.

        :param name: The name of the section to be returned
        :param create_if_not_exists: create the section if it does not exist
        :return: section of the given name
        """
        key = self.__refine_key(name)
        sec = self.sections.get(key, None)
        if sec is not None:
            return sec

        if not create_if_not_exists:
            self.logger.error('The requested section does not exist'
                              + 'Please create one before accessing')
            sys.exit()

        retval = self.sections[key] = Section(str(name))
        return retval

    @staticmethod
    def __refine_key(key):
        return str(key).lower().strip()

    def generate_section(self, item, origin):
        """
        This method is the core of the parser. It converts
        TOML tables into sections

        :param item: Configuration group
        :param origin: The file from which the configuration originated
        """

        section_name = item[0]
        section_content = item[1]
        appends = []

        # Add settings that do not belong to any sections into default section
        if not isinstance(section_content, Table):
            original_value = section_content
            current_section = self.get_section('default', True)
            logging.warning('A setting does not have a section.'
                            'This is a deprecated feature please '
                            'put this setting in a section defined'
                            ' with `[<your-section-name]` in a '
                            'configuration file.')

            # Store full-line comments that appear before any sections
            if section_name is None:
                section_content = section_content.as_string()
                section_name = '(' + 'comment' + str(self.__rand_helper) + ')'
                self.__rand_helper += 1

            self.create_setting(current_section,
                                section_name,
                                section_content,
                                original_value,
                                origin,
                                False
                                )
            return

        # Get the keys to be appended
        if 'appends' in section_content.keys():
            appends = section_content.get('appends')

        # If inherits = [ 'a' , 'b'] is in section 'all',
        # then generate 'all.a' and 'all.b' sections
        if 'inherits' in section_content.keys():

            inherits = section_content.get('inherits')

            if not isinstance(inherits, list):
                inherits = [inherits]

            for parent in inherits:
                s_appends = appends
                s_name = parent + '.' + section_name.as_string()
                current_section = self.get_section(s_name, True)
                if isinstance(appends, Table):
                    s_appends = appends.get(parent, [])
                self.fill_table_settings(current_section, section_content,
                                         origin, s_appends)
        else:

            section_name = section_name.as_string()
            current_section = self.get_section(section_name, True)
            self.fill_table_settings(current_section, section_content,
                                     origin, appends)

    def fill_table_settings(self, current_section, section_content,
                            origin, appends):
        """
        Parses a table into a section. Works on a single table
        at a time.

        :param current_section: The section under consideration
        :param section_content: The TOML table under consideration
        :param origin: The file from which the configuration originated
        :param appends: The list of the keys to be appended
        """
        for content_key, content_value in section_content.value.body:

            original_value = content_value
            # Handle full-line comments
            if content_key is None:
                self.store_full_line_comments(current_section, content_value,
                                              original_value, origin)
            else:
                content_key = content_key.as_string()
                if isinstance(content_value, Table):
                    self.handle_nested_table(content_key, content_value,
                                             current_section, appends,
                                             origin)
                    continue

                to_append = False

                if not isinstance(content_value, str):
                    content_value = self.format_value(content_value)

                if content_key in appends:
                    to_append = True

                self.create_setting(current_section, content_key, content_value,
                                    original_value, origin, to_append)

    def __init_sections(self):
        self.sections = OrderedDict()
        self.sections['default'] = Section('Default')
        self.__rand_helper = 0

    def create_setting(self, current_section, key, value, original_value,
                       origin, to_append):
        """
        Adds the given setting to the specified section
        """
        current_section.add_or_create_setting(
            TomlSetting(key,
                        value,
                        original_value,
                        SourcePosition(
                            str(origin)),
                        to_append=to_append,
                        # Start ignoring PEP8Bear, PycodestyleBear*
                        # they fail to resolve this
                        remove_empty_iter_elements=
                        self.__remove_empty_iter_elements),
            # Stop ignoring
            allow_appending=(key == []))

    def handle_nested_table(self, content_key, content_value,
                            current_section, appends, origin):
        """
        Converts a nested table into a section object

        :param origin: The file from which the configuration originated
        :param appends: The list of the keys to be appended
        :param content_key: The name of the nested table
        :param content_value: The values of the TOML table under consideration
        :param current_section:  The section under consideration
        """

        base_key = content_key
        for k, v in content_value.value.body:
            original_value = v
            if k is None:
                self.store_full_line_comments(current_section, content_value,
                                              original_value, origin)
            else:
                k = k.as_string()

                key = base_key + ':' + k

                if isinstance(v, Table):
                    self.handle_nested_table(key, v, current_section,
                                             appends, origin)
                    continue

                if not isinstance(v, str):
                    v = self.format_value(v)

                to_append = False

                if base_key + '.' + k in appends:
                    to_append = True

                self.create_setting(current_section, key, v, original_value,
                                    origin, to_append)

    def store_full_line_comments(self, current_section, content_value,
                                 original_value, origin):
        content_key = '(' + 'comment' + str(self.__rand_helper) + ')'
        self.__rand_helper += 1
        self.create_setting(current_section, content_key,
                            content_value.as_string(),
                            original_value,
                            origin, False)

    @staticmethod
    def format_value(value):
        """
        Converts a value of any type to a string
        :param value: The original value to be formatted
        :return: A value converted into a string
        """
        if isinstance(value, list):
            value = [str(i) for i in value]
            return ', '.join(value)

        if isinstance(value, Item):
            return value.as_string()

        return str(value)
