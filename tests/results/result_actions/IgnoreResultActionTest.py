import unittest
from os.path import exists

from coalib.misc.ContextManagers import make_temp
from coalib.results.Result import Result
from coalib.results.result_actions.IgnoreResultAction import IgnoreResultAction


class IgnoreResultActionTest(unittest.TestCase):

    def test_is_applicable(self):
        self.assertFalse(IgnoreResultAction.is_applicable('str', {}, {}))
        self.assertFalse(IgnoreResultAction.is_applicable(
            Result.from_values('origin', 'msg', "file doesn't exist", 2),
            {}, {}))
        with make_temp() as f_a:
            self.assertTrue(IgnoreResultAction.is_applicable(
                Result.from_values('origin', 'msg', f_a, 2), {}, {}))

    def test_no_orig(self):
        uut = IgnoreResultAction()
        with make_temp() as f_a:
            file_dict = {
                f_a: ['1\n', '2\n', '3\n']
            }

            file_diff_dict = {}

            # Apply an initial patch
            uut.apply(Result.from_values('origin', 'msg', f_a, 2),
                      file_dict, file_diff_dict, 'c', no_orig=True)
            self.assertFalse(exists(f_a + '.orig'))

    def test_ignore(self):
        uut = IgnoreResultAction()
        with make_temp() as f_a:
            file_dict = {
                f_a: ['1\n', '2\n', '3\n']
            }

            file_diff_dict = {}

            # Apply an initial patch
            uut.apply(Result.from_values('origin', 'msg', f_a, 2),
                      file_dict, file_diff_dict, 'c')
            self.assertEqual(
                file_diff_dict[f_a].modified,
                ['1\n', '2  // Ignore origin\n', '3\n'])
            with open(f_a, 'r') as f:
                self.assertEqual(file_diff_dict[f_a].modified, f.readlines())
            self.assertTrue(exists(f_a + '.orig'))

            # Apply a second patch, old patch has to stay!
            uut.apply(Result.from_values('else', 'msg', f_a, 1),
                      file_dict, file_diff_dict, 'c')
            self.assertEqual(
                file_diff_dict[f_a].modified,
                ['1  // Ignore else\n', '2  // Ignore origin\n', '3\n'])
            with open(f_a, 'r') as f:
                self.assertEqual(file_diff_dict[f_a].modified, f.readlines())
