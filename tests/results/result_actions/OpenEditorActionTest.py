import os
import subprocess
import tempfile
import unittest
from importlib import reload

import coalib.results.result_actions.OpenEditorAction
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.settings.Section import Section, Setting


class OpenEditorActionTest(unittest.TestCase):

    @staticmethod
    def fake_edit(commands):
        filename = commands[1]
        with open(filename) as f:
            lines = f.readlines()

        del lines[1]

        with open(filename, 'w') as f:
            f.writelines(lines)

    @staticmethod
    def fake_edit_subl(commands, stdout):
        """
        Solely the declaration raises an exception if stdout not provided.
        """
        assert ('--wait' in commands), 'Did not wait for the editor to close'

    def setUp(self):
        fahandle, self.fa = tempfile.mkstemp()
        os.close(fahandle)
        fbhandle, self.fb = tempfile.mkstemp()
        os.close(fbhandle)
        self.old_subprocess_call = subprocess.call

    def tearDown(self):
        os.remove(self.fa)
        os.remove(self.fb)
        subprocess.call = self.old_subprocess_call

    def test_apply(self):
        # Initial file contents, *before* a patch was applied
        file_dict = {
            self.fa: ['1\n', '2\n', '3\n'],
            self.fb: ['1\n', '2\n', '3\n'],
            'f_c': ['1\n', '2\n', '3\n']}

        # A patch that was applied for some reason to make things complicated
        diff_dict = {self.fb: Diff(file_dict[self.fb])}
        diff_dict[self.fb].change_line(3, '3\n', '3_changed\n')

        # File contents after the patch was applied, that's what's in the files
        current_file_dict = {
            filename: diff_dict[filename].modified
            if filename in diff_dict else file_dict[filename]
            for filename in (self.fa, self.fb)}
        for filename in current_file_dict:
            with open(filename, 'w') as handle:
                handle.writelines(current_file_dict[filename])

        # End file contents after the patch and the OpenEditorAction was
        # applied
        expected_file_dict = {
            self.fa: ['1\n', '3\n'],
            self.fb: ['1\n', '3_changed\n'],
            'f_c': ['1\n', '2\n', '3\n']}

        section = Section('')
        section.append(Setting('editor', ''))
        uut = OpenEditorAction()
        subprocess.call = self.fake_edit
        diff_dict = uut.apply_from_section(
            Result.from_values('origin', 'msg', self.fa),
            file_dict,
            diff_dict,
            section)
        diff_dict = uut.apply_from_section(
            Result.from_values('origin', 'msg', self.fb),
            file_dict,
            diff_dict,
            section)

        for filename in diff_dict:
            file_dict[filename] = (
                diff_dict[filename].modified)

        self.assertEqual(file_dict, expected_file_dict)

    def test_apply_rename(self):
        # Initial file contents, *before* a patch was applied
        file_dict = {
            self.fa: ['1\n', '2\n', '3\n']}

        # A patch that was applied for some reason to make things complicated
        file_diff_dict = {}
        diff = Diff(file_dict[self.fa], rename=self.fa+'.renamed')
        diff.change_line(3, '3\n', '3_changed\n')
        ApplyPatchAction().apply(
            Result('origin', 'msg', diffs={self.fa: diff}),
            file_dict,
            file_diff_dict)
        # End file contents after the patch and the OpenEditorAction was
        # applied
        expected_file_dict = {
            self.fa: ['1\n', '3_changed\n']}

        section = Section('')
        section.append(Setting('editor', ''))
        uut = OpenEditorAction()
        subprocess.call = self.fake_edit
        diff_dict = uut.apply_from_section(
            Result.from_values('origin', 'msg', self.fa),
            file_dict,
            file_diff_dict,
            section)

        for filename in diff_dict:
            file_dict[filename] = (
                file_diff_dict[filename].modified)

        self.assertEqual(file_dict, expected_file_dict)
        open(self.fa, 'w').close()

    def test_subl(self):
        file_dict = {self.fa: []}
        section = Section('')
        section.append(Setting('editor', 'subl'))
        uut = OpenEditorAction()
        subprocess.call = self.fake_edit_subl
        diff_dict = uut.apply_from_section(
            Result.from_values('origin', 'msg', self.fa),
            file_dict,
            {},
            section)
        file_dict[self.fa] = diff_dict[self.fa].modified

        self.assertEqual(file_dict, file_dict)

    def test_is_applicable(self):
        result1 = Result('', '')
        result2 = Result.from_values('', '', '')
        result3 = Result.from_values('', '', 'file')
        invalid_result = ''

        self.assertEqual(
            OpenEditorAction.is_applicable(result1, None, {}),
            'The result is not associated with any source code.')

        self.assertTrue(OpenEditorAction.is_applicable(result2, None, {}))

        # Check non-existent file
        self.assertEqual(
            OpenEditorAction.is_applicable(result3, None, {}),
            "The result is associated with source code that doesn't "
            'seem to exist.')

        with self.assertRaises(TypeError):
            OpenEditorAction.is_applicable(invalid_result, None, {})

    def test_environ_editor(self):
        old_environ = os.environ

        file_dict = {self.fb: ['1\n', '2\n', '3\n']}
        diff_dict = {}
        subprocess.call = self.fake_edit
        with open(self.fb, 'w') as handle:
            handle.writelines(file_dict[self.fb])
        result = Result.from_values('origin', 'msg', self.fb)

        # Currently an ``editor`` param is required, so this will raise
        # a ``TypeError``.
        from coalib.results.result_actions.OpenEditorAction import (
            OpenEditorAction)
        action = OpenEditorAction()
        with self.assertRaises(TypeError):
            action.apply(result, file_dict, diff_dict)

        # If we reload the module after setting the ``$EDITOR`` variable,
        # we should be able apply the action without an explicit variable.
        os.environ['EDITOR'] = 'vim'
        reload(coalib.results.result_actions.OpenEditorAction)
        from coalib.results.result_actions.OpenEditorAction import (
            OpenEditorAction)
        action = OpenEditorAction()
        action.apply(result, file_dict, diff_dict)

        os.environ = old_environ
