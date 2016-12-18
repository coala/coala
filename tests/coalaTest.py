import os
import re
import sys
import unittest
import unittest.mock
from pkg_resources import VersionConflict

from coalib import coala
from coala_utils.ContextManagers import prepare_file
from tests.TestUtilities import execute_coala, bear_test_module


class coalaTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_coala(self):
        with bear_test_module(), \
                prepare_file(['#fixme'], None) as (lines, filename):
            retval, output = execute_coala(
                             coala.main,
                             'coala', '-c', os.devnull,
                             '-f', re.escape(filename),
                             '-b', 'LineCountTestBear')
            self.assertIn('This file has 1 lines.',
                          output,
                          'The output should report count as 1 lines')

    def test_did_nothing(self):
        retval, output = execute_coala(coala.main, 'coala', '-I',
                                       '-S', 'default.enabled=false')
        self.assertEqual(retval, 2)
        self.assertIn('Did you forget to give the `--files`', output)

        retval, output = execute_coala(coala.main, 'coala', '-I',
                                       '-b', 'JavaTestBear', '-f', '*.java',
                                       '-S', 'default.enabled=false')
        self.assertEqual(retval, 2)
        self.assertIn('Nothing to do.', output)

    def test_show_all_bears(self):
        with bear_test_module():
            retval, output = execute_coala(coala.main, 'coala', '-B')
            self.assertEqual(retval, 0)
            # 6 bears plus 1 line holding the closing colour escape sequence
            self.assertEqual(len(output.strip().splitlines()), 7)

    def test_show_language_bears(self):
        with bear_test_module():
            retval, output = execute_coala(
                coala.main, 'coala', '-B', '-l', 'java')
            self.assertEqual(retval, 0)
            # 2 bears plus 1 line holding the closing colour escape sequence
            self.assertEqual(len(output.splitlines()), 3)

    def test_show_capabilities_with_supported_language(self):
        with bear_test_module():
            retval, output = execute_coala(
                coala.main, 'coala', '-p', 'R')
            self.assertEqual(retval, 0)
            self.assertEqual(len(output.splitlines()), 2)

    @unittest.mock.patch('coalib.parsing.DefaultArgParser.get_all_bears_names')
    @unittest.mock.patch('coalib.collecting.Collectors.icollect_bears')
    def test_version_conflict_in_collecting_bears(self, import_fn, _):
        with bear_test_module():
            import_fn.side_effect = VersionConflict('msg1', 'msg2')
            retval, output = execute_coala(coala.main, 'coala', '-B')
            self.assertEqual(retval, 13)
            self.assertIn(('There is a conflict in the version of a '
                           'dependency you have installed'), output)
            self.assertIn('pip install "msg2"', output)

    @unittest.mock.patch('coalib.collecting.Collectors._import_bears')
    def test_unimportable_bear(self, import_fn):
        with bear_test_module():
            import_fn.side_effect = SyntaxError
            retval, output = execute_coala(coala.main, 'coala', '-B')
            self.assertEqual(retval, 0)
            self.assertIn('Unable to collect bears from', output)

            import_fn.side_effect = VersionConflict('msg1', 'msg2')
            retval, output = execute_coala(coala.main, 'coala', '-B')
            # Note that bear version conflicts don't give exitcode=13,
            # they just give a warning with traceback in log_level debug.
            self.assertEqual(retval, 0)
            self.assertRegex(output,
                             'Unable to collect bears from .* because there '
                             'is a conflict with the version of a dependency '
                             'you have installed')
            self.assertIn('pip install "msg2"', output)
