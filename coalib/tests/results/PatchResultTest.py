import sys

sys.path.insert(0, ".")
from coalib.results.Diff import Diff
from coalib.results.PatchResult import PatchResult
import unittest


class PatchResultTestCase(unittest.TestCase):
    def test_raises(self):
        self.assertRaises(TypeError, PatchResult, origin="test", message="test", diffs=5)
        self.assertRaises(TypeError, PatchResult("t", "t", {}).apply, 5)
        self.assertRaises(TypeError, PatchResult("t", "t", {}).__add__, 5)

    def test_apply(self):
        file_dict = {
            "f_a": ["1", "2", "3"],
            "f_b": ["1", "2", "3"]
        }
        expected_file_dict = {
            "f_a": ["1", "3_changed"],
            "f_b": ["1", "2", "3"]
        }
        diff = Diff()
        diff.delete_line(2)
        diff.change_line(3, "3", "3_changed")

        uut = PatchResult("origin", "msg", {"f_a": diff})
        uut.apply(file_dict)

        self.assertEqual(file_dict, expected_file_dict)

    def test_add(self):
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

        diff = Diff()
        diff.delete_line(2)
        uut1 = PatchResult("origin", "msg", {"f_a": diff})

        diff = Diff()
        diff.change_line(3, "3", "3_changed")
        uut2 = PatchResult("origin", "msg", {"f_a": diff})

        diff = Diff()
        diff.change_line(3, "3", "3_changed")
        uut3 = PatchResult("origin", "msg", {"f_b": diff})

        uut1 += uut2 + uut3
        uut1.apply(file_dict)

        self.assertEqual(file_dict, expected_file_dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
