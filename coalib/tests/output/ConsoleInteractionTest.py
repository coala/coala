import unittest
import os
from os.path import abspath
from collections import OrderedDict
from pyprint.NullPrinter import NullPrinter
from pyprint.ConsolePrinter import ConsolePrinter

from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.results.Diff import Diff
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.misc.ContextManagers import (simulate_console_inputs,
                                         retrieve_stdout,
                                         make_temp)
from coalib.output.ConsoleInteraction import (nothing_done,
                                              acquire_settings,
                                              print_bears,
                                              get_action_info,
                                              print_result,
                                              print_section_beginning,
                                              print_results,
                                              show_bears,
                                              print_results_formatted)
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.StringPrinter import StringPrinter
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.bears.Bear import Bear
from bears.general.KeywordBear import KeywordBear
from bears.general.LineLengthBear import LineLengthBear


STR_GET_VAL_FOR_SETTING = ("Please enter a value for the setting \"{}\" ({}) "
                           "needed by {}: ")
STR_LINE_DOESNT_EXIST = ("The line belonging to the following result "
                         "cannot be printed because it refers to a line "
                         "that doesn't seem to exist in the given file.")
STR_PROJECT_WIDE = "Project wide:"


class TestAction(ResultAction):

    def apply(self, result, original_file_dict, file_diff_dict, param):
        pass


class TestBear(Bear):

    def run(self, setting1, setting2: int=None):
        """
        Test bear Description.

        :param setting1: Required Setting.
        :param setting2: Optional Setting.
        """
        return None


class TestBear2(Bear):

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
        setting = 1
        return None


class SomeglobalBear(Bear):

    def run(self):
        """
        Some Description.
        """
        return None


class ConsoleInteractionTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = LogPrinter(ConsolePrinter(print_colored=False))
        self.console_printer = ConsolePrinter(print_colored=False)
        self.file_diff_dict = {}
        self.local_bears = OrderedDict([("default", [KeywordBear]),
                                        ("test", [LineLengthBear,
                                                  KeywordBear])])
        self.global_bears = OrderedDict([("default", [SomeglobalBear]),
                                         ("test", [SomeglobalBear])])

        self.old_open_editor_applicable = OpenEditorAction.is_applicable
        OpenEditorAction.is_applicable = staticmethod(lambda *args: False)

        self.old_apply_patch_applicable = ApplyPatchAction.is_applicable
        ApplyPatchAction.is_applicable = staticmethod(lambda *args: False)

    def tearDown(self):
        OpenEditorAction.is_applicable = self.old_open_editor_applicable
        ApplyPatchAction.is_applicable = self.old_apply_patch_applicable

    def test_require_settings(self):
        self.assertRaises(TypeError, acquire_settings, self.log_printer, 0)
        self.assertEqual(acquire_settings(self.log_printer, {0: 0}), {})

        with simulate_console_inputs(0, 1, 2) as generator:
            self.assertEqual(acquire_settings(self.log_printer,
                                              {"setting": ["help text",
                                                           "SomeBear"]}),
                             {"setting": 0})

            self.assertEqual(acquire_settings(self.log_printer,
                                              {"setting": ["help text",
                                                           "SomeBear",
                                                           "AnotherBear"]}),
                             {"setting": 1})

            self.assertEqual(acquire_settings(self.log_printer,
                                              {"setting": ["help text",
                                                           "SomeBear",
                                                           "AnotherBear",
                                                           "YetAnotherBear"]}),
                             {"setting": 2})

            self.assertEqual(generator.last_input, 2)

    def test_print_result(self):
        print_result(self.console_printer,
                     self.log_printer,
                     None,
                     self.file_diff_dict,
                     "illegal value",
                     {})

        with simulate_console_inputs(0):
            print_result(self.console_printer,
                         self.log_printer,
                         None,
                         self.file_diff_dict,
                         Result("origin", "msg", diffs={}),
                         {})

        with make_temp() as testfile_path:
            file_dict = {
                testfile_path: ["1\n", "2\n", "3\n"],
                "f_b": ["1", "2", "3"]
            }
            diff = Diff(file_dict[testfile_path])
            diff.delete_line(2)
            diff.change_line(3, "3\n", "3_changed\n")

            with simulate_console_inputs(1), self.assertRaises(ValueError):
                ApplyPatchAction.is_applicable = staticmethod(
                    lambda *args: True)
                print_result(self.console_printer,
                             self.log_printer,
                             None,
                             self.file_diff_dict,
                             Result("origin", "msg", diffs={
                                    testfile_path: diff}),
                             file_dict)

            # Interaction must be closed by the user with `0` if it's not a
            # param
            with simulate_console_inputs("INVALID",
                                         -1,
                                         1,
                                         0,
                                         3) as input_generator:
                curr_section = Section("")
                print_section_beginning(self.console_printer, curr_section)
                print_result(self.console_printer,
                             self.log_printer,
                             curr_section,
                             self.file_diff_dict,
                             Result("origin", "msg", diffs={
                                    testfile_path: diff}),
                             file_dict)
                self.assertEqual(input_generator.last_input, 3)

                self.file_diff_dict.clear()

                with open(testfile_path) as f:
                    self.assertEqual(f.readlines(), ["1\n", "3_changed\n"])

                os.remove(testfile_path + ".orig")

                name, section = get_action_info(curr_section,
                                                TestAction().get_metadata())
                self.assertEqual(input_generator.last_input, 4)
                self.assertEqual(str(section), " {param : '3'}")
                self.assertEqual(name, "TestAction")

        # Check if the user is asked for the parameter only the first time.
        # Use OpenEditorAction that needs this parameter (editor command).
        with simulate_console_inputs(1, "test_editor", 0, 1, 0) as generator:
            OpenEditorAction.is_applicable = staticmethod(lambda *args: True)

            patch_result = Result("origin", "msg", diffs={testfile_path: diff})
            patch_result.file = "f_b"

            print_result(self.console_printer,
                         self.log_printer,
                         curr_section,
                         self.file_diff_dict,
                         patch_result,
                         file_dict)
            # choose action, choose editor, choose no action (-1 -> 2)
            self.assertEqual(generator.last_input, 2)

            # It shoudn't ask for parameter again
            print_result(self.console_printer,
                         self.log_printer,
                         curr_section,
                         self.file_diff_dict,
                         patch_result,
                         file_dict)
            self.assertEqual(generator.last_input, 4)

    def test_print_section_beginning(self):
        with retrieve_stdout() as stdout:
            print_section_beginning(self.console_printer, Section("name"))
            self.assertEqual(stdout.getvalue(), "Executing section name...\n")

    def test_nothing_done(self):
        with retrieve_stdout() as stdout:
            nothing_done(self.log_printer)
            self.assertIn("No existent section was targeted or enabled. "
                          "Nothing to do.\n",
                          stdout.getvalue())

    def test_print_results_empty(self):
        with retrieve_stdout() as stdout:
            print_results(self.log_printer, Section(""), [], {}, {})
            self.assertEqual(stdout.getvalue(), "")

    def test_print_results_project_wide(self):
        with retrieve_stdout() as stdout:
            print_results(self.log_printer,
                          Section(""),
                          [Result("origin", "message")],
                          {},
                          {},
                          color=False)
            self.assertEqual(
                "\n{}\n|    | [NORMAL] origin:\n|    | message"
                "\n".format(STR_PROJECT_WIDE),
                stdout.getvalue())

    def test_print_results_for_file(self):
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result.from_values("SpaceConsistencyBear",
                                    "Trailing whitespace found",
                                    file="filename",
                                    line=2)],
                {abspath("filename"): ["test line\n", "line 2\n", "line 3\n"]},
                {},
                color=False)
            self.assertEqual("""\nfilename
|   2| line 2
|    | [NORMAL] SpaceConsistencyBear:
|    | Trailing whitespace found
""",
                             stdout.getvalue())

        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result.from_values("SpaceConsistencyBear",
                                    "Trailing whitespace found",
                                    file="filename",
                                    line=5)],
                {abspath("filename"): ["test line\n",
                                       "line 2\n",
                                       "line 3\n",
                                       "line 4\n",
                                       "line 5\n"]},
                {},
                color=False)
            self.assertEqual("""\nfilename
|   5| line 5
|    | [NORMAL] SpaceConsistencyBear:
|    | Trailing whitespace found
""",
                             stdout.getvalue())

    def test_print_results_sorting(self):
        with retrieve_stdout() as stdout:
            print_results(self.log_printer,
                          Section(""),
                          [Result.from_values("SpaceConsistencyBear",
                                              "Trailing whitespace found",
                                              file="file",
                                              line=5),
                           Result.from_values("SpaceConsistencyBear",
                                              "Trailing whitespace found",
                                              file="file",
                                              line=2)],
                          {abspath("file"): ["test line\n",
                                             "line 2\n",
                                             "line 3\n",
                                             "line 4\n",
                                             "line 5\n"]},
                          {},
                          color=False)

            self.assertEqual("""
file
|   2| line 2
|    | [NORMAL] SpaceConsistencyBear:
|    | Trailing whitespace found

file
|   5| line 5
|    | [NORMAL] SpaceConsistencyBear:
|    | Trailing whitespace found
""",
                             stdout.getvalue())

    def test_print_results_multiple_ranges(self):
        affected_code = (
            SourceRange.from_values("some_file", 5, end_line=7),
            SourceRange.from_values("another_file", 1, 3, 1, 5),
            SourceRange.from_values("another_file", 3, 3, 3, 5))
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result("ClangCloneDetectionBear",
                        "Clone Found",
                        affected_code)],
                {abspath("some_file"): ["line " + str(i + 1) + "\n"
                                        for i in range(10)],
                 abspath("another_file"): ["line " + str(i + 1) + "\n"
                                           for i in range(10)]},
                {},
                color=False)
            self.assertEqual("""
another_file
|   1| line 1

another_file
|   3| line 3

some_file
|   5| line 5
|   6| line 6
|   7| line 7
|    | [NORMAL] ClangCloneDetectionBear:
|    | Clone Found
""",
                             stdout.getvalue())

    def test_print_results_missing_file(self):
        self.log_printer = LogPrinter(NullPrinter())
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result("t", "msg"),
                 Result.from_values("t", "msg", file="file", line=5)],
                {},
                {},
                color=False)
            self.assertEqual("\n" + STR_PROJECT_WIDE + "\n"
                             "|    | [NORMAL] t:\n"
                             "|    | msg\n"
                             # Second results file isn't there, no context is
                             # printed, only a warning log message which we
                             # don't catch
                             "|    | [NORMAL] t:\n"
                             "|    | msg\n", stdout.getvalue())

    def test_print_results_missing_line(self):
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result.from_values("t", "msg", file="file", line=5),
                 Result.from_values("t", "msg", file="file", line=6)],
                {abspath("file"): ["line " + str(i + 1) for i in range(5)]},
                {},
                color=False)
            self.assertEqual("\n"
                             "file\n"
                             "|   5| line 5\n"
                             "|    | [NORMAL] t:\n"
                             "|    | msg\n"
                             "\n"
                             "file\n"
                             "|    | {}\n"
                             "|    | [NORMAL] t:\n"
                             "|    | msg\n".format(STR_LINE_DOESNT_EXIST),
                             stdout.getvalue())

    def test_print_results_without_line(self):
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result.from_values("t", "msg", file="file")],
                {abspath("file"): []},
                {},
                color=False)
            self.assertEqual(
                "\nfile\n"
                "|    | [NORMAL] t:\n"
                "|    | msg\n",
                stdout.getvalue())

    def test_print_bears_empty(self):
        with retrieve_stdout() as stdout:
            bears = {}
            print_bears(self.log_printer.printer, bears, True)
            self.assertEqual("No bears to show.\n", stdout.getvalue())
        with retrieve_stdout() as stdout:
            bears = {}
            print_bears(self.log_printer.printer, bears, False)
            self.assertEqual("No bears to show.\n", stdout.getvalue())

    def test_print_bears(self):
        with retrieve_stdout() as stdout:
            bears = {TestBear: ["default", "docs"]}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "TestBear:\n"
            expected_string += "  Test bear Description.\n\n"
            expected_string += "  Used in:\n"
            expected_string += "   * default\n"
            expected_string += "   * docs\n\n"
            expected_string += "  Needed Settings:\n"
            expected_string += "   * setting1: Required Setting.\n\n"
            expected_string += "  Optional Settings:\n"
            expected_string += "   * setting2: Optional Setting. ("
            expected_string += "Optional, defaults to 'None'."
            expected_string += ")\n\n"

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_settings(self):
        with retrieve_stdout() as stdout:
            bears = {SomeBear: ["default"]}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "SomeBear:\n"
            expected_string += "  Some Description.\n\n"
            expected_string += "  Used in:\n"
            expected_string += "   * default\n\n"
            expected_string += "  No needed settings.\n\n"
            expected_string += "  No optional settings.\n\n"

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_needed_settings(self):
        with retrieve_stdout() as stdout:
            bears = {SomeOtherBear: ["test"]}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "SomeOtherBear:\n"
            expected_string += "  This is a Bear.\n\n"
            expected_string += "  Used in:\n"
            expected_string += "   * test\n\n"
            expected_string += "  No needed settings.\n\n"
            expected_string += "  Optional Settings:\n"
            expected_string += "   * setting: This is an optional setting. ("
            expected_string += "Optional, defaults to 'None'."
            expected_string += ")\n\n"

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_optional_settings(self):
        with retrieve_stdout() as stdout:
            bears = {TestBear2: ["test"]}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "TestBear2:\n"
            expected_string += "  Test bear 2 description.\n\n"
            expected_string += "  Used in:\n"
            expected_string += "   * test\n\n"
            expected_string += "  Needed Settings:\n"
            expected_string += "   * setting1: Required Setting.\n\n"
            expected_string += "  No optional settings.\n\n"

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_sections(self):
        with retrieve_stdout() as stdout:
            bears = {SomeBear: []}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "SomeBear:\n"
            expected_string += "  Some Description.\n\n"
            expected_string += "  No sections.\n\n"
            expected_string += "  No needed settings.\n\n"
            expected_string += "  No optional settings.\n\n"

            self.assertEqual(expected_string, stdout.getvalue())

    def test_show_bears(self):
        with retrieve_stdout() as stdout:
            bears = {KeywordBear: ['default', 'test'],
                     LineLengthBear: ['test'],
                     SomeglobalBear: ['default', 'test']}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = stdout.getvalue()
        self.maxDiff = None
        with retrieve_stdout() as stdout:
            show_bears(self.local_bears,
                       self.global_bears,
                       False,
                       self.log_printer.printer)
            self.assertEqual(expected_string, stdout.getvalue())

        with retrieve_stdout() as stdout:
            show_bears(self.local_bears,
                       self.global_bears,
                       True,
                       self.log_printer.printer)
            self.assertEqual(" * KeywordBear\n"
                             " * LineLengthBear\n"
                             " * SomeglobalBear\n", stdout.getvalue())


