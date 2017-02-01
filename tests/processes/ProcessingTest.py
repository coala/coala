import multiprocessing
import os
import platform
import queue
import re
import subprocess
import sys
import unittest

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.output.printers.LogPrinter import LogPrinter
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.processes.Processing import (
    ACTIONS, autoapply_actions, check_result_ignore, create_process_group,
    execute_section, filter_raising_callables, get_default_actions,
    get_file_dict, print_result, process_queues, simplify_section_result,
    yield_ignore_ranges)
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.PrintDebugMessageAction import (
    PrintDebugMessageAction)
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.SourceRange import SourceRange
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.misc.Caching import FileCache


process_group_test_code = """
import time, subprocess, os, platform, sys;
p=subprocess.Popen([sys.executable,
                  "-c",
                  "import time; time.sleep(0.1)"]);
pgid = p.pid if platform.system() == "Windows" else os.getpgid(p.pid);
print(p.pid, pgid)
p.terminate()
"""


class DummyProcess(multiprocessing.Process):

    def __init__(self, control_queue, starts_dead=False):
        multiprocessing.Process.__init__(self)
        self.control_queue = control_queue
        self.starts_dead = starts_dead

    def is_alive(self):
        return not self.control_queue.empty() and not self.starts_dead


class ProcessingTestLogPrinter(LogPrinter):

    def __init__(self, log_queue):
        LogPrinter.__init__(self, self)
        self.log_queue = log_queue
        self.set_up = False

    def log_message(self, log_message, timestamp=None, **kwargs):
        self.log_queue.put(log_message)


