import logging
import os
import tempfile
import unittest
from collections import OrderedDict

from coalib.parsing.ConfParser import ConfParser
from coalib.parsing.TomlConfParser import TomlConfParser
from coalib.settings.Section import Section


class TomlConfParserTest(unittest.TestCase):
    example_file = """setting = 'without_section'
comment0 = 'Hello'
# hello
[all]
# Hello World
max_line_length = 80 #cadc
ignore = './vendor'
a = true #ccas

[EMPTY_ELEM_STRIP]
    A = ['a', 'b', 'c']
    B = ['a', '  ', '  ', 'd']
    C = ['','',
    '','']

[foo]
files = '**'
aspects = ['aspectname1', 'AspectName2']
aspectname1.aspect_taste = 80
aspectname1.subaspect_taste = ['word1', 'word2', 'word3']
aspectname1.subaspect_taste1 = 'word5'

[foo2]
inherits = 'foo'
aspects = 'aspectname3'
aspectname1.subaspect_taste1 = ['dog', 'cat']
appends = 'aspectname1.subaspect_taste1'
a.b.c = '10'

[sample]
    # coala
    [sample.item]
    # Hello World
    b = [ '1', #Hello
          '2'
        ]

    a = 10

[a]
p = '10'
q = '20'

[b]
c = '5'
d  = '6'

[c]
inherits = [ 'a', 'b' ]
p  = 'a'
d  = 'b'
appends.a = 'p'
appends.b = 'd'
"""

    incorrect_file = """
    a = b
    c = [1, 3
    """

    def setUp(self):
        self.tempdir = tempfile.gettempdir()
        self.file = os.path.join(self.tempdir, '.coafile.toml')
        self.nonexistentfile = os.path.join(self.tempdir, 'w31efr3rk')
        self.incorrect_file = os.path.join(self.tempdir, 'incorrect')
        with open(self.file, 'w') as file:
            file.write(self.example_file)

        with open(self.incorrect_file, 'w') as file:
            file.write(self.incorrect_file)

        self.uut = TomlConfParser()

        try:
            os.remove(self.nonexistentfile)
        except FileNotFoundError:
            pass

        self.logger = logging.getLogger()

        with self.assertLogs(self.logger, 'WARNING') as self.cm:
            self.sections = self.uut.parse(self.file)

    def tearDown(self):
        os.remove(self.file)

    def assert_values(self, val, should):
        self.assertTrue(isinstance(val, Section))

        is_dict = OrderedDict()

        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, should)

    def test_parse_nonexisting_file(self):
        self.assertRaises(FileNotFoundError,
                          self.uut.parse,
                          self.nonexistentfile)

    def test_parse_nonexistent_section(self):
        with self.assertRaises(SystemExit) as cm:
            self.uut.get_section('non-existent-section')
        self.assertNotEqual(self.uut.parse(self.file, True), self.sections)

    def test_parse_error(self):
        with self.assertRaises(SystemExit) as cm:
            self.uut.parse(self.incorrect_file)

    def test_format_value(self):
        self.assertEqual(self.uut.format_value(80), '80')
        self.assertEqual(self.uut.format_value(True), 'True')
        self.assertEqual(self.uut.format_value([1, 2, 3]), '1, 2, 3')

    def test_parse_default_section_deprecated(self):
        default_should = OrderedDict([
            ('setting', 'without_section'),
            ('comment0', 'Hello'),
            ('(comment0)', '# hello')
        ])

        self.assertTrue('default' in self.sections.keys())
        val = self.sections.pop('default')
        self.assert_values(val, default_should)

        self.assertRegex(self.cm.output[0],
                         'A setting does not have a section.')

    def test_parse_all(self):
        all_should = OrderedDict([
            ('(comment1)', '# Hello World'),
            ('max_line_length', '80'),
            ('ignore', './vendor'),
            ('a', 'true'),
            ('(comment2)', '')
        ])

        self.assertTrue('all' in self.sections.keys())
        val = self.sections.pop('all')
        self.assert_values(val, all_should)

    def test_parse_empty_elem_strip_section(self):
        empty_elem_strip_should = OrderedDict([
            ('a', 'a, b, c'),
            ('b', 'a,   ,   , d'),
            ('c', ', , ,'),
            ('(comment3)', '')
        ])

        self.assertTrue('empty_elem_strip' in self.sections.keys())
        val = self.sections.pop('empty_elem_strip')
        self.assert_values(val,
                           empty_elem_strip_should)

    def test_parse_aspects(self):
        aspects_should = OrderedDict([
            ('files', '**'),
            ('aspects', 'aspectname1, AspectName2'),
            ('aspectname1:aspect_taste', '80'),
            ('aspectname1:subaspect_taste', 'word1, word2, word3'),
            ('aspectname1:subaspect_taste1', 'word5'),
            ('(comment4)', '')
        ])

        self.assertTrue('foo' in self.sections.keys())
        val = self.sections.pop('foo')

        self.assert_values(val,
                           aspects_should)

    def test_inherited(self):
        inherited_should = OrderedDict([
            ('inherits', 'foo'),
            ('aspects', 'aspectname3'),
            ('aspectname1:subaspect_taste1', 'dog, cat'),
            ('appends', 'aspectname1.subaspect_taste1'),
            ('a:b:c', '10'),
            ('(comment5)', '')])

        self.assertTrue('foo.foo2' in self.sections.keys())
        val = self.sections.pop('foo.foo2')

        self.assert_values(val,
                           inherited_should)

    def test_remove_empty_iter_elements(self):

        # Test without stripping.
        uut = TomlConfParser(remove_empty_iter_elements=False)
        uut.parse(self.file)
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['A']),
                         ['a', 'b', 'c'])
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['B']),
                         ['a', '', '', 'd'])
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['C']),
                         ['', '', '', ''])

        # Test with empty-elem stripping.
        uut = TomlConfParser(remove_empty_iter_elements=True)
        uut.parse(self.file)
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['A']),
                         ['a', 'b', 'c'])
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['B']),
                         ['a', 'd'])
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['C']),
                         [])

    def test_nested_inheritance(self):

        inherit_should = OrderedDict([
            ('inherits', 'a, b'),
            ('p', 'a'),
            ('d', 'b'),
            ('appends:a', 'p'),
            ('appends:b', 'd')])

        # Test a.c
        self.assertTrue('a.c' in self.sections.keys())
        val = self.sections.pop('a.c')
        self.assert_values(val,
                           inherit_should)
        self.assertTrue(val.contents.get('p').to_append)
        self.assertFalse(val.contents.get('d').to_append)

        # Test b.c
        self.assertTrue('b.c' in self.sections.keys())
        val = self.sections.pop('b.c')
        self.assert_values(val,
                           inherit_should)
        self.assertTrue(val.contents.get('d').to_append)
        self.assertFalse(val.contents.get('p').to_append)

    def test_config_directory(self):
        self.uut.parse(self.tempdir)

    def test_consistency(self):

        coafile_str = '''
        [foo]
        files = **
        aspects = aspectname1, AspectName2
        aspectname1:aspect_taste = 80
        aspectname1:subaspect_taste = word1, word2, word3
        aspectname1:subaspect_taste1 = word5
        '''

        # Test that the sections generated in toml and coafile format
        # is same

        self.assertTrue('foo' in self.sections.keys())
        toml_dict = OrderedDict()
        val_toml = self.sections.pop('foo')
        key_toml = val_toml.name
        for k in val_toml:
            toml_dict[k] = str(val_toml[k])
        toml_dict.popitem()

        self.coafile = os.path.join(self.tempdir, '.coafile')
        with open(self.coafile, 'w') as file:
            file.write(coafile_str)
        sections_ini = ConfParser().parse(self.coafile)
        os.remove(self.coafile)

        sections_ini.popitem(last=False)
        key_ini, val_ini = sections_ini.popitem(last=False)
        ini_dict = OrderedDict()

        for k in val_ini:
            ini_dict[k] = str(val_ini[k])
        ini_dict.popitem()

        self.assertEqual(key_toml, key_ini)
        self.assertEqual(toml_dict, ini_dict)
