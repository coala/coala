import os
import re
import tempfile
import unittest
import logging
import sys

from pyprint.ClosableObject import close_objects
import pytest

from coalib.misc import Constants
from coalib.settings.Section import Section
from coala_utils.ContextManagers import (
    make_temp, change_directory, retrieve_stdout)
from coala_utils.string_processing import escape
from coalib.settings.ConfigurationGathering import (
    aspectize_sections,
    find_user_config,
    gather_configuration,
    get_filtered_bears,
    load_configuration,
)

from tests.TestUtilities import bear_test_module, TEST_BEARS_COUNT


@pytest.mark.usefixtures('disable_bears')
class ConfigurationGatheringTest(unittest.TestCase):

    def setUp(self):
        # Needed so coala doesn't error out
        self.min_args = ['-f', '*.java', '-b', 'JavaTestBear']

    def tearDown(self):
        close_objects()

    def test_gather_configuration(self):
        def args(): return True

        # Using incomplete settings (e.g. an invalid coafile) will error
        with self.assertRaises(SystemExit):
            gather_configuration(args,
                                 arg_list=['-c abcdefghi/invalid/.coafile'])

        # Using a bad filename explicitly exits coala.
        with self.assertRaises(SystemExit):
            gather_configuration(
                args,
                arg_list=['-S', 'test=5', '-c', 'some_bad_filename'])

        with make_temp() as temporary:
            sections, local_bears, global_bears, targets = (
                gather_configuration(
                    args,
                    arg_list=['-S', 'test=5', '-c', escape(temporary, '\\'),
                              '-s'] + self.min_args))

        self.assertEqual(
            str(sections['cli']),
            "cli {bears : 'JavaTestBear', config : " + repr(temporary) +
            ", files : '*.java', save : 'True', test : '5'}")

        with make_temp() as temporary:
            sections, local_bears, global_bears, targets = (
                gather_configuration(args,
                                     arg_list=['-S test=5',
                                               '-f *.java',
                                               '-c ' + escape(temporary, '\\'),
                                               '-b LineCountBear -s']))

        self.assertEqual(len(local_bears['cli']), 0)

    def test_default_coafile_parsing(self):
        tmp = Constants.system_coafile

        Constants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'section_manager_test_files',
            'default_coafile'))

        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            arg_list=[])

        self.assertEqual(str(sections['test']),
                         "test {value : '1', testval : '5'}")

        Constants.system_coafile = tmp

    def test_user_coafile_parsing(self):
        tmp = Constants.user_coafile

        Constants.user_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'section_manager_test_files',
            'default_coafile'))

        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            arg_list=[])

        self.assertEqual(str(sections['test']),
                         "test {value : '1', testval : '5'}")

        Constants.user_coafile = tmp

    def test_nonexistent_file(self):
        filename = 'bad.one/test\neven with bad chars in it'
        with self.assertRaises(SystemExit):
            gather_configuration(lambda *args: True,
                                 arg_list=['-S', 'config=' + filename])

        tmp = Constants.system_coafile
        Constants.system_coafile = filename

        with self.assertRaises(SystemExit):
            gather_configuration(lambda *args: True,
                                 arg_list=[])

        Constants.system_coafile = tmp

    def test_merge(self):
        tmp = Constants.system_coafile
        Constants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'section_manager_test_files',
            'default_coafile'))

        config = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'section_manager_test_files',
            '.coafile'))

        # Check merging of default_coafile and .coafile
        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            arg_list=['-c', re.escape(config)])

        self.assertEqual(str(sections['test']),
                         "test {value : '2'}")
        self.assertEqual(str(sections['test-2']),
                         "test-2 {files : '.', bears : 'LineCountBear'}")

        # Check merging of default_coafile, .coafile and cli
        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            arg_list=['-c',
                      re.escape(config),
                      '-S',
                      'test.value=3',
                      'test-2.bears=',
                      'test-5.bears=TestBear2'])

        self.assertEqual(str(sections['test']), "test {value : '3'}")
        self.assertEqual(str(sections['test-2']),
                         "test-2 {files : '.', bears : ''}")
        self.assertEqual(str(sections['test-3']),
                         "test-3 {files : 'MakeFile'}")
        self.assertEqual(str(sections['test-4']),
                         "test-4 {bears : 'TestBear'}")
        self.assertEqual(str(sections['test-5']),
                         "test-5 {bears : 'TestBear2'}")

        Constants.system_coafile = tmp

    def test_merge_defaults(self):
        with make_temp() as temporary:
            sections, local_bears, global_bears, targets = (
                gather_configuration(lambda *args: True,
                                     arg_list=['-S', 'value=1', 'test.value=2',
                                               '-c', escape(temporary, '\\')] +
                                     self.min_args))

        self.assertEqual(sections['cli'],
                         sections['test'].defaults)

    def test_back_saving(self):
        filename = os.path.join(tempfile.gettempdir(),
                                'SectionManagerTestFile')

        # We need to use a bad filename or this will parse coalas .coafile
        # Despite missing settings (coala isn't run) the file is saved
        with self.assertRaises(SystemExit):
            gather_configuration(
                lambda *args: True,
                arg_list=['-S',
                          'save=' + escape(filename, '\\'),
                          '-c=some_bad_filename'])

        with open(filename, 'r') as f:
            lines = f.readlines()
        self.assertEqual(['[cli]\n',
                          'config = some_bad_filename\n'], lines)

        with self.assertRaises(SystemExit):
            gather_configuration(
                lambda *args: True,
                arg_list=['-S',
                          'save=true',
                          'config=' + escape(filename, '\\'),
                          'test.value=5'])

        with open(filename, 'r') as f:
            lines = f.readlines()
        os.remove(filename)
        if os.path.sep == '\\':
            filename = escape(filename, '\\')
        self.assertEqual(['[cli]\n',
                          'config = ' + filename + '\n',
                          '[test]\n',
                          'value = 5\n'], lines)

    def test_targets(self):
        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            arg_list=['cli', 'test1', 'test2'])

        self.assertEqual(targets, ['cli', 'test1', 'test2'])

    def test_find_user_config(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        c_file = os.path.join(current_dir,
                              'section_manager_test_files',
                              'project',
                              'test.c')

        retval = find_user_config(c_file, 1)
        self.assertEqual('', retval)

        retval = find_user_config(c_file, 2)
        self.assertEqual(os.path.join(current_dir,
                                      'section_manager_test_files',
                                      '.coafile'), retval)

        child_dir = os.path.join(current_dir,
                                 'section_manager_test_files',
                                 'child_dir')
        retval = find_user_config(child_dir, 2)
        self.assertEqual(os.path.join(current_dir,
                                      'section_manager_test_files',
                                      'child_dir',
                                      '.coafile'), retval)

        with change_directory(child_dir):
            sections, _, _, _ = gather_configuration(
                lambda *args: True,
                arg_list=['--find-config'])
            self.assertEqual(bool(sections['cli']['find_config']), True)

    def test_no_config(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        child_dir = os.path.join(current_dir,
                                 'section_manager_test_files',
                                 'child_dir')
        with change_directory(child_dir):
            sections, targets = load_configuration([])
            self.assertIn('value', sections['cli'])

            sections, targets = load_configuration(
                ['--no-config'])
            self.assertNotIn('value', sections['cli'])

            sections, targets = load_configuration(
                ['--no-config', '-S', 'use_spaces=True'])
            self.assertIn('use_spaces', sections['cli'])
            self.assertNotIn('values', sections['cli'])

            with self.assertRaises(SystemExit) as cm:
                sections, target = load_configuration(
                    ['--no-config', '--save'])
                self.assertEqual(cm.exception.code, 2)

            with self.assertRaises(SystemExit) as cm:
                sections, target = load_configuration(
                    ['--no-config', '--find-config'])
                self.assertEqual(cm.exception.code, 2)

    def test_section_inheritance(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        test_dir = os.path.join(current_dir, 'section_manager_test_files')
        logger = logging.getLogger()

        with change_directory(test_dir), \
                self.assertLogs(logger, 'WARNING') as cm:
            sections, _, _, _ = gather_configuration(
                lambda *args: True,
                arg_list=['-c', 'inherit_coafile'])
            self.assertEqual(sections['all.python'].defaults, sections['all'])
            self.assertEqual(sections['all.c']['key'],
                             sections['cli']['key'])
            self.assertEqual(sections['java.test'].defaults,
                             sections['cli'])
            self.assertEqual(int(sections['all.python']['max_line_length']),
                             80)
            self.assertEqual(sections['all.python.codestyle'].defaults,
                             sections['all.python'])
            self.assertEqual(sections['all.java.codestyle'].defaults,
                             sections['all'])
            self.assertEqual(str(sections['all']['ignore']),
                             './vendor')
            sections['cli']['ignore'] = './user'
            self.assertEqual(str(sections['all']['ignore']),
                             './user, ./vendor')
            sections['cli']['ignore'] = './client'
            self.assertEqual(str(sections['all']['ignore']),
                             './client, ./vendor')
        self.assertRegex(cm.output[0],
                         '\'cli\' is an internally reserved section name.')

    def test_default_section_deprecation_warning(self):
        logger = logging.getLogger()

        with self.assertLogs(logger, 'WARNING') as cm:
            # This gathers the configuration from the '.coafile' of this repo.
            gather_configuration(lambda *args: True,
                                 arg_list=[])

        self.assertIn('WARNING', cm.output[0])

        with retrieve_stdout() as stdout:
            load_configuration(['--no-config'])
            self.assertNotIn('WARNING', stdout.getvalue())

    def test_aspectize_sections(self):
        section = Section('test')
        sections = {'test': section}
        aspectize_sections(sections)

        self.assertIsNone(sections['test'].aspects)


class ConfigurationGatheringCollectionTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        close_objects()
        sys.argv = self.old_argv

    def test_get_filtered_bears(self):
        sys.argv = ['coala', '-I']

        with bear_test_module():
            local_bears, global_bears = get_filtered_bears(None)

        self.assertEqual(len(local_bears['cli']), TEST_BEARS_COUNT)

        with bear_test_module():
            local_bears, global_bears = get_filtered_bears(['Java'])

        self.assertEqual(len(local_bears['cli']), 2)
        self.assertEqual(str(local_bears['cli'][0]),
                         "<class 'JavaTestBear.JavaTestBear'>")
        self.assertEqual(str(local_bears['cli'][1]),
                         "<class 'LineCountTestBear.LineCountTestBear'>")
        self.assertEqual(len(global_bears['cli']), 0)
