import os.path
import unittest
import sys

sys.path.insert(0, ".")
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    extract_documentation,
    extract_documentation_with_docstyle)
from coalib.misc.Compatability import FileNotFoundError
from coalib.results.TextRange import TextRange


class DocumentationExtractionTest(unittest.TestCase):
    def test_extract_documentation_with_docstyle_invalid_input(self):
        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   [["A", "B", "C", "D"]]))

        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   [["A", "B"]]))

        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   [["A"]]))

    def test_extract_documentation_invalid_input(self):
        with self.assertRaises(FileNotFoundError):
            tuple(extract_documentation("", "PYTHON", "INVALID"))

    @staticmethod
    def load_testdata(filename):
        filename = (os.path.dirname(os.path.realpath(__file__)) +
                    "/documentation_extraction_testdata/" + filename)
        with open(filename, "r") as fl:
            data = fl.read()

        return data

    def test_extract_documentation_C(self):
        data = DocumentationExtractionTest.load_testdata("data.c")

        # No built-in documentation for C.
        with self.assertRaises(KeyError):
            tuple(extract_documentation(data, "C", "default"))

        docstyle_C_doxygen = DocstyleDefinition.load("C", "doxygen")

        expected_results = (DocumentationComment(
                                ("\n"
                                 " This is the main function.\n"
                                 "\n"
                                 " @returns Your favorite number.\n"),
                                docstyle_C_doxygen,
                                docstyle_C_doxygen.markers[0],
                                TextRange.from_values(3, 1, 7, 4)),
                            DocumentationComment(
                                ("\n"
                                 " Preserves alignment\n"
                                 " - Main item\n"
                                 "   - sub item\n"
                                 "     - sub sub item\n"),
                                docstyle_C_doxygen,
                                docstyle_C_doxygen.markers[2],
                                TextRange.from_values(15, 1, 20, 4)),
                            DocumentationComment(
                                (" ABC\n"
                                 "    Another type of comment\n"
                                 "\n"
                                 "    ..."),
                                docstyle_C_doxygen,
                                docstyle_C_doxygen.markers[1],
                                TextRange.from_values(23, 1, 26, 11)),
                            DocumentationComment(
                                (" foobar = barfoo.\n"
                                 " @param x whatever...\n"),
                                docstyle_C_doxygen,
                                docstyle_C_doxygen.markers[0],
                                TextRange.from_values(28, 1, 30, 4)))

        self.assertEqual(tuple(extract_documentation(data, "C", "doxygen")),
                         expected_results)

        # Presplitted lines should also work.
        data = data.splitlines(keepends=True)
        self.assertEqual(tuple(extract_documentation(data, "C", "doxygen")),
                         expected_results)

    def test_extract_documentation_CPP(self):
        data = DocumentationExtractionTest.load_testdata("data.cpp")

        # No built-in documentation for C++.
        with self.assertRaises(KeyError):
            tuple(extract_documentation(data, "CPP", "default"))

        docstyle_CPP_doxygen = DocstyleDefinition.load("CPP", "doxygen")

        self.assertEqual(tuple(extract_documentation(data, "CPP", "doxygen")),
                         (DocumentationComment(
                              ("\n"
                               " This is the main function.\n"
                               " @returns Exit code.\n"
                               "          Or any other number.\n"),
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[0],
                              TextRange.from_values(4, 1, 8, 4)),
                          DocumentationComment(
                              (" foobar\n"
                               " @param xyz\n"),
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[0],
                              TextRange.from_values(15, 1, 17, 4)),
                          DocumentationComment(
                              " Some alternate style of documentation\n",
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[4],
                              TextRange.from_values(22, 1, 22, 43)),
                          DocumentationComment(
                              " ends instantly",
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[0],
                              TextRange.from_values(26, 5, 26, 26)),
                          DocumentationComment(
                              (" Should work\n"
                               "\n"
                               " even without a function standing below.\n"
                               "\n"
                               " @param foo WHAT PARAM PLEASE!?\n"),
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[4],
                              TextRange.from_values(32, 1, 36, 36))))

    def test_extract_documentation_CPP_2(self):
        data = DocumentationExtractionTest.load_testdata("data2.cpp")

        docstyle_CPP_doxygen = DocstyleDefinition.load("CPP", "doxygen")

        self.assertEqual(tuple(extract_documentation(data, "CPP", "doxygen")),
                         (DocumentationComment(
                              ("module comment\n"
                               " hello world\n"),
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[0],
                              TextRange.from_values(1, 1, 3, 4)),))

    def test_extract_documentation_PYTHON3(self):
        data = DocumentationExtractionTest.load_testdata("data.py")

        docstyle_PYTHON3_default = DocstyleDefinition.load("PYTHON3",
                                                           "default")
        docstyle_PYTHON3_doxygen = DocstyleDefinition.load("PYTHON3",
                                                           "doxygen")

        expected = (DocumentationComment(
                        ("\n"
                         "Module description.\n"
                         "\n"
                         "Some more foobar-like text.\n"),
                        docstyle_PYTHON3_default,
                        docstyle_PYTHON3_default.markers[0],
                        TextRange.from_values(1, 1, 5, 4)),
                    DocumentationComment(
                        ("\n"
                         "A nice and neat way of documenting code.\n"
                         ":param radius: The explosion radius.\n"),
                        docstyle_PYTHON3_default,
                        docstyle_PYTHON3_default.markers[0],
                        TextRange.from_values(8, 5, 11, 8)),
                    DocumentationComment(
                        ("\n"
                         "Docstring with layouted text.\n"
                         "\n"
                         "    layouts inside docs are preserved for these "
                         "documentation styles.\n"
                         "this is intended.\n"),
                        docstyle_PYTHON3_default,
                        docstyle_PYTHON3_default.markers[0],
                        TextRange.from_values(14, 1, 19, 4)),
                    DocumentationComment(
                        (" Docstring directly besides triple quotes.\n"
                         "    Continues here. "),
                        docstyle_PYTHON3_default,
                        docstyle_PYTHON3_default.markers[0],
                        TextRange.from_values(21, 1, 22, 24)),
                    DocumentationComment(
                        ("super\n"
                         " nicely\n"
                         "short"),
                        docstyle_PYTHON3_default,
                        docstyle_PYTHON3_default.markers[0],
                        TextRange.from_values(35, 1, 37, 9)))

        self.assertEqual(
            tuple(extract_documentation(data, "PYTHON3", "default")),
            expected)

        # Change only the docstyle in expected results.
        expected = list(DocumentationComment(r.documentation,
                                             docstyle_PYTHON3_doxygen,
                                             r.marker,
                                             r.range)
                        for r in expected)

        expected.insert(4, DocumentationComment(
            (" Alternate documentation style in doxygen.\n"
             "  Subtext\n"
             " More subtext (not correctly aligned)\n"
             "      sub-sub-text\n"
             "\n"),
            docstyle_PYTHON3_doxygen,
            docstyle_PYTHON3_doxygen.markers[1],
            TextRange.from_values(25, 1, 29, 3)))

        self.assertEqual(
            list(extract_documentation(data, "PYTHON3", "doxygen")),
            expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
