import os
import tempfile
import unittest
from collections import OrderedDict
import logging

from coalib.parsing.ConfParser import ConfParser
from coalib.settings.Section import Section


class ConfParserTest(unittest.TestCase):
    example_file = """setting = without_section
    [foo]
    to be ignored
    a_default, another = val
    TEST = tobeignored  # do you know that thats a comment
    test = push
    t =
    escaped_\\=equal = escaped_\\#hash
    escaped_\\\\backslash = escaped_\\ space
    escaped_\\,comma = escaped_\\.dot
    [MakeFiles]
     j  , another = a
                   multiline
                   value
    # just a comment
    # just a comment
    nokey. = value
    foo.test = content
    makefiles.lastone = val
    append += key

    [EMPTY_ELEM_STRIP]
    A = a, b, c
    B = a, ,, d
    C = ,,,

    [name]
    key1 = value1
    key2 = value1
    key1 = value2
    """

    def setUp(self):
        self.tempdir = tempfile.gettempdir()
        self.file = os.path.join(self.tempdir, '.coafile')
        self.nonexistentfile = os.path.join(self.tempdir, 'e81k7bd98t')
        with open(self.file, 'w') as file:
            file.write(self.example_file)

        self.uut = ConfParser()
        try:
            os.remove(self.nonexistentfile)
        except FileNotFoundError:
            pass

        logger = logging.getLogger()

        with self.assertLogs(logger, 'WARNING') as self.cm:
            self.sections = self.uut.parse(self.file)

    def tearDown(self):
        os.remove(self.file)

    def test_warning_typo(self):
        logger = logging.getLogger()
        with self.assertLogs(logger, 'WARNING') as cm:
            newConf = ConfParser(comment_seperators=('#',))
            self.assertEquals(cm.output[0], 'WARNING:root:The setting '
                              '`comment_seperators` is deprecated. '
                              'Please use `comment_separators` '
                              'instead.')

    def test_parse_nonexisting_file(self):
        self.assertRaises(FileNotFoundError,
                          self.uut.parse,
                          self.nonexistentfile)
        self.assertNotEqual(self.uut.parse(self.file, True), self.sections)

    def test_parse_nonexisting_section(self):
        self.assertRaises(IndexError,
                          self.uut.get_section,
                          'non-existent section')

    def test_parse_default_section_deprecated(self):
        default_should = OrderedDict([
            ('setting', 'without_section')])

        key, val = self.sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'default')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, default_should)

        self.assertRegex(self.cm.output[0],
                         'A setting does not have a section.')

    def test_parse_foo_section(self):
        foo_should = OrderedDict([
            ('a_default', 'val'),
            ('another', 'val'),
            ('comment0', '# do you know that thats a comment'),
            ('test', 'content'),
            ('t', ''),
            ('escaped_=equal', 'escaped_#hash'),
            ('escaped_\\backslash', 'escaped_ space'),
            ('escaped_,comma', 'escaped_.dot')])

        # Pop off the default section.
        self.sections.popitem(last=False)

        key, val = self.sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'foo')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, foo_should)

    def test_parse_makefiles_section(self):
        makefiles_should = OrderedDict([
            ('j', 'a\nmultiline\nvalue'),
            ('another', 'a\nmultiline\nvalue'),
            ('comment1', '# just a comment'),
            ('comment2', '# just a comment'),
            ('lastone', 'val'),
            ('append', 'key'),
            ('comment3', '')])

        # Pop off the default and foo section.
        self.sections.popitem(last=False)
        self.sections.popitem(last=False)

        key, val = self.sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'makefiles')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, makefiles_should)

        self.assertEqual(val['comment1'].key, 'comment1')

    def test_parse_empty_elem_strip_section(self):
        empty_elem_strip_should = OrderedDict([
            ('a', 'a, b, c'),
            ('b', 'a, ,, d'),
            ('c', ',,,'),
            ('comment4', '')])

        # Pop off the default, foo and makefiles section.
        self.sections.popitem(last=False)
        self.sections.popitem(last=False)
        self.sections.popitem(last=False)

        key, val = self.sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'empty_elem_strip')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, empty_elem_strip_should)

    def test_remove_empty_iter_elements(self):
        # Test with empty-elem stripping.
        uut = ConfParser(remove_empty_iter_elements=True)
        uut.parse(self.file)
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['A']),
                         ['a', 'b', 'c'])
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['B']),
                         ['a', 'd'])
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['C']),
                         [])

        # Test without stripping.
        uut = ConfParser(remove_empty_iter_elements=False)
        uut.parse(self.file)
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['A']),
                         ['a', 'b', 'c'])
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['B']),
                         ['a', '', '', 'd'])
        self.assertEqual(list(uut.get_section('EMPTY_ELEM_STRIP')['C']),
                         ['', '', '', ''])

    def test_config_directory(self):
        self.uut.parse(self.tempdir)

    def test_settings_override_warning(self):
        self.assertEqual(self.cm.output[1], 'WARNING:root:test setting has '
                                            'already been defined in section '
                                            'foo. The previous setting will '
                                            'be overridden.')
        self.assertEqual(self.cm.output[2], 'WARNING:root:key1 setting has '
                                            'already been defined in section '
                                            'name. The previous setting will '
                                            'be overridden.')


