import tempfile
import unittest
import sys
import os
from collections import OrderedDict
from pyprint.NullPrinter import NullPrinter
from pyprint.ConsolePrinter import ConsolePrinter

sys.path.insert(0, ".")
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.misc.i18n import _
from coalib.misc.ContextManagers import (simulate_console_inputs,
                                         retrieve_stdout)
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
from bears.misc.KeywordBear import KeywordBear
from bears.misc.LineLengthBear import LineLengthBear


STR_GET_VAL_FOR_SETTING = _("Please enter a value for the setting \"{}\" ({}) "
                            "needed by {}: ")
STR_LINE_DOESNT_EXIST = _("The line belonging to the following result "
                          "cannot be printed because it refers to a line "
                          "that doesn't seem to exist in the given file.")
STR_PROJECT_WIDE = _("Project wide:")


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

        OpenEditorAction.is_applicable = staticmethod(lambda result: False)
        ApplyPatchAction.is_applicable = staticmethod(lambda result: False)

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

        (testfile, testfile_path) = tempfile.mkstemp()
        os.close(testfile)
        file_dict = {
            testfile_path: ["1\n", "2\n", "3\n"],
            "f_b": ["1", "2", "3"]
        }
        diff = Diff()
        diff.delete_line(2)
        diff.change_line(3, "3\n", "3_changed\n")

        with simulate_console_inputs(1), self.assertRaises(ValueError):
            ApplyPatchAction.is_applicable = staticmethod(lambda result: True)
            print_result(self.console_printer,
                         self.log_printer,
                         None,
                         self.file_diff_dict,
                         Result("origin", "msg", diffs={testfile_path: diff}),
                         file_dict)

        # Interaction must be closed by the user with `0` if it's not a param
        with simulate_console_inputs("INVALID", -1, 1, 0, 3) as input_generator:
            curr_section = Section("")
            print_section_beginning(self.console_printer, curr_section)
            print_result(self.console_printer,
                         self.log_printer,
                         curr_section,
                         self.file_diff_dict,
                         Result("origin", "msg", diffs={testfile_path: diff}),
                         file_dict)
            self.assertEqual(input_generator.last_input, 3)

            self.file_diff_dict.clear()

            with open(testfile_path) as f:
                self.assertEqual(f.readlines(), ["1\n", "3_changed\n"])

            os.remove(testfile_path)
            os.remove(testfile_path + ".orig")

            name, section = get_action_info(curr_section,
                                            TestAction().get_metadata())
            self.assertEqual(input_generator.last_input, 4)
            self.assertEqual(str(section), " {param : 3}")
            self.assertEqual(name, "TestAction")

        # Check if the user is asked for the parameter only the first time.
        # Use OpenEditorAction that needs this parameter (editor command).
        with simulate_console_inputs(1, "test_editor", 0, 1, 0) as generator:
            OpenEditorAction.is_applicable = staticmethod(lambda result: True)

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

    def test_static_functions(self):
        with retrieve_stdout() as stdout:
            print_section_beginning(self.console_printer, Section("name"))
            self.assertEqual(stdout.getvalue(),
                             _("Executing section "
                               "{name}...").format(name="name") + "\n")

        with retrieve_stdout() as stdout:
            nothing_done(self.console_printer)
            self.assertEqual(stdout.getvalue(),
                             _("No existent section was targeted or enabled. "
                               "Nothing to do.") + "\n")

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
                "\n\n{}\n|    | [{}] origin:\n|    | message"
                "\n".format(STR_PROJECT_WIDE,
                            RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                stdout.getvalue())

    def test_print_results_for_file(self):
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result("SpaceConsistencyBear",
                        "Trailing whitespace found",
                        "proj/white",
                        line_nr=2)],
                {"proj/white": ["test line\n", "line 2\n", "line 3\n"]},
                {},
                color=False)
            self.assertEqual("""\n\nproj/white
|   1| test line\n|   2| line 2
|    | [{}] SpaceConsistencyBear:
|    | Trailing whitespace found
""".format(RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                         stdout.getvalue())

        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result("SpaceConsistencyBear",
                        "Trailing whitespace found",
                        "proj/white",
                        line_nr=5)],
                {"proj/white": ["test line\n",
                                "line 2\n",
                                "line 3\n",
                                "line 4\n",
                                "line 5\n"]},
                {},
                color=False)
            self.assertEqual("""\n\nproj/white
| ...| \n|   2| line 2
|   3| line 3
|   4| line 4
|   5| line 5
|    | [{}] SpaceConsistencyBear:
|    | Trailing whitespace found
""".format(RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                             stdout.getvalue())

    def test_print_results_sorting(self):
        with retrieve_stdout() as stdout:
            print_results(self.log_printer,
                          Section(""),
                          [Result("SpaceConsistencyBear",
                                  "Trailing whitespace found",
                                  "proj/white",
                                  line_nr=5),
                           Result("SpaceConsistencyBear",
                                  "Trailing whitespace found",
                                  "proj/white",
                                  line_nr=2)],
                          {"proj/white": ["test line\n",
                                          "line 2\n",
                                          "line 3\n",
                                          "line 4\n",
                                          "line 5\n"]},
                          {},
                          color=False)

            self.assertEqual("""\n\nproj/white
|   1| test line
|   2| line 2
|    | [{}] SpaceConsistencyBear:
|    | Trailing whitespace found
|   3| line 3
|   4| line 4
|   5| line 5
|    | [{}] SpaceConsistencyBear:
|    | Trailing whitespace found
""".format(RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL),
           RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                             stdout.getvalue())

    def test_print_results_missing_file(self):
        # File isn't in dict, shouldn't print but also shouldn't throw. This
        # can occur if filter writers are doing nonsense. If this happens twice
        # the same should happen (whitebox testing: this is a potential bug.)
        self.log_printer = LogPrinter(NullPrinter())
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result("t", "msg", "file", line_nr=5),
                 Result("t", "msg", "file", line_nr=5)],
                {},
                {},
                color=False)
            self.assertEqual("", stdout.getvalue())

    def test_print_results_missing_line(self):
        # Line isn't in dict[file], shouldn't print but also shouldn't throw.
        # This can occur if filter writers are doing nonsense.
        with retrieve_stdout() as stdout:
            print_results(
                self.log_printer,
                Section(""),
                [Result("t", "msg", "file", line_nr=5)],
                {"file": []},
                {},
                color=False)
            self.assertEqual("""\n\nfile\n|    | {}\n|    | [{}] t:
|    | msg\n""".format(STR_LINE_DOESNT_EXIST,
                            RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                             stdout.getvalue())

        self.assertRaises(AssertionError,
                          print_results,
                          self.log_printer,
                          Section(""),
                          [Result("t", "msg", None, line_nr=5)],
                          {},
                          {})

    def test_print_bears_empty(self):
        with retrieve_stdout() as stdout:
            bears = {}
            print_bears(self.log_printer.printer, bears, True)
            self.assertEqual(_("No bears to show.") + "\n", stdout.getvalue())
        with retrieve_stdout() as stdout:
            bears = {}
            print_bears(self.log_printer.printer, bears, False)
            self.assertEqual(_("No bears to show.") + "\n", stdout.getvalue())

    def test_print_bears(self):
        with retrieve_stdout() as stdout:
            bears = {TestBear: ["default", "docs"]}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "TestBear:\n"
            expected_string += "  Test bear Description.\n\n"
            expected_string += "  " + _("Used in:") + "\n"
            expected_string += "   * default\n"
            expected_string += "   * docs\n\n"
            expected_string += "  " + _("Needed Settings:") + "\n"
            expected_string += "   * setting1: Required Setting.\n\n"
            expected_string += "  " + _("Optional Settings:") + "\n"
            expected_string += "   * setting2: Optional Setting. ("
            expected_string += _("Optional, defaults to '{}'.").format("None")
            expected_string += ")\n\n"

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_settings(self):
        with retrieve_stdout() as stdout:
            bears = {SomeBear: ["default"]}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "SomeBear:\n"
            expected_string += "  " + "Some Description." + "\n\n"
            expected_string += "  " + _("Used in:") + "\n"
            expected_string += "   * default\n\n"
            expected_string += "  " + _("No needed settings.") + "\n\n"
            expected_string += "  " + _("No optional settings.") + "\n\n"

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_needed_settings(self):
        with retrieve_stdout() as stdout:
            bears = {SomeOtherBear: ["test"]}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "SomeOtherBear:\n"
            expected_string += "  " + "This is a Bear." + "\n\n"
            expected_string += "  " + _("Used in:") + "\n"
            expected_string += "   * test\n\n"
            expected_string += "  " + _("No needed settings.") + "\n\n"
            expected_string += "  " + _("Optional Settings:") + "\n"
            expected_string += "   * setting: This is an optional setting. ("
            expected_string += _("Optional, defaults to '{}'.").format("None")
            expected_string += ")\n\n"

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_optional_settings(self):
        with retrieve_stdout() as stdout:
            bears = {TestBear2: ["test"]}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "TestBear2:\n"
            expected_string += "  Test bear 2 description.\n\n"
            expected_string += "  " + _("Used in:") + "\n"
            expected_string += "   * test\n\n"
            expected_string += "  " + _("Needed Settings:") + "\n"
            expected_string += "   * setting1: Required Setting.\n\n"
            expected_string += "  " + _("No optional settings.") + "\n\n"

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_sections(self):
        with retrieve_stdout() as stdout:
            bears = {SomeBear: []}
            print_bears(self.log_printer.printer, bears, False)
            expected_string = "SomeBear:\n"
            expected_string += "  " + "Some Description." + "\n\n"
            expected_string += "  " + _("No sections.") + "\n\n"
            expected_string += "  " + _("No needed settings.") + "\n\n"
            expected_string += "  " + _("No optional settings.") + "\n\n"

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
        expected_string = ("id:-?[0-9]+:origin:1:file:None:line_nr:None:"
                           "severity:1:msg:2\n")
        with retrieve_stdout() as stdout:
            print_results_formatted(self.logger,
                                    self.section,
                                    [Result("1", "2")],
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
