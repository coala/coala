import unittest
import argparse

from coalib.parsing.CliParsing import parse_cli


class CliParserTest(unittest.TestCase):

    def setUp(self):
        self.test_arg_parser = argparse.ArgumentParser()
        self.test_arg_parser.add_argument('-t', nargs='+', dest='test')
        self.test_arg_parser.add_argument('-S',
                                          '--settings',
                                          nargs='+',
                                          dest='settings')

    @staticmethod
    def dict_from_sections(parsed_sections):
        parsed_dict = {}
        for section_name, section in parsed_sections.items():
            parsed_dict[section_name] = (
                set([(key,
                      str(value)) for key, value in section.contents.items()]))
        return parsed_dict

    def test_parse_cli(self):
        # regular parse
        parsed_sections = parse_cli(
            ['-t', 'ignored1', 'ignored2',
             '-t', 'taken',
             '-S', 'section1.key1,section2.key2=value1,value2',
             'section2.key2=only_this_value',
             'SECTION2.key2a=k2a',
             'invalid.=shouldnt_be_shown',
             '.=not_either',
             '.key=only_in_default',
             'default_key1,default_key2=single_value',
             'default_key3=first_value,second_value'],
            arg_parser=self.test_arg_parser)
        expected_dict = {
            'default': {
                ("test", "taken"),
                ("key", "only_in_default"),
                ("default_key1", "single_value"),
                ("default_key2", "single_value"),
                ("default_key3", "first_value,second_value")},
            'section1': {
                ("key1", "value1,value2")},
            'section2': {
                ("key2", "only_this_value"),
                ("key2a", "k2a")}}
        self.assertEqual(parsed_sections["default"].name, "Default")
        self.assertEqual(self.dict_from_sections(parsed_sections),
                         expected_dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
