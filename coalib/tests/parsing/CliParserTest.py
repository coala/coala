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
import sys

sys.path.insert(0, ".")
from coalib.parsing.CliParser import CliParser
import unittest
import argparse


class CliParserTestCase(unittest.TestCase):
    def setUp(self):
        self.test_arg_parser = argparse.ArgumentParser()
        self.test_arg_parser.add_argument('-t', nargs='+', dest='test')
        self.uut = CliParser(self.test_arg_parser)

    def dict_from_sections(self, parsed_sections):
        parsed_dict = {}
        for section_name, section in parsed_sections.items():
            parsed_dict[section_name] = set([(key, str(value)) for key, value in section.contents.items()])
        return parsed_dict

    def test_raises(self):
        self.assertRaises(TypeError, CliParser, 5)
        self.assertRaises(SystemExit, self.uut.parse, ["-h"])
        self.assertRaises(SystemExit, self.uut.parse, ["--nonsense"])

    def test_parse(self):
        # regular parse
        parsed_sections = self.uut.parse(['-t', 'ignored1', 'ignored2',
                                          '-t', 'taken',
                                          'section1.key1,section2.key2=value1,value2', 'section2.key2=only_this_value',
                                          'invalid.=shouldnt_be_shown', '.=not_either',
                                          '.key=only_in_default',
                                          'default_key1,default_key2=single_value',
                                          'default_key3=first_value,second_value'])
        expected_dict = {'default': {("test", "taken"), ("key", "only_in_default"), ("default_key1", "single_value"),
                                     ("default_key2", "single_value"), ("default_key3", "first_value,second_value")},
                         'section1': {("key1", "value1,value2")},
                         'section2': {("key2", "only_this_value")}
                         }
        self.assertEqual(self.dict_from_sections(parsed_sections), expected_dict)
        self.assertEqual(self.dict_from_sections(self.uut.export_to_settings()), expected_dict)

        # additional parse
        add_parsed_sections = self.uut.parse(['additional.key=value'])
        add_expected_dict = {'default': {("test", "taken"),
                                         ("key", "only_in_default"),
                                         ("default_key1", "single_value"),
                                         ("default_key2", "single_value"),
                                         ("default_key3", "first_value,second_value")},
                             'section1': {("key1", "value1,value2")},
                             'section2': {("key2", "only_this_value")},
                             'additional': {("key", "value")}
                             }
        self.assertEqual(self.dict_from_sections(add_parsed_sections), add_expected_dict)

        # reparse
        new_parsed_sections = self.uut.reparse(['new_key=value'])
        new_expected_dict = {'default': {("new_key", "value")}}
        self.assertEqual(self.dict_from_sections(new_parsed_sections), new_expected_dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
