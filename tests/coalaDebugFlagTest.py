import os
import re
import sys

import unittest
from unittest.mock import MagicMock, patch

from coalib import coala
from coala_utils.ContextManagers import prepare_file

from tests.TestUtilities import execute_coala, bear_test_module


# patch gets strangely lost when only defined in method or with context where
# actually needed
@patch('coalib.coala_modes.mode_json')
class coalaDebugFlagTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def pipReqIsInstalledMock(self):
        """
        Prepare a patch for ``PipRequirement.is_installed`` method that
        always returns ``True``, used for faking an installed ipdb.
        """
        return patch('dependency_management.requirements.PipRequirement.'
                     'PipRequirement.is_installed', lambda self: True)

    def pipReqIsNotInstalledMock(self):
        """
        Prepare a patch for ``PipRequirement.is_installed`` method that
        always returns ``False``, used for faking a not installed ipdb.
        """
        return patch('dependency_management.requirements.PipRequirement.'
                     'PipRequirement.is_installed', lambda self: False)

    def ipdbMock(self):
        """
        Prepare a mocked ``ipdb`` module with a mocked
        ``launch_ipdb_on_exception`` function, which is used in
        ``coala --debug`` mode to open and ``ipdb>`` prompt when unexpected
        exceptions occur
        """
        mock = MagicMock()

        def __exit__(self, *exc_info):
            """
            Make mocked ``ipdb.launch_ipdb_on_exception()`` context just
            reraise the exception.
            """
            raise

        mock.launch_ipdb_on_exception.__enter__ = None
        mock.launch_ipdb_on_exception.__exit__ = __exit__
        return mock

    def tearDown(self):
        sys.argv = self.old_argv

    def test_no_ipdb(self, mocked_mode_json):
        mocked_mode_json.side_effect = None
        with bear_test_module(), \
                prepare_file(['#fixme  '], None) as (lines, filename), \
                self.pipReqIsNotInstalledMock():
            # additionally use RaiseTestBear to verify independency from
            # failing bears
            status, stdout, stderr = execute_coala(
                coala.main, 'coala', '--debug', '--json',
                '-c', os.devnull,
                '-f', re.escape(filename),
                '-b', 'RaiseTestBear')
        assert status == 13
        assert not stdout
        assert '--debug flag requires ipdb.' in stderr

    def test_bear__init__raises(self, mocked_mode_json):
        mocked_mode_json.side_effect = None
        mocked_ipdb = self.ipdbMock()
        with bear_test_module(), \
                prepare_file(['#fixme  '], None) as (lines, filename), \
                self.pipReqIsInstalledMock(), \
                patch.dict('sys.modules', ipdb=mocked_ipdb), \
                self.assertRaisesRegex(
                    RuntimeError,
                    r'^The bear ErrorTestBear does not fulfill all '
                    r"requirements\. 'I_do_not_exist' is not installed\.$"):
            execute_coala(
                coala.main, 'coala', '--debug',
                '-c', os.devnull,
                '-f', re.escape(filename),
                '-b', 'ErrorTestBear')

        mocked_ipdb.launch_ipdb_on_exception.assert_called_once_with()

    def test_bear_run_raises(self, mocked_mode_json):
        mocked_mode_json.side_effect = None
        mocked_ipdb = self.ipdbMock()
        with bear_test_module(), \
                prepare_file(['#fixme  '], None) as (lines, filename), \
                self.pipReqIsInstalledMock(), \
                patch.dict('sys.modules', ipdb=mocked_ipdb), \
                self.assertRaisesRegex(
                    RuntimeError, r"^That's all the RaiseTestBear can do\.$"):
            execute_coala(
                coala.main, 'coala', '--debug',
                '-c', os.devnull,
                '-f', re.escape(filename),
                '-b', 'RaiseTestBear')

        mocked_ipdb.launch_ipdb_on_exception.assert_called_once_with()

    def test_coala_main_mode_json_launches_ipdb(self, mocked_mode_json):
        mocked_mode_json.side_effect = RuntimeError('Mocked mode_json fails.')
        mocked_ipdb = self.ipdbMock()
        with bear_test_module(), \
                prepare_file(['#fixme  '], None) as (lines, filename), \
                self.pipReqIsInstalledMock(), \
                patch.dict('sys.modules', ipdb=mocked_ipdb), \
                self.assertRaisesRegex(RuntimeError,
                                       r'^Mocked mode_json fails\.$'):
            # additionally use RaiseTestBear to verify independency from
            # failing bears
            execute_coala(
                coala.main, 'coala', '--debug', '--json',
                '-c', os.devnull,
                '-f', re.escape(filename),
                '-b', 'RaiseTestBear')

        mocked_ipdb.launch_ipdb_on_exception.assert_called_once_with()