class ConfParserTestParselinesSections(unittest.TestCase):
    test_file = """
    [basic]

    ignore = aaa,bbb
    ignore += ccc
    ignore += ddd

    [check_inheritence]
    ignore += eee

    [with_unrelated_settings]
    ignore = aaa,bbb
    other = variable
    ignore += ccc

    [multiline]
    ignore = aaa,
             bbb
    other = variable
    ignore += ccc ,
    ddd

    [with_random_spaces]
    ignore =aaa ,
             bbb
    other = variable
    ignore +=                  ccc   ,
                 ddd

    [with_spaces]
    ignore = a  aa,
             bbb
    other = variable
    ignore += c c c ,dd d

    [without_+=]
    ignore = aaa
    ignore = bbb

    [incomplete_ignore]
    ignore = aaa
    ignore +=
    """

    def setUp(self):
        self.tempdir = tempfile.gettempdir()
        self.file = os.path.join(self.tempdir, '.coafile')
        with open(self.file, 'w') as file:
            file.write(self.test_file)
        self.uut = ConfParser()
        self.sections = self.uut.parse(self.file)

    def tearDown(self):
        os.remove(self.file)

    def test_multiple_ignore_in_single_settings(self):
        expected = ['aaa', 'bbb', 'ccc', 'ddd']
        setting = self.uut.sections['basic'].contents['ignore']
        # While parsing .coafile, `\n` is added as the string
        # seperator between multiple values of ignore but while
        # forming a list it is seperated by `,`.
        setting.value = setting._value.replace('\n', ',')
        setting_items = list(setting)
        self.assertEqual(expected, setting_items)

    def test_ignore_with_unrelated_settings(self):
        expected = ['aaa', 'bbb', 'ccc']
        setting = (
            self.uut.sections['with_unrelated_settings'].contents['ignore'])
        setting.value = setting._value.replace('\n', ',')
        setting_items = list(setting)
        self.assertEqual(expected, setting_items)

    def test_multiline_ignore(self):
        expected = ['aaa', 'bbb', 'ccc', 'ddd']
        setting = self.uut.sections['multiline'].contents['ignore']
        setting.value = setting._value.replace('\n', ',')
        setting_items = list(setting)
        self.assertEqual(expected, setting_items)

    def test_ignore_with_random_spaces(self):
        expected = ['aaa', 'bbb', 'ccc', 'ddd']
        setting = self.uut.sections['with_random_spaces'].contents['ignore']
        setting.value = setting._value.replace('\n', ',')
        setting_items = list(setting)
        self.assertEqual(expected, setting_items)

    def test_multiline_ignore_with_spaces_in_names(self):
        expected = ['a  aa', 'bbb', 'c c c', 'dd d']
        setting = self.uut.sections['with_spaces'].contents['ignore']
        setting.value = setting._value.replace('\n', ',')
        setting_items = list(setting)
        self.assertEqual(expected, setting_items)

    # FIXME
    def test_errored_ignore_multiple(self):
        # Expected: It should throw an error, the user should fix it
        current_output = ['aaa', 'bbb']
        setting = self.uut.sections['without_+='].contents['ignore']
        setting.value = setting._value.replace('\n', ',')
        setting_items = list(setting)
        print('setting_items: ', setting_items)
        self.assertEqual(current_output, setting_items)

    # FIXME
    def test_with_incomplete_ignore(self):
        # Expected: It should throw an error, the user should fix it
        current_output = []
        setting = self.uut.sections['incomplete_ignore'].contents['ignore']
        setting.value = setting._value.replace('\n', ',')
        setting_items = list(setting)
        self.assertEqual(current_output, setting_items)

    # FIXME
    def test_ignore_inheritence(self):
        # Expected: setting_items should be a list and
        # it should be equal to expected
        # expected = ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
        current_output = 'eee'
        setting = self.uut.sections['check_inheritence'].contents['ignore']
        setting.value = setting._value.replace('\n', ',')
        # setting_items = list(setting)
        self.assertEqual(current_output, setting._value)
