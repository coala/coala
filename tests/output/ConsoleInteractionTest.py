import os
import unittest
from unittest.mock import patch
from collections import OrderedDict
from os.path import abspath, relpath
import logging

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.Bear import Bear
from coala_utils.ContextManagers import (
    make_temp, retrieve_stdout, simulate_console_inputs)
from coalib.output.ConsoleInteraction import (
    acquire_actions_and_apply, acquire_settings, get_action_info, nothing_done,
    print_affected_files, print_result, print_results,
    print_results_formatted, print_results_no_input, print_section_beginning,
    show_bear, show_bears, ask_for_action_and_apply, print_diffs_info,
    show_language_bears_capabilities)
from coalib.output.ConsoleInteraction import (BackgroundSourceRangeStyle,
                                              BackgroundMessageStyle,
                                              highlight_text)
from coalib.output.printers.ListLogPrinter import ListLogPrinter
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.SourceRange import SourceRange
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting

from pygments.filters import VisibleWhitespaceFilter
from pygments.lexers import TextLexer


STR_GET_VAL_FOR_SETTING = ('Please enter a value for the setting \"{}\" ({}) '
                           'needed by {}: ')
STR_LINE_DOESNT_EXIST = ('The line belonging to the following result '
                         'cannot be printed because it refers to a line '
                         "that doesn't seem to exist in the given file.")
STR_PROJECT_WIDE = 'Project wide:'


class TestAction(ResultAction):

    def apply(self, result, original_file_dict, file_diff_dict, param):
        pass


class TestBear(Bear):

    CAN_DETECT = {'Formatting'}
    CAN_FIX = {'Formatting'}
    LANGUAGES = list(sorted({'F#', 'Shakespearean Programming Language'}))

    def run(self, setting1, setting2: int=None):
        """
        Test bear Description.

        :param setting1: Required Setting.
        :param setting2: Optional Setting.
        """
        return None


class TestBear2(Bear):

    LANGUAGES = {'TestLanguage'}

    def run(self, setting1):
        """
        Test bear 2 description.

        :param setting1: Required Setting.
        """
        return None


class SomeBear(Bear):

    def run(self):
        """
        Some Description.
        """
        return None


class SomeOtherBear(Bear):

    def run(self, setting: int=None):
        """
        This is a Bear.
        :param setting: This is an optional setting.
        """
        return None


class SomeglobalBear(Bear):

    def run(self):
        """
        Some global-bear Description.
        """
        return None


class SomelocalBear(Bear):

    def run(self):
        """
        Some local-bear Description.
        """
        return None


class ConsoleInteractionTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = ListLogPrinter()
        self.console_printer = ConsolePrinter(print_colored=False)
        self.no_color = not self.console_printer.print_colored
        self.file_diff_dict = {}
        self.section = Section('t')
        self.local_bears = OrderedDict([('default', [SomelocalBear]),
                                        ('test', [SomelocalBear])])
        self.global_bears = OrderedDict([('default', [SomeglobalBear]),
                                         ('test', [SomeglobalBear])])

        self.old_open_editor_applicable = OpenEditorAction.is_applicable
        OpenEditorAction.is_applicable = staticmethod(
            lambda *args: 'OpenEditorAction cannot be applied')

        self.old_apply_patch_applicable = ApplyPatchAction.is_applicable
        ApplyPatchAction.is_applicable = staticmethod(
            lambda *args: 'ApplyPatchAction cannot be applied')

        self.lexer = TextLexer()
        self.lexer.add_filter(VisibleWhitespaceFilter(
            spaces=True,
            tabs=True,
            tabsize=SpacingHelper.DEFAULT_TAB_WIDTH))

    def tearDown(self):
        OpenEditorAction.is_applicable = self.old_open_editor_applicable
        ApplyPatchAction.is_applicable = self.old_apply_patch_applicable

    def test_require_settings(self):
        curr_section = Section('')
        self.assertRaises(TypeError, acquire_settings,
                          self.log_printer, 0, curr_section)

        with simulate_console_inputs(0, 1, 2) as generator:
            self.assertEqual(acquire_settings(self.log_printer,
                                              {'setting': ['help text',
                                                           'SomeBear']},
                                              curr_section),
                             {'setting': 0})

            self.assertEqual(acquire_settings(self.log_printer,
                                              {'setting': ['help text',
                                                           'SomeBear',
                                                           'AnotherBear']},
                                              curr_section),
                             {'setting': 1})

            self.assertEqual(acquire_settings(self.log_printer,
                                              {'setting': ['help text',
                                                           'SomeBear',
                                                           'AnotherBear',
                                                           'YetAnotherBear']},
                                              curr_section),
                             {'setting': 2})

            self.assertEqual(generator.last_input, 2)

    def test_print_diffs_info(self):
        file_dict = {'a': ['a\n', 'b\n', 'c\n'], 'b': ['old_first\n']}
        diff_dict = {'a': Diff(file_dict['a']),
                     'b': Diff(file_dict['b'])}
        diff_dict['a'].add_lines(1, ['test\n'])
        diff_dict['a'].delete_line(3)
        diff_dict['b'].add_lines(0, ['first\n'])
        previous_diffs = {'a': Diff(file_dict['a'])}
        previous_diffs['a'].change_line(2, 'b\n', 'b_changed\n')
        with retrieve_stdout() as stdout:
            print_diffs_info(diff_dict, self.console_printer)
            self.assertEqual(stdout.getvalue(),
                             '|    | +1 -1 in a\n'
                             '|    | +1 -0 in b\n')

    @patch('coalib.output.ConsoleInteraction.acquire_actions_and_apply')
    @patch('coalib.output.ConsoleInteraction.ShowPatchAction.'
           'apply_from_section')
    def test_print_result_interactive_small_patch(self, apply_from_section, _):
        file_dict = {'a': ['a\n', 'b\n', 'c\n'], 'b': ['old_first\n']}
        diff_dict = {'a': Diff(file_dict['a']),
                     'b': Diff(file_dict['b'])}
        diff_dict['a'].add_lines(1, ['test\n'])
        diff_dict['a'].delete_line(3)
        result = Result('origin', 'msg', diffs=diff_dict)
        section = Section('test')

        print_result(self.console_printer,
                     section,
                     self.file_diff_dict,
                     result,
                     file_dict,
                     True)
        apply_from_section.assert_called_once_with(
            result, file_dict, self.file_diff_dict, section)

    @patch('coalib.output.ConsoleInteraction.acquire_actions_and_apply')
    @patch('coalib.output.ConsoleInteraction.print_diffs_info')
    def test_print_result_interactive_big_patch(self, diffs_info, _):
        file_dict = {'a': ['a\n', 'b\n', 'c\n'], 'b': ['old_first\n']}
        diff_dict = {'a': Diff(file_dict['a']),
                     'b': Diff(file_dict['b'])}
        diff_dict['a'].add_lines(1, ['test\n', 'test1\n', 'test2\n'])
        diff_dict['a'].delete_line(3)
        diff_dict['a'].add_lines(3, ['3test\n'])
        result = Result('origin', 'msg', diffs=diff_dict)
        section = Section('test')

        print_result(self.console_printer,
                     section,
                     self.file_diff_dict,
                     result,
                     file_dict,
                     True)
        diffs_info.assert_called_once_with(diff_dict, self.console_printer)

    def test_print_result(self):
        print_result(self.console_printer,
                     None,
                     self.file_diff_dict,
                     'illegal value',
                     {})

        with simulate_console_inputs(0):
            print_result(self.console_printer,
                         self.section,
                         self.file_diff_dict,
                         Result('origin', 'msg', diffs={}),
                         {})

        with make_temp() as testfile_path:
            file_dict = {
                testfile_path: ['1\n', '2\n', '3\n'],
                'f_b': ['1', '2', '3']
            }
            diff = Diff(file_dict[testfile_path])
            diff.delete_line(2)
            diff.change_line(3, '3\n', '3_changed\n')

            ApplyPatchAction.is_applicable = staticmethod(
                lambda *args: True)

            # Interaction must be closed by the user with `0` if it's not a
            # param
            with simulate_console_inputs('INVALID',
                                         -1,
                                         1,
                                         0,
                                         3) as input_generator:
                curr_section = Section('')
                print_section_beginning(self.console_printer, curr_section)
                print_result(self.console_printer,
                             curr_section,
                             self.file_diff_dict,
                             Result('origin', 'msg', diffs={
                                    testfile_path: diff}),
                             file_dict)
                self.assertEqual(input_generator.last_input, 3)

                self.file_diff_dict.clear()

                with open(testfile_path) as f:
                    self.assertEqual(f.readlines(), ['1\n', '3_changed\n'])

                os.remove(testfile_path + '.orig')

                name, section = get_action_info(curr_section,
                                                TestAction().get_metadata(),
                                                failed_actions=set())
                self.assertEqual(input_generator.last_input, 4)
                self.assertEqual(str(section), " {param : '3'}")
                self.assertEqual(name, 'TestAction')

        # Check if the user is asked for the parameter only the first time.
        # Use OpenEditorAction that needs this parameter (editor command).
        with simulate_console_inputs(1, 'test_editor', 0, 1, 0) as generator:
            OpenEditorAction.is_applicable = staticmethod(lambda *args: True)

            patch_result = Result('origin', 'msg', diffs={testfile_path: diff})
            patch_result.file = 'f_b'

            print_result(self.console_printer,
                         curr_section,
                         self.file_diff_dict,
                         patch_result,
                         file_dict)
            # choose action, choose editor, choose no action (-1 -> 2)
            self.assertEqual(generator.last_input, 2)

            # It shoudn't ask for parameter again
            print_result(self.console_printer,
                         curr_section,
                         self.file_diff_dict,
                         patch_result,
                         file_dict)
            self.assertEqual(generator.last_input, 4)

    def test_print_affected_files(self):
        with retrieve_stdout() as stdout, \
                make_temp() as some_file:
            file_dict = {some_file: ['1\n', '2\n', '3\n']}
            affected_code = (SourceRange.from_values(some_file),)
            print_affected_files(self.console_printer,
                                 self.log_printer,
                                 Result('origin',
                                        'message',
                                        affected_code=affected_code),
                                 file_dict)
            self.assertEqual(stdout.getvalue(),
                             '\n'+relpath(some_file)+'\n')

    def test_acquire_actions_and_apply(self):
        with make_temp() as testfile_path:
            file_dict = {testfile_path: ['1\n', '2\n', '3\n']}
            diff = Diff(file_dict[testfile_path])
            diff.delete_line(2)
            diff.change_line(3, '3\n', '3_changed\n')
            with simulate_console_inputs(1, 0) as generator, \
                    retrieve_stdout() as sio:
                ApplyPatchAction.is_applicable = staticmethod(
                    lambda *args: True)
                acquire_actions_and_apply(self.console_printer,
                                          Section(''),
                                          self.file_diff_dict,
                                          Result('origin', 'message', diffs={
                                              testfile_path: diff}),
                                          file_dict)
                self.assertEqual(generator.last_input, 1)
                self.assertIn(ApplyPatchAction.SUCCESS_MESSAGE, sio.getvalue())

            class InvalidateTestAction(ResultAction):

                is_applicable = staticmethod(lambda *args: True)

                def apply(*args, **kwargs):
                    ApplyPatchAction.is_applicable = staticmethod(
                        lambda *args: 'ApplyPatchAction cannot be applied.')

            old_applypatch_is_applicable = ApplyPatchAction.is_applicable
            ApplyPatchAction.is_applicable = staticmethod(lambda *args: True)
            cli_actions = [ApplyPatchAction(), InvalidateTestAction()]

            with simulate_console_inputs(2, 1, 0) as generator, \
                    retrieve_stdout() as sio:
                acquire_actions_and_apply(self.console_printer,
                                          Section(''),
                                          self.file_diff_dict,
                                          Result('origin', 'message',
                                                 diffs={testfile_path: diff}),
                                          file_dict,
                                          cli_actions=cli_actions)
                self.assertEqual(generator.last_input, 2)

                action_fail = 'Failed to execute the action'
                self.assertNotIn(action_fail, sio.getvalue())

                apply_path_desc = ApplyPatchAction().get_metadata().desc
                self.assertEqual(sio.getvalue().count(apply_path_desc), 1)

            ApplyPatchAction.is_applicable = old_applypatch_is_applicable

    def test_ask_for_actions_and_apply(self):
        failed_actions = set()
        action = TestAction()
        args = [self.console_printer, Section(''),
                [action.get_metadata()], {'TestAction': action},
                failed_actions, Result('origin', 'message'), {}, {}]

        with simulate_console_inputs(1, 'param1', 1, 'param2') as generator:
            action.apply = unittest.mock.Mock(side_effect=AssertionError)
            ask_for_action_and_apply(*args)
            self.assertEqual(generator.last_input, 1)
            self.assertIn('TestAction', failed_actions)

            action.apply = lambda *args, **kwargs: {}
            ask_for_action_and_apply(*args)
            self.assertEqual(generator.last_input, 3)
            self.assertNotIn('TestAction', failed_actions)

    def test_default_input(self):
        action = TestAction()
        args = [self.console_printer, Section(''),
                [action.get_metadata()], {'TestAction': action},
                set(), Result('origin', 'message'), {}, {}]

        with simulate_console_inputs('') as generator:
            self.assertFalse(ask_for_action_and_apply(*args))

    def test_print_result_no_input(self):
        with make_temp() as testfile_path:
            file_dict = {testfile_path: ['1\n', '2\n', '3\n']}
            diff = Diff(file_dict[testfile_path])
            diff.delete_line(2)
            diff.change_line(3, '3\n', '3_changed\n')
            with simulate_console_inputs(1, 2, 3) as generator, \
                    retrieve_stdout() as stdout:
                ApplyPatchAction.is_applicable = staticmethod(
                    lambda *args: True)
                print_results_no_input(self.log_printer,
                                       Section('someSection'),
                                       [Result('origin', 'message', diffs={
                                           testfile_path: diff})],
                                       file_dict,
                                       self.file_diff_dict,
                                       self.console_printer)
                self.assertEqual(generator.last_input, -1)
                self.assertEqual(stdout.getvalue(),
                                 """
Project wide:
|    | [NORMAL] origin:
|    | {}\n""".format(highlight_text(self.no_color,
                                     'message', style=BackgroundMessageStyle)))

    def test_print_section_beginning(self):
        with retrieve_stdout() as stdout:
            print_section_beginning(self.console_printer, Section('name'))
            self.assertEqual(stdout.getvalue(), 'Executing section name...\n')

    def test_nothing_done(self):
        nothing_done(self.log_printer)
        self.assertEqual(['No existent section was targeted or enabled. '
                          'Nothing to do.'],
                         [log.message for log in self.log_printer.logs])

    def test_print_results_empty(self):
        with retrieve_stdout() as stdout:
            print_results(self.log_printer, Section(''), [], {}, {},
                          self.console_printer)
            self.assertEqual(stdout.getvalue(), '')

    def test_print_results_project_wide(self):
        with retrieve_stdout() as stdout:
            print_results(self.log_printer,
                          Section(''),
                          [Result('origin', 'message')],
                          {},
                          {},
                          self.console_printer)
            self.assertEqual(
                '\n{}\n|    | [NORMAL] origin:\n|    | {}\n'.format(
                    STR_PROJECT_WIDE,
                    highlight_text(self.no_color,
                                   'message', style=BackgroundMessageStyle)),
                stdout.getvalue())

    def test_print_results_for_file(self):
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(''),
                [Result.from_values('SpaceConsistencyBear',
                                    'Trailing whitespace found',
                                    file='filename',
                                    line=2)],
                {abspath('filename'): ['test line\n', 'line 2\n', 'line 3\n']},
                {},
                self.console_printer)
            self.assertEqual("""\nfilename
|   2| {}
|    | [NORMAL] SpaceConsistencyBear:
|    | {}\n""".format(highlight_text(self.no_color, 'line 2', self.lexer),
                      highlight_text(self.no_color, 'Trailing whitespace found',
                                     style=BackgroundMessageStyle)),
                stdout.getvalue())

        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(''),
                [Result.from_values('SpaceConsistencyBear',
                                    'Trailing whitespace found',
                                    file='filename',
                                    line=5)],
                {abspath('filename'): ['test line\n',
                                       'line 2\n',
                                       'line 3\n',
                                       'line 4\n',
                                       'line 5\n']},
                {},
                self.console_printer)
            self.assertEqual("""\nfilename
|   5| {}
|    | [NORMAL] SpaceConsistencyBear:
|    | {}\n""".format(highlight_text(self.no_color, 'line 5', self.lexer),
                      highlight_text(self.no_color, 'Trailing whitespace found',
                                     style=BackgroundMessageStyle)),
                stdout.getvalue())

    def test_print_results_sorting(self):
        with retrieve_stdout() as stdout:
            print_results(self.log_printer,
                          Section(''),
                          [Result.from_values('SpaceConsistencyBear',
                                              'Trailing whitespace found',
                                              file='file',
                                              line=5),
                           Result.from_values('SpaceConsistencyBear',
                                              'Trailing whitespace found',
                                              file='file',
                                              line=2)],
                          {abspath('file'): ['test line\n',
                                             '\t\n',
                                             'line 3\n',
                                             'line 4\n',
                                             'line 5\t\n']},
                          {},
                          self.console_printer)

            self.assertEqual("""
file
|   2| {0}
|    | [NORMAL] SpaceConsistencyBear:
|    | {1}

file
|   5| {2}
|    | [NORMAL] SpaceConsistencyBear:
|    | {1}\n""".format(highlight_text(self.no_color, '\t', self.lexer),
                       highlight_text(self.no_color,
                                      'Trailing whitespace found',
                                      style=BackgroundMessageStyle),
                       highlight_text(self.no_color, 'line 5\t', self.lexer)),
                stdout.getvalue())

    def test_print_results_multiple_ranges(self):
        affected_code = (
            SourceRange.from_values('some_file', 5, end_line=7),
            SourceRange.from_values('another_file', 1, 3, 1, 5),
            SourceRange.from_values('another_file', 3, 3, 3, 5))
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(''),
                [Result('ClangCloneDetectionBear',
                        'Clone Found',
                        affected_code)],
                {abspath('some_file'): ['line ' + str(i + 1) + '\n'
                                        for i in range(10)],
                 abspath('another_file'): ['line ' + str(i + 1)
                                           for i in range(10)]},
                {},
                self.console_printer)
            self.assertEqual("""
another_file
|   1| li{0}{1}

another_file
|   3| li{0}{2}

some_file
|   5| {3}
|   6| {4}
|   7| {5}
|    | [NORMAL] ClangCloneDetectionBear:
|    | {6}\n""".format(highlight_text(self.no_color, 'ne', self.lexer,
                                      BackgroundSourceRangeStyle),
                       highlight_text(self.no_color, ' 1', self.lexer),
                       highlight_text(self.no_color, ' 3', self.lexer),
                       highlight_text(self.no_color, 'line 5', self.lexer),
                       highlight_text(self.no_color, 'line 6', self.lexer),
                       highlight_text(self.no_color, 'line 7', self.lexer),
                       highlight_text(self.no_color, 'Clone Found',
                                      style=BackgroundMessageStyle)),
                stdout.getvalue())

    def test_print_results_missing_file(self):
        self.log_printer.log_level = logging.CRITICAL
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(''),
                [Result('t', 'msg'),
                 Result.from_values('t', 'msg', file='file', line=5)],
                {},
                {},
                self.console_printer)
            self.assertEqual('\n' + STR_PROJECT_WIDE + '\n'
                             '|    | [NORMAL] t:\n'
                             '|    | {0}\n'
                             # Second results file isn't there, no context is
                             # printed, only a warning log message which we
                             # don't catch
                             '|    | [NORMAL] t:\n'
                             '|    | {0}\n'.format(
                                 highlight_text(self.no_color, 'msg',
                                                style=BackgroundMessageStyle)),
                             stdout.getvalue())

    def test_print_results_missing_line(self):
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(''),
                [Result.from_values('t', 'msg', file='file', line=5),
                 Result.from_values('t', 'msg', file='file', line=6)],
                {abspath('file'): ['line ' + str(i + 1) for i in range(5)]},
                {},
                self.console_printer)
            self.assertEqual('\n'
                             'file\n'
                             '|   5| {0}\n'
                             '|    | [NORMAL] t:\n'
                             '|    | {1}\n'
                             '\n'
                             'file\n'
                             '|   6| {2}\n'
                             '|    | [NORMAL] t:\n'
                             '|    | {1}\n'.format(
                                 highlight_text(self.no_color,
                                                'line 5', self.lexer),
                                 highlight_text(self.no_color, 'msg',
                                                style=BackgroundMessageStyle),
                                 STR_LINE_DOESNT_EXIST),
                             stdout.getvalue())

    def test_print_results_without_line(self):
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(''),
                [Result.from_values('t', 'msg', file='file')],
                {abspath('file'): []},
                {},
                self.console_printer)
            self.assertEqual(
                '\nfile\n'
                '|    | [NORMAL] t:\n'
                '|    | {}\n'.format(highlight_text(
                   self.no_color, 'msg', style=BackgroundMessageStyle)),
                stdout.getvalue())


