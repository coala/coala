import unittest
import os

from coalib.misc import Constants
from coalib.settings.Section import Section, Setting, append_to_sections
from coalib.settings.ConfigurationGathering import get_config_directory
from coalib.parsing.Globbing import glob_escape


class SectionTest(unittest.TestCase):

    def test_construction(self):
        uut = Section(Constants.COMPLEX_TEST_STRING, None)
        uut = Section(Constants.COMPLEX_TEST_STRING, uut)
        self.assertRaises(TypeError, Section, 'irrelevant', 5)
        self.assertRaises(ValueError, uut.__init__, 'name', uut)

    def test_append(self):
        uut = Section(Constants.COMPLEX_TEST_STRING, None)
        self.assertRaises(TypeError, uut.append, 5)
        uut.append(Setting(5, 5, 5))
        self.assertEqual(str(uut.get('5 ')), '5')
        self.assertEqual(int(uut.get('nonexistent', 5)), 5)

    def test_enabled(self):
        uut = Section('name')
        self.assertTrue(uut.is_enabled([]))
        self.assertTrue(uut.is_enabled(['name', 'wrongname']))
        self.assertFalse(uut.is_enabled(['wrongname']))

        uut.append(Setting('enabled', 'false'))
        self.assertFalse(uut.is_enabled([]))
        self.assertFalse(uut.is_enabled(['wrong_name']))
        self.assertTrue(uut.is_enabled(['name', 'wrongname']))

    def test_iter(self):
        defaults = Section('default', None)
        uut = Section('name', defaults)
        uut.append(Setting(5, 5, 5))
        uut.add_or_create_setting(Setting('TEsT', 4, 5))
        defaults.append(Setting('tEsT', 1, 3))
        defaults.append(Setting(' great   ', 3, 8))
        defaults.append(Setting(' great   ', 3, 8), custom_key='custom')
        uut.add_or_create_setting(Setting('custom', 4, 8, to_append=True))
        uut.add_or_create_setting(Setting(' NEW   ', 'val', 8))
        uut.add_or_create_setting(Setting(' NEW   ', 'vl', 8),
                                  allow_appending=False)
        uut.add_or_create_setting(Setting('new', 'val', 9),
                                  custom_key='teSt ',
                                  allow_appending=True)
        self.assertEqual(list(uut), ['5', 'test', 'custom', 'new', 'great'])

        for index in uut:
            t = uut[index]
            self.assertNotEqual(t, None)

        self.assertIn('teST', defaults)
        self.assertIn('       GREAT', defaults)
        self.assertNotIn('       GrEAT !', defaults)
        self.assertNotIn('', defaults)
        self.assertEqual(str(uut['test']), '4\nval')
        self.assertEqual(str(uut['custom']), '3, 4')
        self.assertEqual(int(uut['GREAT ']), 3)
        self.assertRaises(IndexError, uut.__getitem__, 'doesnotexist')
        self.assertRaises(IndexError, uut.__getitem__, 'great', True)
        self.assertRaises(IndexError, uut.__getitem__, ' ')

    def test_setitem(self):
        uut = Section('section', None)
        uut['key1'] = 'value1'
        self.assertEqual(str(uut), "section {key1 : 'value1'}")
        uut['key1'] = 'changed_value1'
        self.assertEqual(str(uut), "section {key1 : 'changed_value1'}")
        uut['key1'] = Setting('any key', 'value1')
        self.assertEqual(str(uut), "section {key1 : 'value1'}")

    def test_string_conversion(self):
        uut = Section('name')
        self.assertEqual(str(uut), 'name {}')
        uut.append(Setting('key', 'value'))
        self.assertEqual(str(uut), "name {key : 'value'}")
        uut.append(Setting('another_key', 'another_value'))
        self.assertEqual(str(uut),
                         "name {key : 'value', another_key : 'another_value'}")

    def test_copy(self):
        uut = Section('name')
        uut.append(Setting('key', 'value'))
        self.assertEqual(str(uut['key']), 'value')
        copy = uut.copy()
        self.assertEqual(str(copy), str(uut))
        uut.append(Setting('key', 'another_value'))
        self.assertNotEqual(str(copy), str(uut))

        uut.defaults = copy
        copy = uut.copy()
        self.assertEqual(str(uut.defaults), str(copy.defaults))
        uut.defaults.append(Setting('key', 'quite_something_else'))
        self.assertNotEqual(str(uut.defaults), str(copy.defaults))

    def test_update(self):
        cli = Section('cli', None)
        conf = Section('conf', None)

        self.assertRaises(TypeError, cli.update, 4)

        cli.append(Setting('key1', 'value11'))
        cli.append(Setting('key2', 'value12'))
        conf.append(Setting('key1', 'value21'))
        conf.append(Setting('key3', 'value23'))

        # Values are overwritten, new keys appended
        self.assertEqual(str(conf.copy().update(cli)),
                         "conf {key1 : 'value11', key3 : 'value23', "
                         "key2 : 'value12'}")

        cli.defaults = Section('clidef', None)
        cli.defaults.append(Setting('def1', 'dval1'))

        self.assertEqual(str(conf.copy().update(cli).defaults),
                         "clidef {def1 : 'dval1'}")

        conf.defaults = Section('confdef', None)
        conf.defaults.append(Setting('def2', 'dval2'))

        self.assertEqual(str(conf.copy().update(cli).defaults),
                         "confdef {def2 : 'dval2', def1 : 'dval1'}")

    def test_append_to_sections(self):
        sections = {}

        append_to_sections(sections, '', '', '')
        self.assertEqual(sections, {})

        append_to_sections(sections, 'key', None, '')
        self.assertEqual(sections, {})

        append_to_sections(sections, 'test', 'val', 'origin')
        self.assertIn('default', sections)
        self.assertEqual(len(sections), 1)
        self.assertEqual(len(sections['default'].contents), 1)

    def test_update_setting(self):
        section = Section('section', None)

        section.append(Setting('key1', 'value11'))
        section.append(Setting('key2', 'value12'))

        section.update_setting('key1', new_value='value13')
        self.assertEqual(str(section),
                         "section {key1 : 'value13', key2 : 'value12'}")
        section.update_setting('key1', 'key3')
        self.assertEqual(str(section),
                         "section {key3 : 'value13', key2 : 'value12'}")
        section.update_setting('key3', 'key4', 'value14')
        self.assertEqual(str(section),
                         "section {key4 : 'value14', key2 : 'value12'}")

    def test_delete_setting(self):
        section = Section('section', None)

        section.append(Setting('key1', 'value11'))
        section.append(Setting('key2', 'value12'))

        section.delete_setting('key1')
        self.assertEqual(str(section),
                         "section {key2 : 'value12'}")

        section.append(Setting('key3', 'value13'))
        section.append(Setting('key4', 'value14'))

        section.delete_setting('key3')
        self.assertEqual(str(section),
                         "section {key2 : 'value12', key4 : 'value14'}")

    def test_bear_dirs(self):
        section = Section('section', None)
        empty_bear_dirs_len = len(section.bear_dirs())
        section.append(Setting('bear_dirs', 'test1, test2 (1)'))
        self.assertEqual(len(section.bear_dirs()), empty_bear_dirs_len + 2)
        # Verify if bear directories are properly escaped
        root = get_config_directory(section)
        path = os.path.join(glob_escape(root), glob_escape('test2 (1)'), '**')
        self.assertIn(path, section.bear_dirs())

    def test_set_default_section(self):
        section = Section('section')

        section.set_default_section({})
        self.assertIsNone(section.defaults)

        sections = {'cli': Section('cli')}
        section.set_default_section(sections)
        self.assertEqual(section.defaults, sections['cli'])

        sections = {'all': Section('all'), 'all.python': Section('all.python')}
        sections['all.python'].set_default_section(sections)
        self.assertEqual(sections['all.python'].defaults, sections['all'])
        sections['all.python.codestyle'] = Section('all.python.codestyle')
        sections['all.python.codestyle'].set_default_section(sections)
        self.assertEqual(sections['all.python.codestyle'].defaults,
                         sections['all.python'])
        sections['all.c.codestyle'] = Section('all.c.codestyle')
        sections['all.c.codestyle'].set_default_section(sections)
        self.assertEqual(sections['all.c.codestyle'].defaults,
                         sections['all'])