class ProcessingTest(unittest.TestCase):

    def setUp(self):
        config_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'section_executor_test_files',
            '.coafile'))
        self.testcode_c_path = os.path.join(os.path.dirname(config_path),
                                            'testcode.c')

        self.result_queue = queue.Queue()
        self.queue = queue.Queue()
        self.log_queue = queue.Queue()
        self.console_printer = ConsolePrinter()
        log_printer = LogPrinter(ConsolePrinter())
        self.log_printer = ProcessingTestLogPrinter(self.log_queue)

        (self.sections,
         self.local_bears,
         self.global_bears,
         targets) = gather_configuration(lambda *args: True,
                                         log_printer,
                                         arg_list=['--config',
                                                   re.escape(config_path)])
        self.assertEqual(len(self.local_bears['cli']), 1)
        self.assertEqual(len(self.global_bears['cli']), 1)
        self.assertEqual(targets, [])

    def test_run(self):
        self.sections['cli'].append(Setting('jobs', '1'))
        cache = FileCache(self.log_printer, 'coala_test', flush_cache=True)
        results = execute_section(self.sections['cli'],
                                  self.global_bears['cli'],
                                  self.local_bears['cli'],
                                  lambda *args: self.result_queue.put(args[2]),
                                  cache,
                                  self.log_printer,
                                  console_printer=self.console_printer)
        self.assertTrue(results[0])

        local_results = self.result_queue.get(timeout=0)
        global_results = self.result_queue.get(timeout=0)
        self.assertTrue(self.result_queue.empty())

        self.assertEqual(len(local_results), 1)
        self.assertEqual(len(global_results), 1)
        # Result dict also returned
        # One file
        self.assertEqual(len(results[1]), 1)
        # One global bear
        self.assertEqual(len(results[2]), 1)

        local_result = local_results[0]
        global_result = global_results[0]

        self.assertRegex(repr(local_result),
                         "<Result object\\(id={}, origin='LocalTestBear', aff"
                         'ected_code=\\(\\), severity=NORMAL, confidence=100'
                         ", message='test msg', aspect=NoneType\\) at "
                         '0x[0-9a-fA-F]+>'.format(hex(local_result.id)))
        self.assertRegex(repr(global_result),
                         "<Result object\\(id={}, origin='GlobalTestBear', "
                         'affected_code=\\(.*start=.*file=.*section_executor_'
                         'test_files.*line=None.*end=.*\\), severity=NORMAL, c'
                         "onfidence=100, message='test message', "
                         'aspect=NoneType\\'
                         ') at 0x[0-9a-fA-F]+>'.format(hex(global_result.id)))

    def test_empty_run(self):
        execute_section(self.sections['cli'],
                        [],
                        [],
                        lambda *args: self.result_queue.put(args[2]),
                        None,
                        self.log_printer,
                        console_printer=self.console_printer)
        self.sections['cli'].append(Setting('jobs', 'bogus!'))
        results = execute_section(self.sections['cli'],
                                  [],
                                  [],
                                  lambda *args: self.result_queue.put(args[2]),
                                  None,
                                  self.log_printer,
                                  console_printer=self.console_printer)
        # No results
        self.assertFalse(results[0])
        # One file
        self.assertEqual(len(results[1]), 1)
        # No global bear
        self.assertEqual(len(results[2]), 0)

    def test_process_queues(self):
        ctrlq = queue.Queue()

        # Append custom controlling sequences.

        # Simulated process 1
        ctrlq.put((CONTROL_ELEMENT.LOCAL, 1))
        ctrlq.put((CONTROL_ELEMENT.LOCAL_FINISHED, None))
        ctrlq.put((CONTROL_ELEMENT.GLOBAL, 1))

        # Simulated process 2
        ctrlq.put((CONTROL_ELEMENT.LOCAL, 2))

        # Simulated process 1
        ctrlq.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))

        # Simulated process 2
        ctrlq.put((CONTROL_ELEMENT.LOCAL_FINISHED, None))
        ctrlq.put((CONTROL_ELEMENT.GLOBAL, 1))
        ctrlq.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))

        first_local = Result.from_values('o', 'The first result.', file='f')
        second_local = Result.from_values('ABear',
                                          'The second result.',
                                          file='f',
                                          line=1)
        third_local = Result.from_values('ABear',
                                         'The second result.',
                                         file='f',
                                         line=4)
        fourth_local = Result.from_values('ABear',
                                          'Another result.',
                                          file='f',
                                          line=7)
        first_global = Result('o', 'The one and only global result.')
        section = Section('')
        section.append(Setting('min_severity', 'normal'))
        process_queues(
            [DummyProcess(control_queue=ctrlq) for i in range(3)],
            ctrlq,
            {1: [first_local,
                 second_local,
                 third_local,
                 # The following are to be ignored
                 Result('o', 'm', severity=RESULT_SEVERITY.INFO),
                 Result.from_values('ABear', 'u', 'f', 2, 1),
                 Result.from_values('ABear', 'u', 'f', 3, 1)],
             2: [fourth_local,
                 # The following are to be ignored
                 HiddenResult('t', 'c'),
                 Result.from_values('ABear', 'u', 'f', 5, 1),
                 Result.from_values('ABear', 'u', 'f', 6, 1)]},
            {1: [first_global]},
            {'f': ['first line  # stop ignoring, invalid ignore range\n',
                   'second line  # ignore all\n',
                   'third line\n',
                   "fourth line  # gnore shouldn't trigger without i!\n",
                   '# Start ignoring ABear, BBear and CBear\n',
                   '# Stop ignoring\n',
                   'seventh']},
            lambda *args: self.queue.put(args[2]),
            section,
            None,
            self.log_printer,
            self.console_printer)

        self.assertEqual(self.queue.get(timeout=0), ([first_local,
                                                      second_local,
                                                      third_local]))
        self.assertEqual(self.queue.get(timeout=0), ([fourth_local]))
        self.assertEqual(self.queue.get(timeout=0), ([first_global]))
        self.assertEqual(self.queue.get(timeout=0), ([first_global]))

    def test_dead_processes(self):
        ctrlq = queue.Queue()
        # Not enough FINISH elements in the queue, processes start already dead
        # Also queue elements are reversed
        ctrlq.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))
        ctrlq.put((CONTROL_ELEMENT.LOCAL_FINISHED, None))

        process_queues(
            [DummyProcess(ctrlq, starts_dead=True) for i in range(3)],
            ctrlq, {}, {}, {},
            lambda *args: self.queue.put(args[2]),
            Section(''),
            None,
            self.log_printer,
            self.console_printer)
        with self.assertRaises(queue.Empty):
            self.queue.get(timeout=0)

        # Not enough FINISH elements in the queue, processes start already dead
        ctrlq.put((CONTROL_ELEMENT.LOCAL_FINISHED, None))
        ctrlq.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))

        process_queues(
            [DummyProcess(ctrlq, starts_dead=True) for i in range(3)],
            ctrlq, {}, {}, {},
            lambda *args: self.queue.put(args[2]),
            Section(''),
            None,
            self.log_printer,
            self.console_printer)
        with self.assertRaises(queue.Empty):
            self.queue.get(timeout=0)

    def test_create_process_group(self):
        p = create_process_group([sys.executable,
                                  '-c',
                                  process_group_test_code],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        retval = p.wait()
        if retval != 0:
            for line in p.stderr:
                print(line, end='')
            raise Exception('Subprocess did not exit correctly')
        output = [i for i in p.stdout]
        p.stderr.close()
        p.stdout.close()
        pid, pgid = [int(i.strip()) for i_out in output for i in i_out.split()]
        if platform.system() != 'Windows':
            # There is no way of testing this on windows with the current
            # python modules subprocess and os
            self.assertEqual(p.pid, pgid)

    def test_filter_raising_callables(self):
        class A(Exception):
            pass

        class B(Exception):
            pass

        class C(Exception):
            pass

        def create_exception_raiser(exception):
            def raiser(exc):
                if exception in exc:
                    raise exception
                return exception
            return raiser

        raiseA, raiseB, raiseC = (create_exception_raiser(exc)
                                  for exc in [A, B, C])

        test_list = [raiseA, raiseC, raiseB, raiseC]
        self.assertEqual(list(filter_raising_callables(test_list, A, (A,))),
                         [C, B, C])

        self.assertEqual(list(filter_raising_callables(test_list,
                                                       (B, C),
                                                       exc=(B, C))),
                         [A])

        # Test whether non filtered exceptions bubble up.
        with self.assertRaises(B):
            list(filter_raising_callables(test_list, C, exc=(B, C)))

    def test_get_file_dict(self):
        file_dict = get_file_dict([self.testcode_c_path], self.log_printer)
        self.assertEqual(len(file_dict), 1)
        self.assertEqual(type(file_dict[self.testcode_c_path]),
                         tuple,
                         msg='files in file_dict should not be editable')
        self.assertEqual('Files that will be checked:\n' + self.testcode_c_path,
                         self.log_printer.log_queue.get().message)

    def test_get_file_dict_non_existent_file(self):
        file_dict = get_file_dict(['non_existent_file'], self.log_printer)
        self.assertEqual(file_dict, {})
        self.assertIn(("Failed to read file 'non_existent_file' because of "
                       'an unknown error.'),
                      self.log_printer.log_queue.get().message)

    def test_simplify_section_result(self):
        results = (True,
                   {'file1': [Result('a', 'b')], 'file2': None},
                   {'file3': [Result('a', 'c')]},
                   None)
        yielded, yielded_unfixed, all_results = simplify_section_result(results)
        self.assertEqual(yielded, True)
        self.assertEqual(yielded_unfixed, True)
        self.assertEqual(len(all_results), 2)

    def test_ignore_results(self):
        ranges = [([], SourceRange.from_values('f', 1, 1, 2, 2))]
        result = Result.from_values('origin (Something Specific)',
                                    'message',
                                    file='e',
                                    line=1,
                                    column=1,
                                    end_line=2,
                                    end_column=2)

        self.assertFalse(check_result_ignore(result, ranges))

        ranges.append(([], SourceRange.from_values('e', 2, 3, 3, 3)))
        self.assertFalse(check_result_ignore(result, ranges))

        ranges.append(([], SourceRange.from_values('e', 1, 1, 2, 2)))
        self.assertTrue(check_result_ignore(result, ranges))

        result1 = Result.from_values('origin', 'message', file='e')
        self.assertFalse(check_result_ignore(result1, ranges))

        ranges = [(['something', 'else', 'not origin'],
                   SourceRange.from_values('e', 1, 1, 2, 2))]
        self.assertFalse(check_result_ignore(result, ranges))

        ranges = [(['something', 'else', 'origin'],
                   SourceRange.from_values('e', 1, 1, 2, 2))]
        self.assertTrue(check_result_ignore(result, ranges))

    def test_ignore_glob(self):
        result = Result.from_values('LineLengthBear',
                                    'message',
                                    file='d',
                                    line=1,
                                    column=1,
                                    end_line=2,
                                    end_column=2)
        ranges = [(['(line*|space*)', 'py*'],
                   SourceRange.from_values('d', 1, 1, 2, 2))]
        self.assertTrue(check_result_ignore(result, ranges))

        result = Result.from_values('SpaceConsistencyBear',
                                    'message',
                                    file='d',
                                    line=1,
                                    column=1,
                                    end_line=2,
                                    end_column=2)
        ranges = [(['(line*|space*)', 'py*'],
                   SourceRange.from_values('d', 1, 1, 2, 2))]
        self.assertTrue(check_result_ignore(result, ranges))

        result = Result.from_values('XMLBear',
                                    'message',
                                    file='d',
                                    line=1,
                                    column=1,
                                    end_line=2,
                                    end_column=2)
        ranges = [(['(line*|space*)', 'py*'],
                   SourceRange.from_values('d', 1, 1, 2, 2))]
        self.assertFalse(check_result_ignore(result, ranges))

    def test_yield_ignore_ranges(self):
        test_file_dict_a = {'f':
                            ('# Ignore aBear\n',
                             'a_string = "This string should be ignored"\n')}
        test_ignore_range_a = list(yield_ignore_ranges(test_file_dict_a))
        for test_bears, test_source_range in test_ignore_range_a:
            self.assertEqual(test_bears, ['abear'])
            self.assertEqual(test_source_range.start.line, 1)
            self.assertEqual(test_source_range.start.column, 1)
            self.assertEqual(test_source_range.end.line, 2)
            self.assertEqual(test_source_range.end.column, 43)

        test_file_dict_b = {'f':
                            ('# start Ignoring bBear\n',
                             'b_string = "This string should be ignored"\n',
                             '# stop ignoring\n')}
        test_ignore_range_b = list(yield_ignore_ranges(test_file_dict_b))
        for test_bears, test_source_range in test_ignore_range_b:
            self.assertEqual(test_bears, ['bbear'])
            self.assertEqual(test_source_range.start.line, 1)
            self.assertEqual(test_source_range.start.column, 1)
            self.assertEqual(test_source_range.end.line, 3)
            self.assertEqual(test_source_range.end.column, 16)

        test_file_dict_c = {'f':
                            ('# Start ignoring cBear\n',
                             '# Stop ignoring cBear This & prev ignored\n')}
        test_ignore_range_c = list(yield_ignore_ranges(test_file_dict_c))
        for test_bears, test_source_range in test_ignore_range_c:
            self.assertEqual(test_bears, ['cbear'])
            self.assertEqual(test_source_range.start.line, 1)
            self.assertEqual(test_source_range.start.column, 1)
            self.assertEqual(test_source_range.end.line, 2)
            self.assertEqual(test_source_range.end.column, 42)

        test_file_dict_d = {'f':
                            ('# Start ignoring cBear\n',
                             'All of this ignored\n')}
        test_ignore_range_d = list(yield_ignore_ranges(test_file_dict_d))
        for test_bears, test_source_range in test_ignore_range_d:
            self.assertEqual(test_bears, ['cbear'])
            self.assertEqual(test_source_range.start.line, 1)
            self.assertEqual(test_source_range.start.column, 1)
            self.assertEqual(test_source_range.end.line, 2)
            self.assertEqual(test_source_range.end.column, 20)

        test_file_dict_e = {'f':
                            ('# Ignore all\n',
                             'e_string = "This string should be ignored"\n')}
        test_ignore_range_e = list(yield_ignore_ranges(test_file_dict_e))
        for test_bears, test_source_range in test_ignore_range_e:
            self.assertEqual(test_bears, [])
            self.assertEqual(test_source_range.start.line, 1)
            self.assertEqual(test_source_range.start.column, 1)
            self.assertEqual(test_source_range.end.line, 2)
            self.assertEqual(test_source_range.end.column, 43)

        test_file_dict_n = {'f':
                            ('# noqa nBear\n',
                             'n_string = "This string should be ignored"\n')}
        test_ignore_range_n = list(yield_ignore_ranges(test_file_dict_n))
        for test_bears, test_source_range in test_ignore_range_n:
            self.assertEqual(test_bears, ['nbear'])
            self.assertEqual(test_source_range.start.line, 1)
            self.assertEqual(test_source_range.start.column, 1)
            self.assertEqual(test_source_range.end.line, 2)
            self.assertEqual(test_source_range.end.column, 43)

        test_file_dict_n = {'f':
                            ('# noqa\n',
                             'n_string = "This string should be ignored"\n')}
        test_ignore_range_n = list(yield_ignore_ranges(test_file_dict_n))
        for test_bears, test_source_range in test_ignore_range_n:
            self.assertEqual(test_bears, [])
            self.assertEqual(test_source_range.start.line, 1)
            self.assertEqual(test_source_range.start.column, 1)
            self.assertEqual(test_source_range.end.line, 2)
            self.assertEqual(test_source_range.end.column, 43)

        # This case was a bug.
        test_file_dict_single_line = {'f': ('# ignore XBEAR',)}
        test_ignore_range_single_line = list(yield_ignore_ranges(
            test_file_dict_single_line))

        self.assertEqual(len(test_ignore_range_single_line), 1)
        bears, source_range = test_ignore_range_single_line[0]
        self.assertEqual(bears, ['xbear'])
        self.assertEqual(source_range.start.line, 1)
        self.assertEqual(source_range.start.column, 1)
        self.assertEqual(source_range.end.line, 1)
        self.assertEqual(source_range.end.column, 14)


class ProcessingTest_GetDefaultActions(unittest.TestCase):

    def setUp(self):
        self.section = Section('X')

    def test_no_key(self):
        self.assertEqual(get_default_actions(self.section), ({}, {}))

    def test_no_value(self):
        self.section.append(Setting('default_actions', ''))
        self.assertEqual(get_default_actions(self.section), ({}, {}))

    def test_only_valid_actions(self):
        self.section.append(Setting(
            'default_actions',
            'MyBear: PrintDebugMessageAction, ValidBear: ApplyPatchAction'))
        self.assertEqual(
            get_default_actions(self.section),
            ({'MyBear': PrintDebugMessageAction,
              'ValidBear': ApplyPatchAction},
             {}))

    def test_valid_and_invalid_actions(self):
        self.section.append(Setting(
            'default_actions',
            'MyBear: INVALID_action, ValidBear: ApplyPatchAction, XBear: ABC'))
        self.assertEqual(get_default_actions(self.section),
                         ({'ValidBear': ApplyPatchAction},
                          {'MyBear': 'INVALID_action', 'XBear': 'ABC'}))


class ProcessingTest_AutoapplyActions(unittest.TestCase):

    def setUp(self):
        self.log_queue = queue.Queue()
        self.log_printer = ProcessingTestLogPrinter(self.log_queue)

        self.resultY = Result('YBear', 'msg1')
        self.resultZ = Result('ZBear', 'msg2')
        self.results = [self.resultY, self.resultZ]
        self.section = Section('A')

    def test_no_default_actions(self):
        ret = autoapply_actions(self.results,
                                {},
                                {},
                                self.section,
                                self.log_printer)
        self.assertEqual(ret, self.results)
        self.assertTrue(self.log_queue.empty())

    def test_with_invalid_action(self):
        self.section.append(Setting('default_actions',
                                    'XBear: nonSENSE_action'))
        ret = autoapply_actions(self.results,
                                {},
                                {},
                                self.section,
                                self.log_printer)
        self.assertEqual(ret, self.results)
        self.assertEqual(self.log_queue.get().message,
                         "Selected default action 'nonSENSE_action' for bear "
                         "'XBear' does not exist. Ignoring action.")
        self.assertTrue(self.log_queue.empty())

    def test_without_default_action_and_unapplicable(self):
        # Use a result where no default action is supplied for and another one
        # where the action is not applicable.
        old_is_applicable = ApplyPatchAction.is_applicable
        ApplyPatchAction.is_applicable = (
            lambda *args: 'The ApplyPatchAction cannot be applied'
        )

        self.section.append(Setting(
            'default_actions',
            'NoBear: ApplyPatchAction, YBear: ApplyPatchAction'))
        ret = autoapply_actions(self.results,
                                {},
                                {},
                                self.section,
                                self.log_printer)
        self.assertEqual(ret, self.results)
        self.assertEqual(self.log_queue.get().message,
                         'YBear: The ApplyPatchAction cannot be applied')
        self.assertTrue(self.log_queue.empty())

        ApplyPatchAction.is_applicable = old_is_applicable

        self.section.append(Setting(
            'no_autoapply_warn', True))
        autoapply_actions(self.results,
                          {},
                          {},
                          self.section,
                          self.log_printer)
        self.assertTrue(self.log_queue.empty())

    def test_applicable_action(self):
        # Use a result whose action can be successfully applied.
        log_printer = self.log_printer

        class TestAction(ResultAction):

            def apply(self, *args, **kwargs):
                log_printer.debug('ACTION APPLIED SUCCESSFULLY.')

        ACTIONS.append(TestAction)

        self.section.append(Setting('default_actions', 'Z*: TestAction'))
        ret = autoapply_actions(self.results,
                                {},
                                {},
                                self.section,
                                log_printer)
        self.assertEqual(ret, [self.resultY])
        self.assertEqual(self.log_queue.get().message,
                         'ACTION APPLIED SUCCESSFULLY.')
        self.assertEqual(self.log_queue.get().message,
                         "Applied 'TestAction' "
                         "on the whole project from 'ZBear'.")
        self.assertTrue(self.log_queue.empty())

        ACTIONS.pop()

    def test_failing_action(self):
        class FailingTestAction(ResultAction):

            def apply(self, *args, **kwargs):
                raise RuntimeError("YEAH THAT'S A FAILING BEAR")

        ACTIONS.append(FailingTestAction)

        self.section.append(Setting('default_actions',
                                    'YBear: FailingTestAction'))
        ret = autoapply_actions(self.results,
                                {},
                                {},
                                self.section,
                                self.log_printer)
        self.assertEqual(ret, self.results)
        self.assertEqual(self.log_queue.get().message,
                         "Failed to execute action 'FailingTestAction'"
                         " with error: YEAH THAT'S A FAILING BEAR.")
        self.assertIn("YEAH THAT'S A FAILING BEAR",
                      self.log_queue.get().message)
        self.assertEqual(self.log_queue.get().message,
                         '-> for result ' + repr(self.resultY) + '.')
        self.assertTrue(self.log_queue.empty())

        ACTIONS.pop()


class ProcessingTest_PrintResult(unittest.TestCase):

    def setUp(self):
        self.section = Section('name')
        self.log_printer = LogPrinter(ConsolePrinter(), log_level=0)
        self.console_printer = ConsolePrinter()

    def test_autoapply_override(self):
        """
        Tests that the default_actions aren't automatically applied when the
        autoapply setting overrides that.
        """

        self.section.append(Setting('default_actions',
                                    'somebear: PrintDebugMessageAction'))

        # Verify that it would apply the action, i.e. remove the result
        results = [5, HiddenResult('origin', []),
                   Result('somebear', 'message', debug_msg='debug')]
        retval, newres = print_result(results, {}, 0, lambda *args: None,
                                      self.section, self.log_printer, {}, [],
                                      console_printer=self.console_printer)
        self.assertEqual(newres, [])
