import os
import unittest
from queue import Queue

from bears.tests.BearTestHelper import generate_skip_decorator
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.c_languages.codeclone_detection.ClangASTPrintBear import (
    ClangASTPrintBear)
from clang.cindex import TranslationUnitLoadError
from coalib.settings.Section import Section


@generate_skip_decorator(ClangASTPrintBear)
class ClangASTPrintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.testfile = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "sample.c"))
        self.queue = Queue()
        self.uut = ClangASTPrintBear(Section("name"), self.queue)

    def test_run(self):
        self.uut.run(self.testfile, [])
        with self.assertRaises(TranslationUnitLoadError):
            self.uut.run("notexistant", [])

    def test_ast(self):
        expected_ast = (
            """
|-stdio.h CursorKind.INCLUSION_DIRECTIVE Lines 2-2 (# include < stdio . h > #)
|-not_existant.c CursorKind.INCLUSION_DIRECTIVE Lines 3-3 (# include """
            """"not_existant.c" // Empty function)
|-test() CursorKind.FUNCTION_DECL Lines 6-6 (int test ( void ) ;)
|-g CursorKind.VAR_DECL Lines 9-9 (int g ;)
`-main(int, char *) CursorKind.FUNCTION_DECL Lines 12-30 (int main ( """
            """int t , char * args ) { // Usage in a call smile ( t , g ) ; """
            """// Simple stupid assignment t = g ; // Local declaration int """
            """* asd ; // Simple more stupid reassignment, this time using """
            """other syntax elems t = args [ g ] ; // Declaration in for """
            """loop for ( int i ; i < 5 ; i ++ ) { // Checking out constants"""
            """ printf ( "i is %d" , i ) ; } })\n""")

        self.uut.run(self.testfile, [])

        ast = "\n"
        # Only check beginning of AST
        for i in range(expected_ast.count("\n")-1):
            ast += self.queue.get(timeout=0).message + "\n"

        self.assertEqual(ast, expected_ast)


if __name__ == '__main__':
    unittest.main(verbosity=2)
