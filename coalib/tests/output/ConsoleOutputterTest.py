import queue
import unittest
import sys
sys.path.insert(0, ".")
import builtins
from coalib.bears.results.LineResult import LineResult, Result
from coalib.bears.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.output.NullPrinter import NullPrinter
from coalib.misc.i18n import _

_input = builtins.__dict__["input"]
builtins.__dict__["input"] = lambda x: x
from coalib.output.ConsoleOutputter import ConsoleOutputter


class ConsoleOutputterTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = ConsoleOutputter()

    def test_require_settings(self):
        self.assertRaises(TypeError, self.uut.acquire_settings, 0)
        self.assertEqual(self.uut.acquire_settings({0: 0}), {})

        self.assertEqual(self.uut.acquire_settings({"setting": ["help text", "SomeBear"]}),
                         {"setting": self.uut.STR_GET_VAL_FOR_SETTING.format("setting", "help text", "SomeBear")})

        self.assertEqual(self.uut.acquire_settings({"setting": ["help text", "SomeBear", "AnotherBear"]}),
                         {"setting": self.uut.STR_GET_VAL_FOR_SETTING.format("setting",
                                                                             "help text",
                                                                             "SomeBear" + _(" and ") + "AnotherBear")})

        self.assertEqual(self.uut.acquire_settings({"setting": ["help text",
                                                                "SomeBear",
                                                                "AnotherBear",
                                                                "YetAnotherBear"]}),
                         {"setting": self.uut.STR_GET_VAL_FOR_SETTING.format("setting",
                                                                             "help text",
                                                                             "SomeBear, AnotherBear" + _(" and ") +
                                                                             "YetAnotherBear")})

    def test_print_result(self):
        self.assertRaises(TypeError, self.uut._print_result, 5)
        self.uut.print = lambda x: x
        self.assertEqual("|    |    | [{normal}] {bear}:".format(normal=RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL),
                                                                 bear="origin") + "\n|    |    | message",
                         self.uut.print_result(Result("origin", "message")))

    def test_print_results(self):
        self.assertRaises(TypeError, self.uut.print_results, 5, {})
        self.assertRaises(TypeError, self.uut.print_results, [], 5)
        q = queue.Queue()
        self.uut._print = lambda string: q.put(string)

        self.uut.print_results([], {})
        self.assertRaises(queue.Empty, q.get, timeout=0)

        self.uut.print_results([Result("origin", "message")], {})
        self.assertEqual("\n\n{}\n|    |    | [{}] origin:\n|    |    | message"
                         "\n".format(self.uut.STR_PROJECT_WIDE, RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                         self.get_str_from_queue(q))

        self.uut.print_results([LineResult("SpaceConsistencyBear", 2, "", "Trailing whitespace found", "proj/white")],
                               {"proj/white": ["test line\n",
                                               "line 2\n",
                                               "line 3\n"]})
        self.assertEqual("""\n\nproj/white
|   1|   1| test line\n|   2|   2| line 2
|    |    | [{}] SpaceConsistencyBear:
|    |    | Trailing whitespace found
""".format(RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)), self.get_str_from_queue(q))

        self.uut.print_results([LineResult("SpaceConsistencyBear", 5, "", "Trailing whitespace found", "proj/white")],
                               {"proj/white": ["test line\n",
                                               "line 2\n",
                                               "line 3\n",
                                               "line 4\n",
                                               "line 5\n"]})
        self.assertEqual("""\n\nproj/white
|    .    | \n|    .    | \n|    .    | \n|   2|   2| line 2
|   3|   3| line 3
|   4|   4| line 4
|   5|   5| line 5
|    |    | [{}] SpaceConsistencyBear:
|    |    | Trailing whitespace found
""".format(RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)), self.get_str_from_queue(q))

        # Check sorting and multi result output
        self.uut.print_results([LineResult("SpaceConsistencyBear", 5, "", "Trailing whitespace found", "proj/white"),
                                LineResult("SpaceConsistencyBear", 2, "", "Trailing whitespace found", "proj/white")],
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
           RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)), self.get_str_from_queue(q))

        # File isn't in dict, shouldn't print but also shouldn't throw. This can occur if filter writers are doing
        # nonsense. If this happens twice the same should happen (whitebox testing: this is a potential bug.)
        self.uut.log_printer = NullPrinter()
        self.uut.print_results([LineResult("t", 5, "", "msg", "file"), LineResult("t", 5, "", "msg", "file")], {})
        self.assertEqual("", self.get_str_from_queue(q))

        # Line isn't in dict[file], shouldn't print but also shouldn't throw. This can occur if filter writers are doing
        # nonsense.
        self.uut.print_results([LineResult("t", 5, "", "msg", "file")], {"file": []})
        self.assertEqual("""\n\nfile\n|    |    | {}\n|    |    | [{}] t:
|    |    | msg\n""".format(self.uut.STR_LINE_DOESNT_EXIST, RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL)),
                         self.get_str_from_queue(q))

        self.assertRaises(AssertionError, self.uut.print_results, [LineResult("t", 5, "", "msg", None)], {})

    @staticmethod
    def get_str_from_queue(q):
        result = ""
        try:
            while True:
                result += q.get(timeout=0)
        except queue.Empty:
            pass

        return result


if __name__ == '__main__':
    unittest.main(verbosity=2)

builtins.__dict__["input"] = _input
