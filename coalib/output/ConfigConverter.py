import re

from coalib.output.ConfWriter import ConfWriter
from tomlkit import table, key
from tomlkit.items import Key, KeyType
from coalib.output.TomlConfWriter import TomlWriter


class ConfigConverter(TomlWriter):
    """
    Class that contains functions for generating
    coafile from toml sections and toml file from
    coala sections
    """

    def __init__(self, file):
        super().__init__(file)
        self.__key_delimiter = ','

    def coafile_to_toml(self, sections):
        """
        Creates a toml document from coafile
        sections

        :param sections: sections obtained from coafile
        """
        comment_regex = re.compile(r'comment[\d]+')

        if 'default' in sections.keys():
            self.remove_defaults(sections)

        for item in sections:
            section = sections[item]
            section.set_default_section(sections)
            table_name, inherits = self.get_section_name(section.name)

            if table_name in self.document:
                existing_table = self.document[table_name]
                existing_table.get('inherits', []).append(inherits)
                existing_table.add(Key('appends.{}'.format(inherits),
                                       t=KeyType.Bare,
                                       dotted=True),
                                   self.get_appended_keys(section))
                continue

            appends = []
            table_contents = table()
            defaults = section.defaults
            for _, setting in section.contents.items():
                setting_key = self.get_setting_key(setting)

                if comment_regex.search(setting_key.as_string()):
                    continue

                if (defaults and
                    (setting.key in defaults and
                     str(section.get(setting.key)).startswith(
                         str(defaults[setting.key]) + ','))):

                    appends.append(setting.key)
                    value = self.get_original_value(
                        self.__get_append_val(str(section.get(setting.key)),
                                              str(defaults[setting.key])))
                else:
                    value = self.get_original_value(setting.value)
                table_contents.add(setting_key, value)
            if not inherits == []:
                table_contents.add(key('inherits'), [inherits])

            if not appends == []:
                if inherits:
                    table_contents.add(Key('appends.{}'.format(inherits),
                                           t=KeyType.Bare,
                                           dotted=True), appends)
                else:
                    table_contents.add(key('appends'), appends)

            self.document.add(table_name, table_contents)
        self.write_to_file()

    def __get_append_val(self, val, def_val):
        def_val_list = def_val.split(self.__key_delimiter)
        append_val = (self.__key_delimiter + ' ').join(
            [v.strip() for v in val.split(
                self.__key_delimiter)
             if v not in def_val_list])
        return append_val

    def toml_to_coafile(self, sections):
        """
        Creates a coafile from TOML sections

        :param sections: sections obtained from TOML
        """
        appends_regex = re.compile(r'appends(:[\w]+)?')
        comment_regex = re.compile(r'comment[\d]+')

        self.remove_defaults(sections)

        for item in sections:
            to_delete = []
            section = sections[item]
            section.set_default_section(sections)
            for _, setting in section.contents.items():
                if setting.key == 'inherits':
                    to_delete.append(setting.key)
                if appends_regex.search(setting.key):
                    to_delete.append(setting.key)
                if comment_regex.search(setting.key):
                    if setting.value == '':
                        setting.key = setting.key[1:len(setting.key) - 1]
                    else:
                        to_delete.append(setting.key)
                if setting.key in self.unsavable_keys:
                    to_delete.append(setting.key)

            for setting_key in to_delete:
                section.delete_setting(setting_key)
        conf_writer = ConfWriter(self.file)
        conf_writer.write_sections(sections)
        conf_writer.close()

    @staticmethod
    def remove_defaults(sections):
        if not sections['default'].contents == {}:
            sections['default'].name = 'cli'
            sections['cli'] = sections['default']
        del sections['default']

    @staticmethod
    def get_appended_keys(section):
        """
        Gets the keys of the settings to be appended
        """
        appends = []
        for _, setting in section.contents.items():

            if setting.to_append:
                appends.append(setting.key)

        return appends

    @staticmethod
    def get_section_name(section_name):
        """
        Returns the table name for a section name
        """
        dot_pos = section_name.rfind('.')

        inherits = []
        if dot_pos != -1:
            inherits = section_name[:dot_pos]

        return section_name[dot_pos + 1:], inherits
