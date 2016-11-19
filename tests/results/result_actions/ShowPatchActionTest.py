import unittest
from os.path import join

from coalib.misc.ContextManagers import retrieve_stdout
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction
from coalib.settings.Section import Section, Setting


class DummyFileProxy:

    def __init__(self, lines):
        self.lines = lines


class ShowPatchActionTest(unittest.TestCase):

    def setUp(self):
        self.uut = ShowPatchAction()
        self.file_dict = {"a": DummyFileProxy(["a\n", "b\n", "c\n"]),
                          "b": DummyFileProxy(["old_first\n"])}
        self.diff_dict = {"a": Diff(self.file_dict['a'].lines),
                          "b": Diff(self.file_dict['b'].lines)}
        self.diff_dict["a"].add_lines(1, ["test\n"])
        self.diff_dict["a"].delete_line(3)
        self.diff_dict["b"].add_lines(0, ["first\n"])

        self.test_result = Result("origin", "message", diffs=self.diff_dict)
        self.section = Section("name")
        self.section.append(Setting("colored", "false"))

    def test_is_applicable(self):
        self.assertFalse(self.uut.is_applicable(1, None, None))
        self.assertFalse(self.uut.is_applicable(Result("o", "m"), None, None))
        self.assertTrue(self.uut.is_applicable(self.test_result, {}, {}))
        self.assertFalse(self.uut.is_applicable(self.test_result, {},
                                                self.diff_dict))

    def test_apply(self):
        with retrieve_stdout() as stdout:
            self.assertEqual(self.uut.apply_from_section(self.test_result,
                                                         self.file_dict,
                                                         {},
                                                         self.section),
                             {})
            self.assertEqual(stdout.getvalue(),
                             "|----|    | a\n"
                             "|    |++++| a\n"
                             "|   1|   1| a\n"
                             "|    |   2|+test\n"
                             "|   2|   3| b\n"
                             "|   3|    |-c\n"
                             "|----|    | b\n"
                             "|    |++++| b\n"
                             "|    |   1|+first\n"
                             "|   1|   2| old_first\n")

    def test_apply_renaming_only(self):
        with retrieve_stdout() as stdout:
            test_result = Result("origin", "message",
                                 diffs={'a': Diff([], rename='b')})
            file_dict = {'a': DummyFileProxy([])}
            self.assertEqual(self.uut.apply_from_section(test_result,
                                                         file_dict,
                                                         {},
                                                         self.section),
                             {})
            self.assertEqual(stdout.getvalue(),
                             '|----|    | ' + join('a', 'a') + '\n'
                             '|    |++++| ' + join('b', 'b') + '\n')

    def test_apply_empty(self):
        with retrieve_stdout() as stdout:
            test_result = Result("origin", "message",
                                 diffs={'a': Diff([])})
            file_dict = {'a': DummyFileProxy([])}
            self.assertEqual(self.uut.apply_from_section(test_result,
                                                         file_dict,
                                                         {},
                                                         self.section),
                             {})
            self.assertEqual(stdout.getvalue(), '')

    def test_apply_with_previous_patches(self):
        with retrieve_stdout() as stdout:
            previous_diffs = {"a": Diff(self.file_dict['a'].lines)}
            previous_diffs["a"].change_line(2, "b\n", "b_changed\n")
            self.assertEqual(self.uut.apply_from_section(self.test_result,
                                                         self.file_dict,
                                                         previous_diffs,
                                                         self.section),
                             previous_diffs)
            self.assertEqual(stdout.getvalue(),
                             "|----|    | a\n"
                             "|    |++++| a\n"
                             "|   1|   1| a\n"
                             "|    |   2|+test\n"
                             "|   2|   3| b_changed\n"
                             "|   3|    |-c\n"
                             "|----|    | b\n"
                             "|    |++++| b\n"
                             "|    |   1|+first\n"
                             "|   1|   2| old_first\n")

    def test_apply_with_rename(self):
        with retrieve_stdout() as stdout:
            previous_diffs = {"a": Diff(self.file_dict['a'].lines)}
            previous_diffs["a"].change_line(2, "b\n", "b_changed\n")

            diff_dict = {"a": Diff(self.file_dict['a'].lines,
                                   rename="a.rename"),
                         "b": Diff(self.file_dict['b'].lines, delete=True)}
            diff_dict["a"].add_lines(1, ["test\n"])
            diff_dict["a"].delete_line(3)
            diff_dict["b"].add_lines(0, ["first\n"])

            test_result = Result("origin", "message", diffs=diff_dict)

            self.assertEqual(self.uut.apply_from_section(test_result,
                                                         self.file_dict,
                                                         previous_diffs,
                                                         self.section),
                             previous_diffs)
            self.assertEqual(stdout.getvalue(),
                             "|----|    | a\n"
                             "|    |++++| a.rename\n"
                             "|   1|   1| a\n"
                             "|    |   2|+test\n"
                             "|   2|   3| b_changed\n"
                             "|   3|    |-c\n"
                             "|----|    | b\n"
                             "|    |++++| /dev/null\n"
                             "|   1|    |-old_first\n")
