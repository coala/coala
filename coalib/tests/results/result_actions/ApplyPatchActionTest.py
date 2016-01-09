import os
import sys
from tempfile import mkstemp
import unittest

sys.path.insert(0, ".")
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.settings.Section import Section


class ApplyPatchActionTest(unittest.TestCase):

    def test_apply(self):
        uut = ApplyPatchAction()
        fh_a, f_a = mkstemp()
        fh_b, f_b = mkstemp()
        fh_c, f_c = mkstemp()
        os.close(fh_a)
        os.close(fh_b)
        os.close(fh_c)

        file_dict = {
            f_a: ["1\n", "2\n", "3\n"],
            f_b: ["1\n", "2\n", "3\n"],
            f_c: ["1\n", "2\n", "3\n"]
        }
        expected_file_dict = {
            f_a: ["1\n", "3_changed\n"],
            f_b: ["1\n", "2\n", "3_changed\n"],
            f_c: ["1\n", "2\n", "3\n"]
        }

        file_diff_dict = {}

        diff = Diff(file_dict[f_a])
        diff.delete_line(2)
        uut.apply_from_section(Result("origin", "msg", diffs={f_a: diff}),
                               file_dict,
                               file_diff_dict,
                               Section("t"))

        diff = Diff(file_dict[f_a])
        diff.change_line(3, "3\n", "3_changed\n")
        uut.apply_from_section(Result("origin", "msg", diffs={f_a: diff}),
                               file_dict,
                               file_diff_dict,
                               Section("t"))

        diff = Diff(file_dict[f_b])
        diff.change_line(3, "3\n", "3_changed\n")
        uut.apply(Result("origin", "msg", diffs={f_b: diff}),
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

        os.remove(f_a)
        os.remove(f_b)
        os.remove(f_c)

    def test_is_applicable(self):
        diff = Diff(["1\n", "2\n", "3\n"])
        diff.delete_line(2)
        patch_result = Result("", "", diffs={'f': diff})
        self.assertTrue(
            ApplyPatchAction.is_applicable(patch_result, {}, {}))

    def test_is_applicable_conflict(self):
        diff = Diff(["1\n", "2\n", "3\n"])
        diff.add_lines(2, ['a line'])

        conflict_result = Result("", "", diffs={'f': diff})
        # Applying the same diff twice will result in a conflict
        self.assertFalse(
            ApplyPatchAction.is_applicable(conflict_result, {}, {'f': diff}))

    def test_is_applicable_empty_patch(self):
        empty_patch_result = Result("", "", diffs={})
        self.assertFalse(
            ApplyPatchAction.is_applicable(empty_patch_result, {}, {}))

    def test_is_applicable_without_patch(self):
        result = Result("", "")
        self.assertFalse(ApplyPatchAction.is_applicable(result, {}, {}))


if __name__ == '__main__':
    unittest.main(verbosity=2)
