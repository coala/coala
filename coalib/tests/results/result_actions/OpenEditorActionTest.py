import subprocess
import sys
import os
import unittest
import tempfile

sys.path.insert(0, ".")
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.settings.Section import Section, Setting


class ResultActionTest(unittest.TestCase):
    @staticmethod
    def fake_edit(commands):
        filename = commands[1]
        with open(filename) as f:
            lines = f.readlines()

        del lines[1]

        with open(filename, "w") as f:
            f.writelines(lines)

    @staticmethod
    def fake_edit_subl(commands, stdout):
        """
        Solely the declaration raises an exception if stdout not provided.
        """
        assert ("--wait" in commands), "Did not wait for the editor to close"

    def setUp(self):
        fahandle, self.fa = tempfile.mkstemp()
        os.close(fahandle)
        fbhandle, self.fb = tempfile.mkstemp()
        os.close(fbhandle)

    def tearDown(self):
        os.remove(self.fa)
        os.remove(self.fb)

    def test_apply(self):
        # Initial file contents, *before* a patch was applied
        file_dict = {
            self.fa: ["1\n", "2\n", "3\n"],
            self.fb: ["1\n", "2\n", "3\n"],
            "f_c": ["1\n", "2\n", "3\n"]}

        # A patch that was applied for some reason to make things complicated
        diff_dict = {self.fb: Diff(file_dict[self.fb])}
        diff_dict[self.fb].change_line(3, "3\n", "3_changed\n")

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
            self.fa: ["1\n", "3\n"],
            self.fb: ["1\n", "3_changed\n"],
            "f_c": ["1\n", "2\n", "3\n"]}

        section = Section("")
        section.append(Setting("editor", ""))
        uut = OpenEditorAction()
        subprocess.call = self.fake_edit
        diff_dict = uut.apply_from_section(
            Result.from_values("origin", "msg", self.fa),
            file_dict,
            diff_dict,
            section)
        diff_dict = uut.apply_from_section(
            Result.from_values("origin", "msg", self.fb),
            file_dict,
            diff_dict,
            section)

        for filename in diff_dict:
            file_dict[filename] = (
                diff_dict[filename].modified)

        self.assertEqual(file_dict, expected_file_dict)

    def test_subl(self):
        file_dict = {self.fa: []}
        section = Section("")
        section.append(Setting("editor", "subl"))
        uut = OpenEditorAction()
        subprocess.call = self.fake_edit_subl
        diff_dict = uut.apply_from_section(
            Result.from_values("origin", "msg", self.fa),
            file_dict,
            {},
            section)
        file_dict[self.fa] = diff_dict[self.fa].modified

        self.assertEqual(file_dict, file_dict)

    def test_is_applicable(self):
        result1 = Result("", "")
        result2 = Result.from_values("", "", "")
        invalid_result = ""
        self.assertFalse(OpenEditorAction.is_applicable(result1, None, None))
        self.assertTrue(OpenEditorAction.is_applicable(result2, None, None))

        self.assertFalse(
            OpenEditorAction.is_applicable(invalid_result, None, None))
if __name__ == '__main__':
    unittest.main(verbosity=2)
