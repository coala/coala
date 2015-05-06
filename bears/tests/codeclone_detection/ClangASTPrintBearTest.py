from queue import Queue
import sys
import unittest
import os
import inspect

sys.path.insert(0, ".")

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.codeclone_detection.ClangASTPrintBear import ClangASTPrintBear
from coalib.bearlib.parsing.clang.cindex import Index, LibclangError
from coalib.settings.Section import Section


class SpaceConsistencyBearTest(LocalBearTestHelper):
    def setUp(self):
        self.testfile = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SpaceConsistencyBearTest)),
            "sample.c"))
        self.queue = Queue()
        self.uut = ClangASTPrintBear(Section("name"), self.queue)

    def test_run(self):
        self.uut.run(self.testfile, [])
        with self.assertRaises(AssertionError):
            self.uut.run("notexistant", [])

    def test_ast(self):
        expected_ast = \
            """
|-stdio.h CursorKind.INCLUSION_DIRECTIVE Lines 2-2 (# include < stdio . h > #)
|-not_existant.c CursorKind.INCLUSION_DIRECTIVE Lines 3-3 (# include """ + \
            """"not_existant.c" // Empty function)
|-test() CursorKind.FUNCTION_DECL Lines 6-6 (int test ( void ) ;)
|-g CursorKind.VAR_DECL Lines 9-9 (int g ;)
"""

        self.uut.run(self.testfile, [])

        ast = "\n"
        # Only check beginning of AST
        for i in range(expected_ast.count("\n")-1):
            ast += self.queue.get(timeout=0).message + "\n"

        self.assertEqual(ast, expected_ast)


def skip_test():
    try:
        Index.create()
        return False
    except LibclangError as error:
        return str(error)


if __name__ == '__main__':
    unittest.main(verbosity=2)
