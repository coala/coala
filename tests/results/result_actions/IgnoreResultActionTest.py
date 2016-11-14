import unittest

from coalib.misc.ContextManagers import make_temp
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.IgnoreResultAction import IgnoreResultAction


class IgnoreResultActionTest(unittest.TestCase):

    def test_ignore(self):
        uut = IgnoreResultAction()
        with make_temp() as f_a:

            file_dict = {
                f_a: ["1\n", "2\n", "3\n"]
            }
            expected_file_dict = {
                f_a: ["1\n", "3_changed\n"],
            }

            file_diff_dict = {}

            diff = Diff(file_dict[f_a])
            diff.delete_line(2)
            uut.apply(Result("origin", "msg", diffs={f_a: diff}),
                      file_dict,
                      file_diff_dict,
                      "c",
                      "f_a",
                      False)

            for filename in file_diff_dict:
                file_dict[filename] = file_diff_dict[filename].modified

            self.assertEqual(file_dict, expected_file_dict)
