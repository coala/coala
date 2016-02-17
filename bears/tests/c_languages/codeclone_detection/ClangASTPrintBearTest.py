import os
import unittest
from queue import Queue

from clang.cindex import TranslationUnitLoadError

from bears.c_languages.codeclone_detection.ClangASTPrintBear import (
    ClangASTPrintBear)
from bears.tests.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section


@generate_skip_decorator(ClangASTPrintBear)
class ClangASTPrintBearTest(unittest.TestCase):

    def setUp(self):
        testfile = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "sample.c"))
        self.queue = Queue()
        with open(testfile) as file:
            testfile_lines = file.readlines()
        self.uut = ClangASTPrintBear({testfile: testfile_lines},
                                     Section("name"),
                                     self.queue)

    def test_run(self):
        self.uut.run()
        with self.assertRaises(TranslationUnitLoadError):
            old_file_dict = self.uut.file_dict
            self.uut.file_dict = {"notexistant": []}
            self.uut.run()
            self.uut.file_dict = old_file_dict

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

        self.uut.run()

        ast = "\n"
        # Only check beginning of AST
        for i in range(expected_ast.count("\n")-1):
            ast += self.queue.get(timeout=0).message + "\n"

        self.assertEqual(ast, expected_ast)
