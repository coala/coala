import tempfile
import unittest
import sys
import os

sys.path.insert(0, ".")
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.PatchResult import PatchResult, Result
from coalib.results.Diff import Diff
from coalib.settings.Section import Section
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.output.printers.NullPrinter import NullPrinter
from coalib.misc.i18n import _
from coalib.misc.ContextManagers import (simulate_console_inputs,
                                         retrieve_stdout)
from coalib.output.ConsoleInteractor import (finalize,
                                             nothing_done,
                                             acquire_settings,
                                             print_bears,
                                             get_action_info,
                                             print_result,
                                             print_section_beginning,
                                             print_results)
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.bears.Bear import Bear


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


class ConsoleInteractorTest(unittest.TestCase):
    def setUp(self):
        self.log_printer = ConsolePrinter(print_colored=False)
        self.console_printer = ConsolePrinter(print_colored=False)
        self.file_diff_dict = {}

        # All those tests assume that Result has no actions and PatchResult has
        # one. This makes this test independent from the real number of actions
        # applicable to those results.
        Result.get_actions = lambda x: []
        PatchResult.get_actions = lambda x: [ApplyPatchAction()]

        if sys.version_info < (3, 3):
            self.FileNotFoundError = OSError
        else:
            self.FileNotFoundError = FileNotFoundError

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
                         PatchResult("origin", "msg", {}),
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
            print_result(self.console_printer,
                         self.log_printer,
                         None,
                         self.file_diff_dict,
                         PatchResult("origin", "msg", {testfile_path: diff}),
                         file_dict)

        # To assure user can rechose if he didn't chose wisely
        with simulate_console_inputs("INVALID", -1, 1, 3) as input_generator:
            curr_section = Section("")
            print_section_beginning(self.console_printer, curr_section)
            print_result(self.console_printer,
                         self.log_printer,
                         curr_section,
                         self.file_diff_dict,
                         PatchResult("origin", "msg", {testfile_path: diff}),
                         file_dict)
            self.assertEqual(input_generator.last_input, 2)
            finalize(self.file_diff_dict, file_dict)
            # Check that the next section does not use the same file_diff_dict
            self.assertEqual(len(self.file_diff_dict), 0)

            with open(testfile_path) as f:
                self.assertEqual(f.readlines(), ["1\n", "3_changed\n"])

            os.remove(testfile_path)
            os.remove(testfile_path + ".orig")

            name, section = get_action_info(curr_section,
                                            TestAction().get_metadata())
            self.assertEqual(input_generator.last_input, 3)
            self.assertEqual(str(section), " {param : 3}")
            self.assertEqual(name, "TestAction")

        # Check if the user is asked for the parameter only the first time.
        # Use OpenEditorAction that needs this parameter (editor command).
        with simulate_console_inputs(1, "test_editor", 0, 1, 0) as generator:
            PatchResult.get_actions = lambda self: [OpenEditorAction()]

            patch_result = PatchResult("origin", "msg", {testfile_path: diff})
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

    def test_print_results_raising(self):
        self.assertRaises(TypeError,
                          print_results,
                          self.log_printer,
                          Section(""),
                          5,
                          {},
                          {})
        self.assertRaises(TypeError,
                          print_results,
                          self.log_printer,
                          Section(""),
                          [],
                          5,
                          {})
        self.assertRaises(TypeError,
                          print_results,
                          self.log_printer,
                          Section(""),
                          [],
                          {},
                          5)

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
                "\n\n{}\n|    |    | [{}] origin:\n|    |    | message"
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
|   1|   1| test line\n|   2|   2| line 2
|    |    | [{}] SpaceConsistencyBear:
|    |    | Trailing whitespace found
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
| ...| ...| \n|   2|   2| line 2
|   3|   3| line 3
|   4|   4| line 4
|   5|   5| line 5
|    |    | [{}] SpaceConsistencyBear:
|    |    | Trailing whitespace found
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
|   1|   1| test line
|   2|   2| line 2
|    |    | [{}] SpaceConsistencyBear:
|    |    | Trailing whitespace found
|   3|   3| line 3
|   4|   4| line 4
|   5|   5| line 5
|    |    | [{}] SpaceConsistencyBear:
|    |    | Trailing whitespace found
""".format(RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL),
           RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                             stdout.getvalue())

    def test_print_results_missing_file(self):
        # File isn't in dict, shouldn't print but also shouldn't throw. This
        # can occur if filter writers are doing nonsense. If this happens twice
        # the same should happen (whitebox testing: this is a potential bug.)
        self.log_printer = NullPrinter()
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
            self.assertEqual("""\n\nfile\n|    |    | {}\n|    |    | [{}] t:
|    |    | msg\n""".format(STR_LINE_DOESNT_EXIST,
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
            print_bears(self.log_printer, bears)
            self.assertEqual(_("No bears to show.\n"), stdout.getvalue())

    def test_print_bears(self):
        with retrieve_stdout() as stdout:
            bears = {TestBear: ["default", "docs"]}
            print_bears(self.log_printer, bears)
            expected_string = "TestBear:\n"
            expected_string += "  Test bear Description.\n\n"
            expected_string += "  " + _("Used in:") + "\n"
            expected_string += "   * default\n"
            expected_string += "   * docs\n\n"
            expected_string += "  " + _("Needed Settings:") + "\n"
            expected_string += "   * setting1: Required Setting.\n\n"
            expected_string += "  " + _("Optional Settings:") + "\n"
            expected_string += ("   * setting2: Optional Setting. (Optional, "
                                "defaults to 'None'.)\n\n")

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_settings(self):
        with retrieve_stdout() as stdout:
            bears = {SomeBear: ["default"]}
            print_bears(self.log_printer, bears)
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
            print_bears(self.log_printer, bears)
            expected_string = "SomeOtherBear:\n"
            expected_string += "  " + "This is a Bear." + "\n\n"
            expected_string += "  " + _("Used in:") + "\n"
            expected_string += "   * test\n\n"
            expected_string += "  " + _("No needed settings.") + "\n\n"
            expected_string += "  " + _("Optional Settings:") + "\n"
            expected_string += ("   * setting: This is an optional "
                                "setting. (Optional, defaults to 'None'.)\n\n")

            self.assertEqual(expected_string, stdout.getvalue())

    def test_print_bears_no_optional_settings(self):
        with retrieve_stdout() as stdout:
            bears = {TestBear2: ["test"]}
            print_bears(self.log_printer, bears)
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
            print_bears(self.log_printer, bears)
            expected_string = "SomeBear:\n"
            expected_string += "  " + "Some Description." + "\n\n"
            expected_string += "  " + _("No sections.") + "\n\n"
            expected_string += "  " + _("No needed settings.") + "\n\n"
            expected_string += "  " + _("No optional settings.") + "\n\n"

            self.assertEqual(expected_string, stdout.getvalue())


if __name__ == '__main__':
    unittest.main(verbosity=2)
