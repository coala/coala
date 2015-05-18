import sys
import os
import unittest
import inspect

sys.path.insert(0, ".")
from coalib.settings.Setting import Setting
from bears.codeclone_detection.ClangCountVectorCreator import (
    ClangCountVectorCreator)
from bears.codeclone_detection import ClangCountingConditions
from coalib.bearlib.parsing.clang.cindex import Index, LibclangError


class ClangCountingConditionsTest(unittest.TestCase):
    def setUp(self):
        self.testfile = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(ClangCountingConditionsTest)),
            "conditions_samples.c"))

    def check_counting_condition(self, conditions, function, expected):
        """
        Checks if the given count vectors match the given expected data.

        :param conditions: String indicating which condition(s) to use (will
                           be fed to
                           ClangCountingConditions.counting_condition)
        :param function:   String indicating which function from test file to
                           use. (i.e. "used(int, int)")
        :param expected:   Dict with python lists of counts for all variables.
        """
        counter = ClangCountVectorCreator(
            ClangCountingConditions.counting_condition(
                Setting("irrelevant", conditions)))
        vectors = counter.get_vectors_for_file(self.testfile)

        actual = vectors[function]
        self.assertEqual(len(actual), len(expected))
        self.assertEqual(sorted(actual.keys()),
                         sorted(expected.keys()))
        for variable in actual:
            self.assertEqual(actual[variable].count_vector,
                             expected[variable],
                             "Variable '{}' doesnt match.".format(variable))

    def test_conversion(self):
        with self.assertRaises(TypeError):
            ClangCountingConditions.counting_condition(5)

        self.assertEqual(
            ClangCountingConditions.counting_condition(
                Setting("irrelevant", "used, in_condition")),
            [ClangCountingConditions.used,
             ClangCountingConditions.in_condition])

    def test_used(self):
        self.check_counting_condition(
            "used",
            (1, "used(int, int)"),
            {"a": [5],
             "b": [6]})

    def test_returned(self):
        self.check_counting_condition(
            "returned",
            (13, "returned(int, int)"),
            {"a": [3],
             "b": [2]})

    def test_is_condition(self):
        self.check_counting_condition(
            "is_condition",
            (22, "loopy(int, int)"),
            {"a": [2],
             "b": [1]})

    def test_in_condition(self):
        self.check_counting_condition(
            "in_condition",
            (47, "in_condition(int, int)"),
            {"a": [1],
             "b": [1],
             "c": [1],
             "d": [1]})

    def test_is_assignee(self):
        self.check_counting_condition(
            "is_assignee",
            (62, "assignation(int, int)"),
            {"a": [3],
             "b": [9]})

    def test_is_assigner(self):
        self.check_counting_condition(
            "is_assigner",
            (62, "assignation(int, int)"),
            {"a": [6],
             "b": [9]})

    def test_loop_content(self):
        self.check_counting_condition(
            "loop_content",
            (22, "loopy(int, int)"),
            {"a": [0],
             "b": [6]})

    def test_is_param(self):
        self.check_counting_condition(
            "is_param",
            (47, "in_condition(int, int)"),
            {"a": [1],
             "b": [1],
             "c": [0],
             "d": [0]})

    def test_in_operation(self):
        self.check_counting_condition(
            "in_sum",
            (89, "arithmetics(int, int)"),
            {"a": [4],
             "b": [3]})

        self.check_counting_condition(
            "in_product",
            (89, "arithmetics(int, int)"),
            {"a": [6],
             "b": [6]})

        self.check_counting_condition(
            "in_binary_operation",
            (89, "arithmetics(int, int)"),
            {"a": [6],
             "b": [2]})


def skip_test():
    try:
        Index.create()
        return False
    except LibclangError as error:
        return str(error)


if __name__ == '__main__':
    unittest.main(verbosity=2)
