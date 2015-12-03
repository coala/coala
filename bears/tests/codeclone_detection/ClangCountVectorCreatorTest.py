import sys
import os
import unittest

sys.path.insert(0, ".")
from bears.codeclone_detection.ClangCountVectorCreator import (
    ClangCountVectorCreator)
from clang.cindex import CursorKind, Index, LibclangError


def no_condition(stack):
    return True


def is_call_argument(stack):
    for elem, child_num in stack:
        if elem.kind == CursorKind.CALL_EXPR:
            return True

    return False


class ClangCountVectorCreatorTest(unittest.TestCase):
    functions = sorted(["main(int, char *)", "test()"])

    def setUp(self):
        self.testfile = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "sample.c"))

    def test_empty_counting(self):
        expected_results = {
            (6, "test()"): {},
            (12, "main(int, char *)"): {
                # Variables
                "i": [],
                "asd": [],
                "t": [],
                "args": [],
                # Globals
                "g": [],
                # Functions
                "smile": [],
                "printf": [],
                # Constants
                "#5": [],
                '#"i is %d"': []}}

        self.uut = ClangCountVectorCreator()
        cv_dict = self.uut.get_vectors_for_file(self.testfile)

        self.check_cv_dict(cv_dict, expected_results)

    def check_cv_dict(self, actual, expected):
        self.assertEqual(len(actual), len(expected), str(actual))
        self.assertEqual(sorted(actual.keys()), sorted(expected.keys()))

        for function in actual:
            self.assertEqual(len(actual[function]), len(expected[function]))
            self.assertEqual(sorted(actual[function].keys()),
                             sorted(expected[function].keys()))
            for variable in actual[function]:
                self.assertEqual(actual[function][variable].count_vector,
                                 expected[function][variable])

    def test_counting(self):
        expected_results = {
            (6, "test()"): {},
            (12, "main(int, char *)"): {
                # Variables
                "i": [4, 1],
                "asd": [1, 0],
                "t": [4, 1],
                "args": [2, 0],
                # Globals
                "g": [3, 1],
                # Functions
                "smile": [1, 1],
                "printf": [1, 1],
                # Constants
                "#5": [1, 0],
                '#"i is %d"': [1, 1]}}

        self.uut = ClangCountVectorCreator([no_condition, is_call_argument])
        cv_dict = self.uut.get_vectors_for_file(self.testfile)

        self.check_cv_dict(cv_dict, expected_results)


def skip_test():
    try:
        Index.create()
        return False
    except LibclangError as error:
        return str(error)


if __name__ == '__main__':
    unittest.main(verbosity=2)
