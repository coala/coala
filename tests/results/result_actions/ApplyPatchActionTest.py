import unittest
import os
from os.path import isfile

from coala_utils.ContextManagers import make_temp
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.settings.Section import Section


class ApplyPatchActionTest(unittest.TestCase):

    def test_apply(self):
        uut = ApplyPatchAction()
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

            file_diff_dict = {}

            diff = Diff(file_dict[f_a])
            diff.delete_line(2)
            uut.apply_from_section(Result('origin', 'msg', diffs={f_a: diff}),
                                   file_dict,
                                   file_diff_dict,
                                   Section('t'))

            diff = Diff(file_dict[f_a])
            diff.change_line(3, '3\n', '3_changed\n')
            uut.apply_from_section(Result('origin', 'msg', diffs={f_a: diff}),
                                   file_dict,
                                   file_diff_dict,
                                   Section('t'))

            diff = Diff(file_dict[f_b])
            diff.change_line(3, '3\n', '3_changed\n')
            uut.apply(Result('origin', 'msg', diffs={f_b: diff}),
                      file_dict,
                      file_diff_dict)

            for filename in file_diff_dict:
                file_dict[filename] = file_diff_dict[filename].modified

            self.assertEqual(file_dict, expected_file_dict)
            with open(f_a) as fa:
                self.assertEqual(file_dict[f_a], fa.readlines())
            with open(f_b) as fb:
                self.assertEqual(file_dict[f_b], fb.readlines())
            with open(f_c) as fc:
                # File c is unchanged and should be untouched
                self.assertEqual([], fc.readlines())

    def test_apply_orig_option(self):
        uut = ApplyPatchAction()
        with make_temp() as f_a, make_temp() as f_b:
            file_dict = {
                f_a: ['1\n', '2\n', '3\n'],
                f_b: ['1\n', '2\n', '3\n']
                }
            expected_file_dict = {
                f_a: ['1\n', '2\n', '3_changed\n'],
                f_b: ['1\n', '2\n', '3_changed\n']
                }
            file_diff_dict = {}
            diff = Diff(file_dict[f_a])
            diff.change_line(3, '3\n', '3_changed\n')
            uut.apply(Result('origin', 'msg', diffs={f_a: diff}),
                      file_dict,
                      file_diff_dict,
                      no_orig=True)
            diff = Diff(file_dict[f_b])
            diff.change_line(3, '3\n', '3_changed\n')
            uut.apply(Result('origin', 'msg', diffs={f_b: diff}),
                      file_dict,
                      file_diff_dict,
                      no_orig=False)
            self.assertFalse(isfile(f_a+'.orig'))
            self.assertTrue(isfile(f_b+'.orig'))

            for filename in file_diff_dict:
                file_dict[filename] = file_diff_dict[filename].modified

            self.assertEqual(file_dict, expected_file_dict)

    def test_apply_rename(self):
        uut = ApplyPatchAction()
        with make_temp() as f_a:
            file_dict = {f_a: ['1\n', '2\n', '3\n']}
            expected_file_dict = {f_a+'.renamed':
                                      ['1\n', '2_changed\n', '3_changed\n']}
            file_diff_dict = {}
            diff = Diff(file_dict[f_a], rename=f_a+'.renamed')
            diff.change_line(3, '3\n', '3_changed\n')
            uut.apply(Result('origin', 'msg', diffs={f_a: diff}),
                      file_dict,
                      file_diff_dict)
            self.assertTrue(isfile(f_a+'.orig'))
            self.assertTrue(isfile(f_a+'.renamed'))
            self.assertFalse(isfile(f_a))

            diff = Diff(file_dict[f_a])
            diff.change_line(2, '2\n', '2_changed\n')
            uut.apply(Result('origin', 'msg', diffs={f_a: diff}),
                      file_dict,
                      file_diff_dict)
            self.assertFalse(isfile(f_a+'.renamed.orig'))

            file_dict = {f_a+'.renamed': open(f_a+'.renamed').readlines()}

            self.assertEqual(file_dict, expected_file_dict)
            # Recreate file so that context manager make_temp() can delete it
            open(f_a, 'w').close()

    def test_apply_delete(self):
        uut = ApplyPatchAction()
        with make_temp() as f_a:
            file_dict = {f_a: ['1\n', '2\n', '3\n']}
            file_diff_dict = {}
            diff = Diff(file_dict[f_a], delete=True)
            uut.apply(Result('origin', 'msg', diffs={f_a: diff}),
                      file_dict,
                      file_diff_dict)
            self.assertFalse(isfile(f_a))
            self.assertTrue(isfile(f_a+'.orig'))
            os.remove(f_a+'.orig')

            diff = Diff(file_dict[f_a])
            diff.change_line(3, '3\n', '3_changed\n')
            uut.apply(Result('origin', 'msg', diffs={f_a: diff}),
                      file_dict,
                      file_diff_dict)
            self.assertFalse(isfile(f_a+'.orig'))
            # Recreate file so that context manager make_temp() can delete it
            open(f_a, 'w').close()

    def test_is_applicable(self):
        diff = Diff(['1\n', '2\n', '3\n'])
        diff.delete_line(2)
        patch_result = Result('', '', diffs={'f': diff})
        self.assertTrue(
            ApplyPatchAction.is_applicable(patch_result, {}, {}))

    def test_is_applicable_conflict(self):
        diff = Diff(['1\n', '2\n', '3\n'])
        diff.add_lines(2, ['a line'])

        conflict_result = Result('', '', diffs={'f': diff})
        # Applying the same diff twice will result in a conflict
        self.assertIn(
            'Two or more patches conflict with each other: ',
            ApplyPatchAction.is_applicable(conflict_result, {}, {'f': diff})
        )

    def test_is_applicable_empty_patch(self):
        diff = Diff([], rename='new_name')
        result = Result('', '', diffs={'f': diff})

        # Two renames donot result in any change
        self.assertEqual(
            ApplyPatchAction.is_applicable(result, {}, {'f': diff}),
            'The given patches do not change anything anymore.'
        )

    def test_is_applicable_without_patch(self):
        result = Result('', '')
        self.assertEqual(
            ApplyPatchAction.is_applicable(result, {}, {}),
            'This result has no patch attached.'
        )
