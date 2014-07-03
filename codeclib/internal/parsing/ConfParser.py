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
    def __init__(self):
        self.parsed = False
        # ignore comments and keep them as keys without value
        self.parser = self.__get_config_parser()

    def parse(self, input_data):
        """
        :param input_data: the filename of the config file to read
        """
        if not self.parsed:
            self.reparse(input_data)
        else:
            # add new data to the existing
            tmpparser = self.__get_config_parser()
            tmpparser.read(input_data)
            self.__import_data_from_configparser(tmpparser)

    def __import_data_from_configparser(self, configparser):
        assert self.parsed

        for section_name in configparser:
            section = configparser[section_name]
            if section_name not in self.parser:
                self.parser.add_section(section)

            for key in section:
                self.parser[section_name][key] = section[key]
                pass

    def reparse(self, input_data):
        """
        :param input_data: the filename of the config file to read
        """
        self.parser.read(input_data)
        self.parsed = True

    def export_to_settings(self):
        assert self.parsed

        result = []
        for section in self.parser:
            settings = Settings(section)
            settings.import_section(self.parser)
            result.append(settings)

        return result

    @staticmethod
    def __get_config_parser():
        return ConfigParser(allow_no_value=True, comment_prefixes='', empty_lines_in_values=False)