class ShowBearsTest(unittest.TestCase):

    def setUp(self):
        self.console_printer = ConsolePrinter(print_colored=False)

    def test_show_bear_minimal(self):
        with retrieve_stdout() as stdout:
            show_bear(
                SomelocalBear, False, False, self.console_printer)
            self.assertEqual(stdout.getvalue(), 'SomelocalBear\n')

    def test_show_bear_desc_only(self):
        with retrieve_stdout() as stdout:
            show_bear(
                SomelocalBear, True, False, self.console_printer)
            self.assertEqual(
                stdout.getvalue(),
                'SomelocalBear\n  Some local-bear Description.\n\n')

    def test_show_bear_details_only(self):
        with retrieve_stdout() as stdout:
            show_bear(
                SomelocalBear, False, True, self.console_printer)
            self.assertEqual(stdout.getvalue(),
                             'SomelocalBear\n'
                             '  The bear does not provide information about '
                             'which languages it can analyze.\n\n'
                             '  No needed settings.\n\n'
                             '  No optional settings.\n\n'
                             '  This bear does not provide information about '
                             'what categories it can detect.\n\n'
                             '  This bear cannot fix issues or does not '
                             'provide information about what categories it '
                             'can fix.\n\n  Path:\n   ' +
                             repr(SomelocalBear.source_location) + '\n\n')

    def test_show_bear_long_without_content(self):
        with retrieve_stdout() as stdout:
            show_bear(
                SomelocalBear, True, True, self.console_printer)
            self.assertEqual(stdout.getvalue(),
                             'SomelocalBear\n'
                             '  Some local-bear Description.\n\n'
                             '  The bear does not provide information about '
                             'which languages it can analyze.\n\n'
                             '  No needed settings.\n\n'
                             '  No optional settings.\n\n'
                             '  This bear does not provide information about '
                             'what categories it can detect.\n\n'
                             '  This bear cannot fix issues or does not '
                             'provide information about what categories it '
                             'can fix.\n\n  Path:\n   ' +
                             repr(SomelocalBear.source_location) + '\n\n')

    def test_show_bear_with_content(self):
        with retrieve_stdout() as stdout:
            show_bear(TestBear, True, True, self.console_printer)
            self.assertEqual(stdout.getvalue(),
                             'TestBear\n'
                             '  Test bear Description.\n\n'
                             '  Supported languages:\n'
                             '   * F#\n'
                             '   * Shakespearean Programming Language\n\n'
                             '  Needed Settings:\n'
                             '   * setting1: Required Setting.\n\n'
                             '  Optional Settings:\n'
                             '   * setting2: Optional Setting. ('
                             "Optional, defaults to 'None'."
                             ')\n\n'
                             '  Can detect:\n   * Formatting\n\n'
                             '  Can fix:\n   * Formatting\n\n  Path:\n   ' +
                             repr(TestBear.source_location) + '\n\n')

    def test_show_bears_empty(self):
        with retrieve_stdout() as stdout:
            show_bears({}, {}, True, True, self.console_printer)
            self.assertIn('No bears to show.', stdout.getvalue())

    @patch('coalib.output.ConsoleInteraction.show_bear')
    def test_show_bears(self, show_bear):
        local_bears = OrderedDict([('default', [SomelocalBear]),
                                   ('test', [SomelocalBear])])
        show_bears(local_bears, {}, True, True, self.console_printer)
        show_bear.assert_called_once_with(SomelocalBear,
                                          True,
                                          True,
                                          self.console_printer)

    def test_show_bears_capabilities(self):
        with retrieve_stdout() as stdout:
            show_language_bears_capabilities(
                {'some_language': ({'Formatting', 'Security'}, {'Formatting'})},
                self.console_printer)
            self.assertIn('coala can do the following for SOME_LANGUAGE\n'
                          '    Can detect only: Formatting, Security\n'
                          '    Can fix        : Formatting\n',
                          stdout.getvalue())
            show_language_bears_capabilities(
                {'some_language': (set(), set())}, self.console_printer)
            self.assertIn('coala does not support some_language',
                          stdout.getvalue())
            show_language_bears_capabilities(
                {}, self.console_printer)
            self.assertIn(
                'There is no bear available for this language',
                stdout.getvalue())
            show_language_bears_capabilities(
                {'some_language': ({'Formatting', 'Security'}, set())},
                self.console_printer)
            self.assertIn('coala can do the following for SOME_LANGUAGE\n'
                          '    Can detect only: Formatting, Security\n',
                          stdout.getvalue())
