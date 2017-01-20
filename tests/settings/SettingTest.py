import os
import re
import unittest
from collections import OrderedDict

from coalib.settings.Setting import (
    Setting, path, path_list, url, typed_dict, typed_list, typed_ordered_dict,
    glob, glob_list)
from coalib.parsing.Globbing import glob_escape


class SettingTest(unittest.TestCase):

    def test_construction(self):
        self.assertRaises(ValueError, Setting, '', 2, 2)
        self.assertRaises(TypeError, Setting, '', '', '', from_cli=5)
        self.assertRaisesRegex(TypeError, 'to_append',
                               Setting, '', '', '', to_append=10)

    def test_path(self):
        self.uut = Setting(
            'key', ' 22\n', '.' + os.path.sep, strip_whitespaces=True)
        self.assertEqual(path(self.uut),
                         os.path.abspath(os.path.join('.', '22')))

        abspath = os.path.abspath('.')
        self.uut = Setting('key', re.escape(abspath))
        self.assertEqual(path(self.uut), abspath)

        self.uut = Setting('key', ' 22', '')
        self.assertRaises(ValueError, path, self.uut)
        self.assertEqual(path(self.uut,
                              origin='test' + os.path.sep),
                         os.path.abspath(os.path.join('test', '22')))

    def test_glob(self):
        self.uut = Setting('key', '.',
                           origin=os.path.join('test (1)', 'somefile'))
        self.assertEqual(glob(self.uut),
                         glob_escape(os.path.abspath('test (1)')))

    def test_path_list(self):
        abspath = os.path.abspath('.')
        # Need to escape backslashes since we use list conversion
        self.uut = Setting('key', '., ' + abspath.replace('\\', '\\\\'),
                           origin=os.path.join('test', 'somefile'))
        self.assertEqual(path_list(self.uut),
                         [os.path.abspath(os.path.join('test', '.')), abspath])

    def test_url(self):
        uut = Setting('key', 'http://google.com')
        self.assertEqual(url(uut), 'http://google.com')

        with self.assertRaises(ValueError):
            uut = Setting('key', 'abc')
            url(uut)

    def test_glob_list(self):
        abspath = glob_escape(os.path.abspath('.'))
        # Need to escape backslashes since we use list conversion
        self.uut = Setting('key', '., ' + abspath.replace('\\', '\\\\'),
                           origin=os.path.join('test (1)', 'somefile'))
        self.assertEqual(
            glob_list(self.uut),
            [glob_escape(os.path.abspath(os.path.join('test (1)', '.'))),
             abspath])

    def test_typed_list(self):
        self.uut = Setting('key', '1, 2, 3')
        self.assertEqual(typed_list(int)(self.uut),
                         [1, 2, 3])

        with self.assertRaises(ValueError):
            self.uut = Setting('key', '1, a, 3')
            typed_list(int)(self.uut)

    def test_typed_dict(self):
        self.uut = Setting('key', '1, 2: t, 3')
        self.assertEqual(typed_dict(int, str, None)(self.uut),
                         {1: None, 2: 't', 3: None})

        with self.assertRaises(ValueError):
            self.uut = Setting('key', '1, a, 3')
            typed_dict(int, str, '')(self.uut)

    def test_typed_ordered_dict(self):
        self.uut = Setting('key', '1, 2: t, 3')
        self.assertEqual(typed_ordered_dict(int, str, None)(self.uut),
                         OrderedDict([(1, None), (2, 't'), (3, None)]))

        with self.assertRaises(ValueError):
            self.uut = Setting('key', '1, a, 3')
            typed_ordered_dict(int, str, '')(self.uut)

    def test_inherited_conversions(self):
        self.uut = Setting('key', ' 22\n', '.', strip_whitespaces=True)
        self.assertEqual(str(self.uut), '22')
        self.assertEqual(int(self.uut), 22)
        self.assertRaises(ValueError, bool, self.uut)

    def test_value_getter(self):
        with self.assertRaisesRegex(ValueError, 'This property is invalid'):
            self.uut = Setting('key', '22\n', '.', to_append=True)
            self.uut.value

        with self.assertRaisesRegex(ValueError,
                                    'Iteration on this object is invalid'):
            self.uut = Setting('key', '1, 2, 3', '.', to_append=True)
            list(self.uut)