# Own test because this is easy and not tied to the rest
class PrintFormattedResultsTest(unittest.TestCase):

    def setUp(self):
        self.printer = StringPrinter()
        self.logger = LogPrinter(self.printer)
        self.section = Section("t")

    def test_default_format(self):
        expected_string = ("id:-?[0-9]+:origin:1:file:None:from_line:None:"
                           "from_column:None:to_line:None:to_column:None:"
                           "severity:1:msg:2\n")
        with retrieve_stdout() as stdout:
            print_results_formatted(self.logger,
                                    self.section,
                                    [Result("1", "2")],
                                    None,
                                    None)
            self.assertRegex(stdout.getvalue(), expected_string)

    def test_multiple_ranges(self):
        expected_string = (
            "id:-?[0-9]+:origin:1:.*file:.*another_file:from_line:5:"
            "from_column:3:to_line:5:to_column:5:"
            "severity:1:msg:2\n"
            "id:-?[0-9]+:origin:1:.*file:.*some_file:from_line:5:"
            "from_column:None:to_line:7:to_column:None:"
            "severity:1:msg:2\n")
        affected_code = (SourceRange.from_values("some_file", 5, end_line=7),
                         SourceRange.from_values("another_file", 5, 3, 5, 5))
        with retrieve_stdout() as stdout:
            print_results_formatted(self.logger,
                                    self.section,
                                    [Result("1", "2", affected_code)],
                                    None,
                                    None)
            self.assertRegex(stdout.getvalue(), expected_string)

    def test_bad_format(self):
        self.section.append(Setting("format_str", "{nonexistant}"))
        print_results_formatted(self.logger,
                                self.section,
                                [Result("1", "2")],
                                None,
                                None)
        self.assertRegex(self.printer.string, ".*Unable to print.*")

    def test_good_format(self):
        self.section.append(Setting("format_str", "{origin}"))
        with retrieve_stdout() as stdout:
            print_results_formatted(self.logger,
                                    self.section,
                                    [Result("1", "2")],
                                    None,
                                    None)
            self.assertEqual(stdout.getvalue(), "1\n")

    def test_empty_list(self):
        self.section.append(Setting("format_str", "{origin}"))
        # Shouldn't attempt to format the string None and will fail badly if
        # its done wrong.
        print_results_formatted(None,
                                self.section,
                                [],
                                None,
                                None,
                                None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
