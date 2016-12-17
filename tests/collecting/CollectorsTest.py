import os
import pkg_resources
import unittest

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.bears.Bear import Bear
from coalib.collecting.Collectors import (
    collect_all_bears_from_sections, collect_bears, collect_dirs, collect_files,
    collect_registered_bears_dirs, filter_section_bears_by_languages,
    get_all_bears, get_all_bears_names)
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.ListLogPrinter import ListLogPrinter
from coalib.settings.Section import Section
from tests.TestUtilities import bear_test_module


class CollectFilesTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                'collectors_test_dir')
        self.log_printer = ListLogPrinter()

    def test_file_empty(self):
        self.assertRaises(TypeError, collect_files)

    def test_file_invalid(self):
        self.assertEqual(collect_files(['invalid_path'],
                                       self.log_printer), [])
        self.assertEqual([log.message for log in self.log_printer.logs],
                         ["No files matching 'invalid_path' were found."])

    def test_file_collection(self):
        self.assertEqual(collect_files([os.path.join(self.collectors_test_dir,
                                                     'others',
                                                     '*',
                                                     '*2.py')],
                                       self.log_printer),
                         [os.path.normcase(os.path.join(
                             self.collectors_test_dir,
                             'others',
                             'py_files',
                             'file2.py'))])

    def test_file_string_collection(self):
        self.assertEqual(collect_files(os.path.join(self.collectors_test_dir,
                                                    'others',
                                                    '*',
                                                    '*2.py'),
                                       self.log_printer),
                         [os.path.normcase(os.path.join(
                             self.collectors_test_dir,
                             'others',
                             'py_files',
                             'file2.py'))])

    def test_ignored(self):
        self.assertEqual(collect_files([os.path.join(self.collectors_test_dir,
                                                     'others',
                                                     '*',
                                                     '*2.py'),
                                        os.path.join(self.collectors_test_dir,
                                                     'others',
                                                     '*',
                                                     '*2.py')],
                                       self.log_printer,
                                       ignored_file_paths=[os.path.join(
                                           self.collectors_test_dir,
                                           'others',
                                           'py_files',
                                           'file2.py')]),
                         [])

    def test_limited(self):
        self.assertEqual(
            collect_files([os.path.join(self.collectors_test_dir,
                                        'others',
                                        '*',
                                        '*py')],
                          self.log_printer,
                          limit_file_paths=[os.path.join(
                                                self.collectors_test_dir,
                                                'others',
                                                '*',
                                                '*2.py')]),
            [os.path.normcase(os.path.join(self.collectors_test_dir,
                                           'others',
                                           'py_files',
                                           'file2.py'))])


class CollectDirsTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                'collectors_test_dir')

    def test_dir_empty(self):
        self.assertRaises(TypeError, collect_dirs)

    def test_dir_invalid(self):
        self.assertEqual(collect_dirs(['invalid_path']), [])

    def test_dir_collection(self):
        self.assertEqual(
            sorted(i for i in
                   collect_dirs([os.path.join(self.collectors_test_dir,
                                              '**')])
                   if '__pycache__' not in i),
            sorted([os.path.normcase(os.path.join(
                self.collectors_test_dir, 'bears')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'bears_local_global')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'others')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'others',
                                              'c_files')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'others',
                                              'py_files')),
                os.path.normcase(self.collectors_test_dir)]))

    def test_dir_string_collection(self):
        self.assertEqual(
            sorted(i for i in
                   collect_dirs(os.path.join(self.collectors_test_dir,
                                             '**'))
                   if '__pycache__' not in i),
            sorted([os.path.normcase(os.path.join(
                self.collectors_test_dir, 'bears')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'bears_local_global')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'others')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'others',
                                              'c_files')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'others',
                                              'py_files')),
                os.path.normcase(self.collectors_test_dir)]))

    def test_ignored(self):
        self.assertEqual(
            sorted(i for i in
                   collect_dirs([os.path.join(self.collectors_test_dir,
                                              '**')],
                                [os.path.normcase(os.path.join(
                                    self.collectors_test_dir,
                                    'others',
                                    'py_files'))])
                   if '__pycache__' not in i),

            sorted([os.path.normcase(os.path.join(
                self.collectors_test_dir, 'bears')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'bears_local_global')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'others')),
                os.path.normcase(os.path.join(self.collectors_test_dir,
                                              'others',
                                              'c_files')),
                os.path.normcase(self.collectors_test_dir)]))

    def test_collect_registered_bears_dirs(self):
        old_iter = pkg_resources.iter_entry_points

        def test_iter_entry_points(name):
            assert name == 'hello'

            class EntryPoint1:

                @staticmethod
                def load():
                    class PseudoPlugin:
                        __file__ = '/path1/file1'
                    return PseudoPlugin()

            class EntryPoint2:

                @staticmethod
                def load():
                    raise pkg_resources.DistributionNotFound

            return iter([EntryPoint1(), EntryPoint2()])

        pkg_resources.iter_entry_points = test_iter_entry_points
        output = sorted(collect_registered_bears_dirs('hello'))
        self.assertEqual(output, [os.path.abspath('/path1')])
        pkg_resources.iter_entry_points = old_iter


class CollectBearsTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                'collectors_test_dir')

        self.log_printer = ListLogPrinter()

    def test_bear_empty(self):
        self.assertRaises(TypeError, collect_bears)

    def test_bear_invalid(self):
        self.assertEqual(collect_bears(['invalid_paths'],
                                       ['invalid_name'],
                                       ['invalid kind'],
                                       self.log_printer), ([],))
        self.assertEqual([log.message for log in self.log_printer.logs],
                         ["No bears matching 'invalid_name' were found. Make "
                          'sure you have coala-bears installed or you have '
                          'typed the name correctly.'])

        self.assertEqual(collect_bears(['invalid_paths'],
                                       ['invalid_name'],
                                       ['invalid kind1', 'invalid kind2'],
                                       self.log_printer), ([], []))

    def test_simple_single(self):
        self.assertEqual(len(collect_bears(
            [os.path.join(self.collectors_test_dir, 'bears')],
            ['bear1'],
            ['kind'],
            self.log_printer)[0]), 1)

    def test_string_single(self):
        self.assertEqual(len(collect_bears(
            os.path.join(self.collectors_test_dir, 'bears'),
            ['bear1'],
            ['kind'],
            self.log_printer)[0]), 1)

    def test_reference_single(self):
        self.assertEqual(len(collect_bears(
            [os.path.join(self.collectors_test_dir, 'bears')],
            ['metabear'],
            ['kind'],
            self.log_printer)[0]), 1)

    def test_no_duplications(self):
        self.assertEqual(len(collect_bears(
            [os.path.join(self.collectors_test_dir, 'bears', '**')],
            ['*'],
            ['kind'],
            self.log_printer)[0]), 2)

    def test_wrong_kind(self):
        self.assertEqual(len(collect_bears(
            [os.path.join(self.collectors_test_dir, 'bears', '**')],
            ['*'],
            ['other_kind'],
            self.log_printer)[0]), 0)

    def test_all_bears_from_sections(self):
        test_section = Section('test_section')
        test_section.bear_dirs = lambda: os.path.join(self.collectors_test_dir,
                                                      'bears_local_global',
                                                      '**')
        local_bears, global_bears = collect_all_bears_from_sections(
            {'test_section': test_section},
            self.log_printer)

        self.assertEqual(len(local_bears['test_section']), 2)
        self.assertEqual(len(global_bears['test_section']), 2)


class CollectorsTests(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.collectors_test_dir = os.path.join(current_dir,
                                                'collectors_test_dir')
        self.log_printer = LogPrinter(ConsolePrinter())

    def test_filter_section_bears_by_languages(self):
        test_section = Section('test_section')
        test_section.bear_dirs = lambda: os.path.join(self.collectors_test_dir,
                                                      'bears_local_global',
                                                      '**')
        local_bears, global_bears = collect_all_bears_from_sections(
            {'test_section': test_section},
            self.log_printer)
        local_bears = filter_section_bears_by_languages(local_bears, ['C'])
        self.assertEqual(len(local_bears['test_section']), 1)
        self.assertEqual(str(local_bears['test_section'][0]),
                         "<class 'bears2.Test2LocalBear'>")

        global_bears = filter_section_bears_by_languages(global_bears, ['Java'])
        self.assertEqual(len(global_bears['test_section']), 1)
        self.assertEqual(str(global_bears['test_section'][0]),
                         "<class 'bears1.Test1GlobalBear'>")

    def test_get_all_bears(self):
        with bear_test_module():
            bears = get_all_bears()
            assert isinstance(bears, list)
            for bear in bears:
                assert issubclass(bear, Bear)
            self.assertSetEqual(
                {b.name for b in bears},
                {'DependentBear',
                 'EchoBear',
                 'LineCountTestBear',
                 'JavaTestBear',
                 'SpaceConsistencyTestBear',
                 'TestBear'})

    def test_get_all_bears_names(self):
        with bear_test_module():
            names = get_all_bears_names()
            assert isinstance(names, list)
            self.assertSetEqual(
                set(names),
                {'DependentBear',
                 'EchoBear',
                 'LineCountTestBear',
                 'JavaTestBear',
                 'SpaceConsistencyTestBear',
                 'TestBear'})
