import os
import tempfile
import unittest
import logging
import sys

from pyprint.ClosableObject import close_objects
from pyprint.NullPrinter import NullPrinter
import pytest

from coalib.bearlib.aspects.Metadata import CommitMessage
from coalib.bearlib.languages import Language
from coalib.misc import Constants
from coalib.parsing.DefaultArgParser import PathArg
from coalib.settings.Section import Section
from coala_utils.ContextManagers import (
    make_temp, change_directory, retrieve_stdout)
from coalib.output.printers.LogPrinter import LogPrinter
from coala_utils.string_processing import escape
from coalib.settings.ConfigurationGathering import (
    aspectize_sections,
    validate_aspect_config,
    _set_section_language,
    find_user_config,
    gather_configuration,
    get_filtered_bears,
    load_configuration,
)
from coalib.settings.Setting import Setting
from coalib.misc.Constants import get_system_coafile

from tests.TestUtilities import (
    bear_test_module,
    TEST_BEARS_COUNT,
    TEST_BEAR_NAMES,
)
from testfixtures import log_capture


@pytest.mark.usefixtures('disable_bears')
class ConfigurationGatheringTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = LogPrinter(NullPrinter())

        # Needed so coala doesn't error out
        self.min_args = ['-f', '*.java', '-b', 'JavaTestBear']

    def tearDown(self):
        close_objects(self.log_printer)

    def test_gather_configuration(self):
        args = (lambda *args: True, self.log_printer)

        # Using incomplete settings (e.g. an invalid coafile) will error
        with self.assertRaises(SystemExit):
            gather_configuration(*args,
                                 arg_list=['-c abcdefghi/invalid/.coafile'])

        # Using a bad filename explicitly exits coala.
        with self.assertRaises(SystemExit):
            gather_configuration(
                *args,
                arg_list=['-S', 'test=5', '-c', 'some_bad_filename'])

        with make_temp() as temporary:
            sections, local_bears, global_bears, targets = (
                gather_configuration(
                    *args,
                    arg_list=['-S', 'test=5', '-c', temporary,
                              '-s'] + self.min_args))

        self.assertEqual(
            str(sections['cli']),
            "cli {bears : 'JavaTestBear', config : " +
            repr(PathArg(temporary)) +
            ", files : '*.java', save : 'True', test : '5'}")

        with make_temp() as temporary:
            sections, local_bears, global_bears, targets = (
                gather_configuration(*args,
                                     arg_list=['-S test=5',
                                               '-f *.java',
                                               '-c ' + (temporary),
                                               '-b LineCountBear -s']))

        self.assertEqual(len(local_bears['cli']), 0)

    @log_capture()
    def test_default_coafile_deprecation(self, capture):
        system_coafile_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'section_manager_test_files',
            'child_dir'))

        get_system_coafile(system_coafile_path)

        capture.check(
            ('root', 'WARNING', 'Filename deafult_coafile has been deprecated. '
             'Please use system_coafile instead.')
        )

    def test_system_coafile_parsing(self):
        tmp = Constants.system_coafile

        Constants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'section_manager_test_files',
            'system_coafile'))

        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=[])

        self.assertEqual(str(sections['test']),
                         "test {value : '1', testval : '5'}")

        Constants.system_coafile = tmp

    def test_user_coafile_parsing(self):
        tmp = Constants.user_coafile

        Constants.user_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'section_manager_test_files',
            'system_coafile'))

        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=[])

        self.assertEqual(str(sections['test']),
                         "test {value : '1', testval : '5'}")

        Constants.user_coafile = tmp

    def test_nonexistent_file(self):
        filename = 'bad.one/test\neven with bad chars in it'
        with self.assertRaises(SystemExit):
            gather_configuration(lambda *args: True,
                                 self.log_printer,
                                 arg_list=['-S', 'config=' + filename])

        tmp = Constants.system_coafile
        Constants.system_coafile = filename

        with self.assertRaises(SystemExit):
            gather_configuration(lambda *args: True,
                                 self.log_printer,
                                 arg_list=[])

        Constants.system_coafile = tmp

    def test_merge(self):
        tmp = Constants.system_coafile
        Constants.system_coafile = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'section_manager_test_files',
            'system_coafile'))

        config = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'section_manager_test_files',
            '.coafile'))

        # Check merging of system_coafile and .coafile
        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=['-c', config])

        self.assertEqual(str(sections['test']),
                         "test {value : '2'}")
        self.assertEqual(str(sections['test-2']),
                         "test-2 {files : '.', bears : 'LineCountBear'}")

        # Check merging of system_coafile, .coafile and cli
        sections, local_bears, global_bears, targets = gather_configuration(
            lambda *args: True,
            self.log_printer,
            arg_list=['-c',
                      config,
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
                                     self.log_printer,
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
                self.log_printer,
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
                self.log_printer,
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
            self.log_printer,
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
                self.log_printer,
                arg_list=['--find-config'])
            self.assertEqual(bool(sections['cli']['find_config']), True)

    def test_no_config(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        child_dir = os.path.join(current_dir,
                                 'section_manager_test_files',
                                 'child_dir')
        with change_directory(child_dir):
            sections, targets = load_configuration([], self.log_printer)
            self.assertIn('value', sections['cli'])

            sections, targets = load_configuration(
                ['--no-config'],
                self.log_printer)
            self.assertNotIn('value', sections['cli'])

            sections, targets = load_configuration(
                ['--no-config', '-S', 'use_spaces=True'],
                self.log_printer)
            self.assertIn('use_spaces', sections['cli'])
            self.assertNotIn('values', sections['cli'])

            with self.assertRaises(SystemExit) as cm:
                sections, target = load_configuration(
                    ['--no-config', '--save'],
                    self.log_printer)
                self.assertEqual(cm.exception.code, 2)

            with self.assertRaises(SystemExit) as cm:
                sections, target = load_configuration(
                    ['--no-config', '--find-config'],
                    self.log_printer)
                self.assertEqual(cm.exception.code, 2)

    def test_section_inheritance(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        test_dir = os.path.join(current_dir, 'section_manager_test_files')
        logger = logging.getLogger()

        with change_directory(test_dir), \
                self.assertLogs(logger, 'WARNING') as cm:
            sections, _, _, _ = gather_configuration(
                lambda *args: True,
                self.log_printer,
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
                                 self.log_printer,
                                 arg_list=[])

        self.assertIn('WARNING', cm.output[0])

        with retrieve_stdout() as stdout:
            load_configuration(['--no-config'], self.log_printer)
            self.assertNotIn('WARNING', stdout.getvalue())


class AspectConfigurationTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('aspect section')
        self.section.append(Setting('aspects', 'commitmessage'))
        self.section.language = Language['python']
        self.sections = {'aspect section': self.section}

    def test_aspectize_sections(self):
        no_aspect_section = Section('no aspect')
        self.sections['no aspect'] = no_aspect_section
        aspectize_sections(self.sections)
        self.assertTrue(validate_aspect_config(self.section))
        self.assertEqual(self.section.aspects[0], CommitMessage('py'))
        self.assertIsNone(no_aspect_section.aspects)

    def test_validate_aspect_config_no_aspects(self):
        self.section['aspects'] = ''
        self.assertFalse(validate_aspect_config(self.section))

    def test_validate_aspect_config_have_bears(self):
        self.section['bears'] = 'TestBear'

        logger = logging.getLogger()
        with self.assertLogs(logger, 'WARNING') as cm:
            self.assertTrue(validate_aspect_config(self.section))
            self.assertRegex(
                cm.output[0],
                '`aspects` and `bears` setting is detected '
                'in section `aspect section`. Aspect-based configuration will '
                'takes priority and will overwrite any '
                'explicitly listed bears.')

    def test_validate_aspect_no_language(self):
        self.section.language = None

        logger = logging.getLogger()
        with self.assertLogs(logger, 'WARNING') as cm:
            self.assertFalse(validate_aspect_config(self.section))
            self.assertRegex(
                cm.output[0],
                'Setting `language` is not found in section `aspect section`. '
                'Usage of aspect-based setting must include '
                'language information.')


class ValidateAndInjectLanguageTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('language section')
        self.section.append(Setting('language', 'python'))
        self.sections = {'language section': self.section}
        self.language = Language['python']

    def test__set_section_language(self):
        _set_section_language(self.sections)
        self.assertIsInstance(self.section.language, Language)
        self.assertEqual(str(self.language), str(self.section.language))

    def test__set_section_language_no_language(self):
        self.section['language'] = ''
        _set_section_language(self.sections)
        self.assertIsNone(self.section.language)

    def test__set_section_language_wrong_language(self):
        self.section['language'] = 'INVALID_LANGUAGE'

        logger = logging.getLogger()
        with self.assertLogs(logger, 'WARNING') as cm:
            _set_section_language(self.sections)
            self.assertRegex(
                cm.output[0],
                'Section `language section` contain invalid language setting. '
                '\'Language `INVALID_LANGUAGE` is not a valid language name or '
                'not recognized by coala.\'')
            self.assertIsNone(self.section.language)


class ConfigurationGatheringCollectionTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv
        self.log_printer = LogPrinter(NullPrinter())

    def tearDown(self):
        close_objects(self.log_printer)
        sys.argv = self.old_argv

    def test_get_filtered_bears(self):
        sys.argv = ['coala', '-I']

        with bear_test_module():
            local_bears, global_bears = get_filtered_bears(
                None, self.log_printer)

        self.assertEqual(len(local_bears['cli']), TEST_BEARS_COUNT)

        self.assertEqual(
            [str(bear) for bear in local_bears['cli']],
            TEST_BEAR_NAMES)

        with bear_test_module():
            local_bears, global_bears = get_filtered_bears(
                ['Java'], self.log_printer)

        self.assertEqual(len(local_bears['cli']), 2)
        self.assertEqual(str(local_bears['cli'][0]),
                         "<class 'JavaTestBear.JavaTestBear'>")
        self.assertEqual(str(local_bears['cli'][1]),
                         "<class 'LineCountTestBear.LineCountTestBear'>")
        self.assertEqual(len(global_bears['cli']), 0)
