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

from codeclib.fillib.misc.i18n import _
from codeclib.fillib.settings.Settings import Settings
from codeclib.internal.parsing.LineParser import LineParser
from codeclib.internal.parsing.Parser import Parser


class ConfParser(Parser):
    def __init__(self,
                 key_value_delimiters=['=', ':'],
                 comment_seperators=['#', ';', '//'],
                 key_delimiters=[',',' '],
                 section_name_surroundings={'[':"]"}):
        Parser.__init__(self)
        self.parsed = False
        self.line_parser = LineParser(key_value_delimiters,
                                      comment_seperators,
                                      key_delimiters,
                                      section_name_surroundings)
        self.sections = {}

    def parse(self, input_data, overwrite=False):
        """
        :param input_data: the filename of the config file to read
        :return a non empty string containing an error message on failure
        """
        try:
            f = open(input_data, "r")
            lines = f.readlines()

            if overwrite:
                self.sections = {}

            section_name = "default"
            settings = self.sections.get(section_name.lower(), Settings(section_name))
            self.sections[section_name] = settings
            for line in lines:
                section_name, keys, value, comment = self.line_parser.parse(line)
                if section_name != '':
                    settings = self.sections.get(section_name.lower(), Settings(section_name))
                    self.sections[section_name] = settings
                else:
                    if comment != '':
                        settings.append(comment, '', input_data)
                    for key in keys:
                        settings.append(key, value, input_data)

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
        return self.sections