# Own test because this is easy and not tied to the rest


class PrintFormattedResultsTest(unittest.TestCase):

    def setUp(self):
        self.logger = ListLogPrinter()
        self.section = Section('t')

    def test_default_format(self):
        expected_string = ('id:-?[0-9]+:origin:1:file:None:line:None:'
                           'column:None:end_line:None:end_column:None:'
                           'severity:1:severity_str:NORMAL:message:2\n')
        with retrieve_stdout() as stdout:
            print_results_formatted(self.logger,
                                    self.section,
                                    [Result('1', '2')],
                                    None,
                                    None)
            self.assertRegex(stdout.getvalue(), expected_string)

        self.section.append(Setting('format', 'True'))
        with retrieve_stdout() as stdout:
            print_results_formatted(self.logger,
                                    self.section,
                                    [Result('1', '2')],
                                    None,
                                    None)
            self.assertRegex(stdout.getvalue(), expected_string)

    def test_multiple_ranges(self):
        expected_string = (
            'id:-?[0-9]+:origin:1:.*file:.*another_file:line:5:'
            'column:3:end_line:5:end_column:5:'
            'severity:1:severity_str:NORMAL:message:2\n'
            'id:-?[0-9]+:origin:1:.*file:.*some_file:line:5:'
            'column:None:end_line:7:end_column:None:'
            'severity:1:severity_str:NORMAL:message:2\n')
        affected_code = (SourceRange.from_values('some_file', 5, end_line=7),
                         SourceRange.from_values('another_file', 5, 3, 5, 5))
        with retrieve_stdout() as stdout:
            print_results_formatted(self.logger,
                                    self.section,
                                    [Result('1', '2', affected_code)],
                                    None,
                                    None)
            self.assertRegex(stdout.getvalue(), expected_string)

    def test_bad_format(self):
        self.section.append(Setting('format', '{nonexistant}'))
        print_results_formatted(self.logger,
                                self.section,
                                [Result('1', '2')],
                                None,
                                None)
        self.assertRegex(''.join(log.message for log in self.logger.logs),
                         '.*Unable to print.*')

    def test_good_format(self):
        self.section.append(Setting('format', '{origin}'))
        with retrieve_stdout() as stdout:
            print_results_formatted(self.logger,
                                    self.section,
                                    [Result('1', '2')],
                                    None,
                                    None)
            self.assertEqual(stdout.getvalue(), '1\n')

    def test_empty_list(self):
        self.section.append(Setting('format', '{origin}'))
        # Shouldn't attempt to format the string None and will fail badly if
        # its done wrong.
        print_results_formatted(None,
                                self.section,
                                [],
                                None,
                                None,
                                None)
