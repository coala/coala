import unittest

from coala_utils.ContextManagers import retrieve_stdout
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.DoNothingAction import DoNothingAction
from coalib.settings.Section import Section, Setting


class DoNothingActionTest(unittest.TestCase):

    def setUp(self):
        self.uut = DoNothingAction()
        self.file_dict = {'a': ['a\n', 'b\n', 'c\n'], 'b': ['old_first\n']}
        self.diff_dict = {'a': Diff(self.file_dict['a']),
                          'b': Diff(self.file_dict['b'])}
        self.diff_dict['a'].add_lines(1, ['test\n'])
        self.diff_dict['a'].delete_line(3)
        self.diff_dict['b'].add_lines(0, ['first\n'])

        self.test_result = Result('origin', 'message', diffs=self.diff_dict)
        self.section = Section('name')
        self.section.append(Setting('colored', 'false'))

    def test_is_applicable(self):
        diff = Diff([], rename='new_name')
        result = Result('', '', diffs={'f': diff})

        self.assertTrue(self.uut.is_applicable(result, {}, {'f': diff}))

    def test_apply(self):
        with retrieve_stdout() as stdout:
            self.assertEqual(self.uut.apply(self.test_result,
                                            self.file_dict,
                                            {}), None)
