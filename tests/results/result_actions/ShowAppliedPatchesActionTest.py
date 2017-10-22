import unittest

from coala_utils.ContextManagers import make_temp
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.ShowAppliedPatchesAction import \
    ShowAppliedPatchesAction
from coalib.settings.Section import Section
from coala_utils.ContextManagers import (
    make_temp, retrieve_stdout, simulate_console_inputs)


class ShowAppliedPatchesActionTest(unittest.TestCase):

    def test_apply(self):
        uut = ShowAppliedPatchesAction()

        with make_temp() as f_a, make_temp() as f_b, make_temp() as f_c:

            file_dict = {
                f_a: ['1\n', '2\n', '3\n'],
                f_b: ['1\n', '2\n', '3\n'],
                f_c: ['1\n', '2\n', '3\n']
            }
            expected_file_dict = {
                f_a: ['1\n', '3_changed\n'],
                f_b: ['1\n', '2\n', '3_changed\n'],
                f_c: ['1\n', '2\n', '3\n']
            }

            with make_temp() as testfile_path:
                file_diff_dict = {}
                file_dict = {testfile_path: ['1\n', '2\n', '3\n']}
                diff = Diff(file_dict[testfile_path])
                diff.delete_line(2)
                diff.change_line(3, '3\n', '3_changed\n')
                result = Result('origin', 'msg', diffs={f_a: diff},
                                applied_actions={'ApplyPatchAction': [Result(
                                    'origin', 'message',
                                    diffs={testfile_path: diff}),
                                    file_dict, file_diff_dict, Section('')]})

                self.assertTrue(uut.apply(result,
                                          file_dict,
                                          file_diff_dict))
