import os
import sys
import unittest
import unittest.mock
from pkg_resources import VersionConflict

from coalib.coala_main import run_coala
from coalib.output.printers.LogPrinter import LogPrinter
from coalib import assert_supported_version, coala
from pyprint.ConsolePrinter import ConsolePrinter
from coala_utils.ContextManagers import prepare_file
from coalib.output.Logging import configure_logging
from coala_utils.ContextManagers import (
    make_temp, retrieve_stdout, simulate_console_inputs)

from tests.TestUtilities import (
    bear_test_module,
    execute_coala,
    TEST_BEARS_COUNT,
    JAVA_BEARS_COUNT,
)

# Java bears plus 1 line holding the closing colour escape sequence.
JAVA_BEARS_COUNT_OUTPUT = JAVA_BEARS_COUNT + 1


class coalaTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_coala(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(
                             coala.main,
                             'coala', '-c', os.devnull,
                             '--non-interactive', '--no-color',
                             '-f', filename,
                             '-b', 'LineCountTestBear')
            self.assertIn('This file has 1 lines.',
                          stdout,
                          'The output should report count as 1 lines')
            self.assertEqual(1, len(stderr.splitlines()))
            self.assertIn(
                'LineCountTestBear: This result has no patch attached.',
                stderr)
            self.assertNotEqual(retval, 0,
                                'coala must return nonzero when errors occured')

    def test_coala2(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            with simulate_console_inputs('a', 'n') as generator, \
                    retrieve_stdout() as sio:
                retval, stdout, stderr = execute_coala(
                                 coala.main,
                                 'coala', '-c', os.devnull,
                                 '--non-interactive', '--no-color',
                                 '-f', filename,
                                 '-b', 'LineCountTestBear', '-A')
                self.assertIn('',
                              stdout,
                              '')
                self.assertEqual(1, len(stderr.splitlines()))
                self.assertIn(
                    'LineCountTestBear: This result has no patch attached.',
                    stderr)
                self.assertNotEqual(retval, 0,
                                    'coala must return nonzero when errors '
                                    'occured')

    def test_coala3(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            with simulate_console_inputs('1', 'n') as generator, \
                    retrieve_stdout() as sio:
                retval, stdout, stderr = execute_coala(
                                 coala.main,
                                 'coala', '-c', os.devnull,
                                 '--non-interactive', '--no-color',
                                 '-f', filename,
                                 '-b', 'LineCountTestBear', '-A')
                self.assertIn('',
                              stdout,
                              '')
                self.assertEqual(1, len(stderr.splitlines()))
                self.assertIn(
                    'LineCountTestBear: This result has no patch attached.',
                    stderr)
                self.assertNotEqual(retval, 0,
                                    'coala must return nonzero when errors '
                                    'occured')

    def test_coala4(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            with simulate_console_inputs('x', 'n') as generator, \
                    retrieve_stdout() as sio:
                retval, stdout, stderr = execute_coala(
                                 coala.main,
                                 'coala', '-c', os.devnull,
                                 '--non-interactive', '--no-color',
                                 '-f', filename,
                                 '-b', 'LineCountTestBear', '-A')
                self.assertIn('',
                              stdout,
                              '')
                self.assertEqual(1, len(stderr.splitlines()))
                self.assertIn(
                    'LineCountTestBear: This result has no patch attached.',
                    stderr)
                self.assertNotEqual(retval, 0,
                                    'coala must return nonzero when errors '
                                    'occured')

    def test_coala_aspect(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(
                             coala.main,
                             'coala', '-c', os.devnull,
                             '--non-interactive', '--no-color',
                             '-f', filename,
                             '-S', 'cli.aspects=UnusedLocalVariable',
                             'cli.language=Python')
            self.assertIn(
                'AspectTestBear: This result has no patch attached.',
                stderr)
            self.assertIn('This is just a dummy result',
                          stdout)
            self.assertNotEqual(retval, 0,
                                'coala must return nonzero when errors occured')

    @unittest.mock.patch('sys.version_info', tuple((2, 7, 11)))
    def test_python_version_27(self):
        with self.assertRaises(SystemExit) as cm:
            assert_supported_version()

        self.assertEqual(cm.exception.code, 4)

    @unittest.mock.patch('sys.version_info', tuple((3, 3, 6)))
    def test_python_version_33(self):
        with self.assertRaises(SystemExit) as cm:
            assert_supported_version()

        self.assertEqual(cm.exception.code, 4)

    def test_python_version_34(self):
        assert_supported_version()

    def test_did_nothing(self, debug=False):
        retval, stdout, stderr = execute_coala(coala.main, 'coala', '-I',
                                               '-S', 'cli.enabled=false',
                                               debug=debug)
        self.assertEqual(retval, 2)
        self.assertIn('Did you forget to give the `--files`', stderr)
        self.assertFalse(stdout)

        retval, stdout, stderr = execute_coala(coala.main, 'coala', '-I',
                                               '-b', 'JavaTestBear', '-f',
                                               '*.java',
                                               '-S', 'cli.enabled=false',
                                               debug=debug)
        self.assertEqual(retval, 2)
        self.assertIn('Nothing to do.', stderr)
        self.assertFalse(stdout)

    def test_did_nothing_debug(self):
        self.test_did_nothing(debug=True)

    def test_show_all_bears(self, debug=False):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '-I', debug=debug)
            self.assertEqual(retval, 0)
            # All bears plus 1 line holding the closing colour escape sequence.
            self.assertEqual(len(stdout.strip().splitlines()),
                             TEST_BEARS_COUNT + 1)
            self.assertFalse(stderr)

    def test_show_all_bears_debug(self):
        return self.test_show_all_bears(debug=True)

    def test_show_language_bears(self, debug=False):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-B', '-l', 'java', '-I', debug=debug)
            self.assertEqual(retval, 0)
            self.assertEqual(len(stdout.splitlines()),
                             JAVA_BEARS_COUNT_OUTPUT)
            self.assertIn(
                "'--filter-by-language ...' is deprecated", stderr)

    def test_show_language_bears_debug(self):
        self.test_show_language_bears(debug=True)

    def test_show_capabilities_with_supported_language(self, debug=False):
        with bear_test_module():
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '-p', 'R', '-I', debug=debug)
            self.assertEqual(retval, 0)
            self.assertEqual(len(stdout.splitlines()), 2)
            self.assertFalse(stderr)

    def test_execute_with_bad_filters(self, debug=False):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala', '--filter-by', 'language', 'python',
                '-f', filename, '-b', 'TestBear', '--no-color', '-I',
                debug=debug)

            self.assertIn(
                "'language_filter' can only handle ('bearclass',). "
                'The context of your usage might be wrong.', stdout)
            # Calling without config, hence 0
            # else, it'll be 1
            self.assertEqual(retval, 0)

    def test_execute_with_bad_filters_debug(self):
        self.test_execute_with_bad_filters(True)

    def test_execute_with_filters(self, debug=False):
        coala_config = ('[section_one]',
                        'tags = save',
                        '[section_two]',
                        'tags = change',)

        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (_, filename), \
                prepare_file(coala_config, None) as (_, configuration):
            results, retval, _ = run_coala(
                                    console_printer=ConsolePrinter(),
                                    log_printer=LogPrinter(),
                                    arg_list=(
                                        '-c', configuration,
                                        '-f', filename,
                                        '-b', 'TestBear',
                                        '--filter-by', 'section_tags',
                                        'save'
                                    ),
                                    autoapply=False,
                                    debug=debug)

            self.assertTrue('section_one' in results)

    def test_execute_with_filters_debug(self):
        self.test_execute_with_filters(True)

    def test_show_capabilities_with_supported_language_debug(self):
        self.test_show_capabilities_with_supported_language(debug=True)

    @unittest.mock.patch('coalib.collecting.Collectors.icollect_bears')
    def test_version_conflict_in_collecting_bears(self, import_fn):
        with bear_test_module():
            import_fn.side_effect = VersionConflict('msg1', 'msg2')
            retval, stdout, stderr = execute_coala(coala.main, 'coala', '-B')
            self.assertEqual(retval, 13)
            self.assertIn(('There is a conflict in the version of a '
                           'dependency you have installed'), stderr)
            self.assertIn('pip3 install "msg2"', stderr)
            self.assertFalse(stdout)
            self.assertNotEqual(retval, 0,
                                'coala must return nonzero when errors occured')

    @unittest.mock.patch('coalib.collecting.Collectors._import_bears')
    def test_unimportable_bear(self, import_fn):
        with bear_test_module():
            import_fn.side_effect = SyntaxError
            retval, stdout, stderr = execute_coala(coala.main, 'coala', '-B')
            self.assertEqual(retval, 0)
            self.assertIn('Unable to collect bears from', stderr)
            self.assertIn('No bears to show.', stdout)

            import_fn.side_effect = VersionConflict('msg1', 'msg2')
            retval, stdout, stderr = execute_coala(coala.main, 'coala', '-B')
            # Note that bear version conflicts don't give exitcode=13,
            # they just give a warning with traceback in log_level debug.
            self.assertEqual(retval, 0)
            self.assertRegex(stderr,
                             'Unable to collect bears from .* because there '
                             'is a conflict with the version of a dependency '
                             'you have installed')
            self.assertIn('pip3 install "msg2"', stderr)
            self.assertIn('No bears to show.', stdout)

    def test_run_coala_no_autoapply(self, debug=False):
        with bear_test_module(), \
                prepare_file(['#fixme  '], None) as (lines, filename):
            self.assertEqual(
                1,
                len(run_coala(
                    console_printer=ConsolePrinter(),
                    log_printer=LogPrinter(),
                    arg_list=(
                        '-c', os.devnull,
                        '-f', filename,
                        '-b', 'SpaceConsistencyTestBear',
                        '--apply-patches',
                        '-S', 'use_spaces=yeah'
                    ),
                    autoapply=False,
                    debug=debug
                )[0]['cli'])
            )

            self.assertEqual(
                0,
                len(run_coala(
                    console_printer=ConsolePrinter(),
                    log_printer=LogPrinter(),
                    arg_list=(
                        '-c', os.devnull,
                        '-f', filename,
                        '-b', 'SpaceConsistencyTestBear',
                        '--apply-patches',
                        '-S', 'use_spaces=yeah'
                    ),
                    debug=debug
                )[0]['cli'])
            )

    def test_run_coala_no_autoapply_debug(self):
        self.test_run_coala_no_autoapply(debug=True)

    def test_logged_error_causes_non_zero_exitcode(self):
        configure_logging()
        with bear_test_module(), \
                prepare_file(['#fixme  '], None) as (lines, filename):
            _, exitcode, _ = run_coala(
                console_printer=ConsolePrinter(),
                log_printer=LogPrinter(),
                arg_list=(
                    '-c', os.devnull,
                    '-f', filename,
                    '-b', 'ErrorTestBear'
                ),
                autoapply=False
            )

            assert exitcode == 1

    def test_coala_with_color(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(
                coala.main, 'coala')
            errors = filter(bool, stderr.split('\n'))
            # Every error message must start with characters
            # used for coloring.
            for err in errors:
                self.assertNotRegex(err, r'^\[WARNING\]')
            self.assertEqual(
                retval, 0, 'coala must return zero when there are no errors')

    def test_coala_without_color(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):

            retval, stdout, stderr = execute_coala(
                             coala.main, 'coala', '-N')
            errors = filter(bool, stderr.split('\n'))
            # Any error message must not start with characters
            # used for coloring.
            for err in errors:
                self.assertRegex(err, r'^\[WARNING\]')
            self.assertEqual(
                retval, 0, 'coala must return zero when there are no errors')

    def test_coala_ignore_file(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, stdout, stderr = execute_coala(
                    coala.main, 'coala',
                    '-c', os.devnull,
                    '--non-interactive',
                    '-f', filename,
                    '--ignore', filename,
                    '-b', 'LineCountTestBear')
            self.assertEqual(stdout, 'Executing section cli...\n')
            self.assertEqual(
                retval, 0, 'coala must return zero when there are no errors')
