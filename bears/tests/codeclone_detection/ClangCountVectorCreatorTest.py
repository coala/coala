import sys
import os
import unittest
import inspect

sys.path.insert(0, ".")
from bears.codeclone_detection.ClangCountVectorCreator import \
    ClangCountVectorCreator
from coalib.bearlib.parsing.clang.cindex import (CursorKind,
                                                 Index,
                                                 LibclangError)


def no_condition(cursor, stack):
    return True


def is_call_argument(cursor, stack):
    for elem, child_num in stack:
        if elem.kind == CursorKind.CALL_EXPR:
            return True

    return False


class ClangCountVectorCreatorTest(unittest.TestCase):
    functions = sorted(["main(int, char *)", "test()"])

    def setUp(self):
        self.testfile = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(ClangCountVectorCreatorTest)),
            "sample.c"))

    def test_empty_counting(self):
        expected_results = {
            (6, "test()"): {},
            (12, "main(int, char *)"): {
                "i": [],
                "asd": [],
                "t": [],
                "args": []}}

        self.uut = ClangCountVectorCreator()
        cv_dict = self.uut.get_vectors_for_file(self.testfile)

        self.check_cv_dict(cv_dict, expected_results)

    def check_cv_dict(self, actual, expected):
        self.assertEqual(len(actual), len(expected))
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
                "i": [4, 1],
                "asd": [1, 0],
                "t": [4, 1],
                "args": [2, 0]}}

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
