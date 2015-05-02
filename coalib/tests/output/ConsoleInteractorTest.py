import queue
import tempfile
import unittest
import sys
import os
import builtins

sys.path.insert(0, ".")
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.PatchResult import PatchResult, Result
from coalib.results.Diff import Diff
from coalib.settings.Section import Section, Setting
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.output.printers.NullPrinter import NullPrinter
from coalib.misc.i18n import _
from coalib.output.ConsoleInteractor import ConsoleInteractor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction


class TestAction(ResultAction):
    def apply(self, result, original_file_dict, file_diff_dict, param):
        pass


class ConsoleInteractorTest(unittest.TestCase):
    def setUp(self):
        self._input = builtins.__dict__["input"]
        builtins.__dict__["input"] = lambda x: x
        self.log_printer = ConsolePrinter()
        self.uut = ConsoleInteractor(self.log_printer)

        # All those tests assume that Result has no actions and PatchResult has
        # one. This makes this test independent from the real number of actions
        # applicable to those results.
        Result.get_actions = lambda self: []
        PatchResult.get_actions = lambda self: [ApplyPatchAction()]

        if sys.version_info < (3, 3):  # pragma: no cover
            self.FileNotFoundError = OSError
        else:
            self.FileNotFoundError = FileNotFoundError

    def tearDown(self):
        builtins.__dict__["input"] = self._input

    def test_require_settings(self):
        self.assertRaises(TypeError, self.uut.acquire_settings, 0)
        self.assertEqual(self.uut.acquire_settings({0: 0}), {})

        self.assertEqual(self.uut.acquire_settings({"setting": ["help text",
                                                                "SomeBear"]}),
                         {"setting": self.uut.STR_GET_VAL_FOR_SETTING.format(
                             "setting",
                             "help text",
                             "SomeBear")})

        self.assertEqual(self.uut.acquire_settings({"setting":
                                                        ["help text",
                                                         "SomeBear",
                                                         "AnotherBear"]}),
                         {"setting": self.uut.STR_GET_VAL_FOR_SETTING.format(
                             "setting",
                             "help text",
                             "SomeBear" + _(" and ") + "AnotherBear")})

        self.assertEqual(self.uut.acquire_settings({"setting":
                                                        ["help text",
                                                         "SomeBear",
                                                         "AnotherBear",
                                                         "YetAnotherBear"]}),
                         {"setting": self.uut.STR_GET_VAL_FOR_SETTING.format(
                             "setting",
                             "help text",
                             "SomeBear, AnotherBear" + _(" and ") +
                             "YetAnotherBear")})

    def test_print_result(self):
        builtins.__dict__["input"] = lambda x: 0

        self.uut.print_result(PatchResult("origin", "msg", {}), {})

        (testfile, testfile_path) = tempfile.mkstemp()
        os.close(testfile)
        file_dict = {
            testfile_path: ["1\n", "2\n", "3\n"],
            "f_b": ["1", "2", "3"]
        }
        diff = Diff()
        diff.delete_line(2)
        diff.change_line(3, "3\n", "3_changed\n")

        builtins.__dict__["input"] = lambda x: 1
        with self.assertRaises(ValueError):
            self.uut.print_result(PatchResult("origin",
                                              "msg",
                                              {testfile_path: diff}),
                                  file_dict)

        # To assure user can rechose if he didn't chose wisely
        input_generator = InputGenerator(["INVALID", -1, 1, 3])
        builtins.__dict__["input"] = input_generator.generate_input
        # To load current_section in ConsoleInteractor object
        self.uut.begin_section(Section(""))
        self.uut.print_result(PatchResult("origin",
                                          "msg",
                                          {testfile_path: diff}), file_dict)
        self.assertEqual(input_generator.current_input, 2)
        self.uut.finalize(file_dict)
        with open(testfile_path) as f:
            self.assertEqual(f.readlines(), ["1\n", "3_changed\n"])

        os.remove(testfile_path)
        os.remove(testfile_path + ".orig")

        name, section = self.uut._get_action_info(TestAction().get_metadata())
        self.assertEqual(str(section), " {param : 3}")
        self.assertEqual(name, "TestAction")

        # Check if the user is asked for the parameter only the first time.
        # Use OpenEditorAction that needs this parameter (editor command).
        input_generator = InputGenerator([1, "test_editor", 0, 1, 0])
        # Choose open editor action
        builtins.__dict__["input"] = input_generator.generate_input
        PatchResult.get_actions = lambda self: [OpenEditorAction()]

        patch_result = PatchResult("origin", "msg", {testfile_path: diff})
        patch_result.file = "f_b"

        self.uut.print_result(patch_result, file_dict)
        # choose action, choose editor, choose no action (-1 -> 2)
        self.assertEqual(input_generator.current_input, 2)

        # Increase by 1, It shoudn't ask for parameter again
        self.uut.print_result(patch_result, file_dict)
        self.assertEqual(input_generator.current_input, 4)

    def test_static_functions(self):
        q = queue.Queue()
        # 0:-1 to strip of the trailing newline character
        self.uut._print = lambda string: q.put(string[0:-1])
        self.uut.begin_section(Section("name"))
        self.assertEqual(q.get(timeout=0), _("Executing section "
                                             "{name}...").format(name="name"))

        self.uut.did_nothing()
        self.assertEqual(q.get(timeout=0),
                         _("No existent section was targeted or enabled. "
                           "Nothing to do."))

    def test_print_results(self):
        q = queue.Queue()
        self.uut._print = lambda string, color="": q.put(string)

        self.assertRaises(TypeError, self.uut.print_results, 5, {})
        self.assertRaises(TypeError, self.uut.print_results, [], 5)

        self.uut.print_results([], {})
        self.assertRaises(queue.Empty, q.get, timeout=0)

        self.uut.print_results([Result("origin", "message")], {})
        self.assertEqual("\n\n{}\n|    |    | [{}] origin:\n|    |    | "
                         "message\n".format(
                             self.uut.STR_PROJECT_WIDE,
                             RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                         self.get_str_from_queue(q))

        self.uut.print_results([Result("SpaceConsistencyBear",
                                       "Trailing whitespace found",
                                       "proj/white",
                                       line_nr=2)],
                               {"proj/white": ["test line\n",
                                               "line 2\n",
                                               "line 3\n"]})
        self.assertEqual("""\n\nproj/white
|   1|   1| test line\n|   2|   2| line 2
|    |    | [{}] SpaceConsistencyBear:
|    |    | Trailing whitespace found
""".format(RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                         self.get_str_from_queue(q))

        self.uut.print_results([Result("SpaceConsistencyBear",
                                       "Trailing whitespace found",
                                       "proj/white",
                                       line_nr=5)],
                               {"proj/white": ["test line\n",
                                               "line 2\n",
                                               "line 3\n",
                                               "line 4\n",
                                               "line 5\n"]})
        self.assertEqual("""\n\nproj/white
| ...| ...| \n|   2|   2| line 2
|   3|   3| line 3
|   4|   4| line 4
|   5|   5| line 5
|    |    | [{}] SpaceConsistencyBear:
|    |    | Trailing whitespace found
""".format(RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                         self.get_str_from_queue(q))

        # Check sorting and multi result output
        self.uut.print_results([Result("SpaceConsistencyBear",
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
                                               "line 5\n"]})

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
                         self.get_str_from_queue(q))

        # File isn't in dict, shouldn't print but also shouldn't throw. This
        # can occur if filter writers are doing nonsense. If this happens twice
        # the same should happen (whitebox testing: this is a potential bug.)
        self.uut.log_printer = NullPrinter()
        self.uut.print_results([Result("t", "msg", "file", line_nr=5),
                                Result("t", "msg", "file", line_nr=5)], {})
        self.assertEqual("", self.get_str_from_queue(q))

        # Line isn't in dict[file], shouldn't print but also shouldn't throw.
        # This can occur if filter writers are doing nonsense.
        self.uut.print_results([Result("t", "msg", "file", line_nr=5)],
                               {"file": []})
        self.assertEqual("""\n\nfile\n|    |    | {}\n|    |    | [{}] t:
|    |    | msg\n""".format(self.uut.STR_LINE_DOESNT_EXIST,
                            RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                         self.get_str_from_queue(q))

        self.assertRaises(AssertionError,
                          self.uut.print_results,
                          [Result("t", "msg", None, line_nr=5)],
                          {})

    def test_from_section(self):
        section = Section("test")
        ConsoleInteractor.from_section(section, log_printer=self.log_printer)
        section.append(Setting("output", "stderr"))
        ConsoleInteractor.from_section(section, log_printer=self.log_printer)

    @staticmethod
    def get_str_from_queue(q):
        result = ""
        try:
            while True:
                result += q.get(timeout=0)
        except queue.Empty:
            pass

        return result


class InputGenerator:
    def __init__(self, inputs):
        self.current_input = -1
        self.inputs = inputs

    def generate_input(self, x):
        self.current_input += 1
        return self.inputs[self.current_input]


if __name__ == '__main__':
    unittest.main(verbosity=2)
