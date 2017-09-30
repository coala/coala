import unittest
import os.path

from coalib.results.Diff import Diff
from coala_utils.ContextManagers import make_temp
from coalib.results.Result import Result
from coalib.results.result_actions.GeneratePatchesAction import (
    GeneratePatchesAction)
from coalib.settings.Section import Section, Setting
from coala_utils.ContextManagers import (
    make_temp, retrieve_stdout, simulate_console_inputs)
from tests.TestUtilities import (
    bear_test_module,
    execute_coala,
    TEST_BEARS_COUNT,
)
from coala_utils.ContextManagers import prepare_file


class GeneratePatchesActionTest(unittest.TestCase):

    def setUp(self):
        self.uut = GeneratePatchesAction()
        self.file_dict = {'a.py': ['a\n', 'b\n', 'c\n'], 'b': ['old_first\n']}
        self.diff_dict = {'a.py': Diff(self.file_dict['a.py']),
                          'b': Diff(self.file_dict['b'])}
        self.diff_dict['a.py'].add_lines(1, ['test\n'])
        self.diff_dict['a.py'].delete_line(3)
        self.diff_dict['b'].add_lines(0, ['first\n'])

        self.test_result = Result('origin', 'message', diffs=self.diff_dict)
        self.section = Section('name')
        self.section.append(Setting('no_color', 'True'))

    def test_is_applicable(self):
        diff = Diff([], rename='new_name')
        result = Result('', '', diffs={'f': diff})

        self.assertTrue(self.uut.is_applicable(result, {}, {'f': diff}))

    def test_apply(self):
        with prepare_file(['fixme   '], None) as (lines, filename):
            dir_path = os.path.dirname(filename)
            file_path = os.path.basename(filename)
            newfilename = os.path.join(dir_path, file_path + '.py')
            os.rename(filename, newfilename)
            file_dict = {newfilename: ['fixme   ']}
            diff_dict = {newfilename: Diff(file_dict[newfilename])}
            diff_dict[newfilename].add_line(1, ['test\n'])
            test_result = Result('origin', 'message', diffs=diff_dict)
            section = Section('name')
            section.append(Setting('no_color', 'True'))
            with simulate_console_inputs('1', 'True', '0') as generator:
                with retrieve_stdout() as stdout:
                    self.uut.apply_from_section(test_result, file_dict, {},
                                                section)
                    self.assertIn('[    ] *0. Do Nothing\n'
                                  '[    ]  1. Apply patch '
                                  '(\'SpaceConsistencyBear\')\n'
                                  '[    ]', stdout.getvalue())
                    os.rename(newfilename, filename)

    def test_apply_no_input(self):
        with retrieve_stdout() as stdout:
            with simulate_console_inputs('', '0') as generator:
                self.assertEqual(self.uut.apply_from_section(self.test_result,
                                                             self.file_dict,
                                                             {},
                                                             self.section),
                                 False)
