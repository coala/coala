import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.Diff import Diff
from coalib.results.PatchResult import PatchResult
from coalib.results.Result import Result
from coalib.settings.Section import Section

class ApplyPatchActionTest(unittest.TestCase):
    def test_apply(self):
        uut = ApplyPatchAction()
        file_dict = {
            "f_a": ["1", "2", "3"],
            "f_b": ["1", "2", "3"],
            "f_c": ["1", "2", "3"]
        }
        expected_file_dict = {
            "f_a": ["1", "3_changed"],
            "f_b": ["1", "2", "3_changed"],
            "f_c": ["1", "2", "3"]
        }

        file_diff_dict = {}

        diff = Diff()
        diff.delete_line(2)
        uut.apply_from_section(PatchResult("origin", "msg", {"f_a": diff}),
                               file_dict,
                               file_diff_dict,
                               Section("t"))

        diff = Diff()
        diff.change_line(3, "3", "3_changed")
        uut.apply_from_section(PatchResult("origin", "msg", {"f_a": diff}),
                               file_dict,
                               file_diff_dict,
                               Section("t"))

        diff = Diff()
        diff.change_line(3, "3", "3_changed")
        uut.apply(PatchResult("origin", "msg", {"f_b": diff}),
                  file_dict,
                  file_diff_dict)

        for filename in file_diff_dict:
            file_dict[filename] = (
                file_diff_dict[filename].apply(file_dict[filename]))

        self.assertEqual(file_dict, expected_file_dict)

    def test_is_applicable(self):
        patch_result = PatchResult("", "", {})
        result = Result("", "")
        self.assertTrue(ApplyPatchAction.is_applicable(patch_result))
        self.assertFalse(ApplyPatchAction.is_applicable(result))


if __name__ == '__main__':
    unittest.main(verbosity=2)
