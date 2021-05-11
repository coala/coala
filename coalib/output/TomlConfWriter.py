import os

from coala_utils.string_processing import unescape
from coalib.parsing.TomlConfParser import TomlSetting

from tomlkit import document, table, dumps, array, string, key, integer
from tomlkit.items import (Array, String, Bool, Integer, Comment, Key,
                           KeyType, Trivia)


class TomlWriter:

    def __init__(self, file):
        self.file = file
        self.unsavable_keys = ['save', 'toml_config']
        self.document = document()

    def write_to_file(self):
        """
        Write the TOML document in the specified file
        """
        with open(self.file, 'w') as f:
            f.write(dumps(self.document))

    @staticmethod
    def get_original_value(value):
        """
        Converts a string into its original value

        :param value: The value as a string
        :return: The original value deduced from the string
        """

        if ',' in value:
            v = [unescape(v) for v in value.split(',')]
            return [unescape(v, '\n').strip() for v in v]

        if value.lower() == 'true':
            return True

        if value.lower() == 'false':
            return False

        if value.isdigit():
            return int(value)

        return unescape(value)

    @staticmethod
    def get_setting_key(setting):
        """
        Returns the key of a setting as a
        TomlKit key object

        :param setting: The setting from a section
        :return: The setting key as a TomlKit key object
        """
        if ':' in setting.key:
            count = setting.key.count(':')
            setting_key = Key(setting.key.replace(':', '.', count),
                              t=KeyType.Bare,
                              dotted=True)
        else:
            setting_key = key(setting.key)
        return setting_key


class TomlConfWriter(TomlWriter):
    """
    Class that contains functions for
    converting toml sections to toml
    file
    """

    def __init__(self, file):
        super().__init__(file)
        if os.path.isdir(self.file):
            self.file = os.path.join(self.file, '.coafile.toml')

    def write(self, sections):
        """
        Converts the given sections into a TOML
        document and writes the document into
        the specified file

        :param sections: The sections that have to be
                         written into the file
        """

        if sections.get('cli', None):
            self.remove_unsavable_settings(sections)

        for item in sections:
            section = sections[item]
            table_name = self.get_table_name(section)
            if table_name in self.document:
                continue
            table_contents = table()
            for _, setting in section.contents.items():

                setting_key = self.get_setting_key(setting)

                if isinstance(setting, TomlSetting):
                    value = setting.original_value
                else:
                    value = self.get_original_value(setting.value)

                if isinstance(value, Array):
                    table_contents.add(setting_key, array(value.as_string()))
                    if value.trivia.comment:
                        table_contents[setting_key].comment(value.trivia
                                                            .comment)
                elif isinstance(value, String):
                    table_contents.add(setting_key, string(value))
                    if value.trivia.comment:
                        table_contents[setting_key].comment(value.trivia
                                                            .comment)
                elif isinstance(value, Bool):
                    table_contents.add(setting_key, value)
                elif isinstance(value, Integer):
                    table_contents.add(setting_key, integer(value.as_string()))
                    if value.trivia.comment:
                        table_contents[setting_key].comment(value.trivia
                                                            .comment)
                elif isinstance(value, Comment):
                    table_contents.add(Comment(
                        Trivia(comment_ws='  ', comment=str(value))
                    ))
                else:
                    table_contents.add(setting_key, value)

            self.document.add(table_name, table_contents)
        self.write_to_file()

    def remove_unsavable_settings(self, sections):
        """
        Removes the un-savable keys from the sections
        before they are written into a file

        :param sections: The sections that have to be
                         written into the file
        """

        cli_section_contents = sections['cli'].contents
        for unsavable_key in self.unsavable_keys:
            if unsavable_key in cli_section_contents:
                del cli_section_contents[unsavable_key]

    @staticmethod
    def get_table_name(section):
        """
        Returns the table name for a section

        :param section: The section to obtain the table name from
        :return: Returns the table name obtained from the section name
        """
        name = section.name

        if name.startswith('"') or name.startswith("'"):
            start_quote = name[0]
            if start_quote == "'":
                return Key(unescape(name, "\\'"), t=KeyType.Literal)
            else:
                return Key(unescape(name, '\\"'), t=KeyType.Basic)

        if '.' in name:
            parent = ''
            inherits = section.contents.get('inherits').original_value
            parent_pos = -1
            if isinstance(inherits, Array):
                i = 0
                while parent_pos == -1:
                    parent = inherits[i]
                    parent_pos = name.find(parent)
                    i += 1
            else:
                parent = inherits
                parent_pos = name.find(parent)
            name = name[parent_pos + len(parent) + 1:]
            return key(name)

        return key(name)
