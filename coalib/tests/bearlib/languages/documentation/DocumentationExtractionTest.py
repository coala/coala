import os.path
import unittest
import sys

sys.path.insert(0, ".")
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition,
    DOCTYPES)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    extract_documentation,
    extract_documentation_with_docstyle)
from coalib.misc.Compatability import FileNotFoundError


class DocumentationExtractionTest(unittest.TestCase):
    def test_extract_documentation_with_docstyle_invalid_input(self):
        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   DOCTYPES.standard,
                                   ("A", "B", "C", "D")))

        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   DOCTYPES.standard,
                                   ("A", "B")))

        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   DOCTYPES.simple,
                                   ("A",)))

        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   DOCTYPES.simple,
                                   ("A", "B", "C")))

        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   DOCTYPES.continuous,
                                   ("A", "B", "C")))

        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   DOCTYPES.continuous,
                                   ("A",)))

    def test_extract_documentation_invalid_input(self):
        with self.assertRaises(FileNotFoundError):
            tuple(extract_documentation("", "PYTHON", "INVALID"))

    @staticmethod
    def load_testdata(language):
        filename = (os.path.dirname(os.path.realpath(__file__)) +
                    "/documentation_extraction_testdata/data" + language)
        with open(filename, "r") as fl:
            data = fl.read()

        return data

    def test_extract_documentation_C(self):
        data = DocumentationExtractionTest.load_testdata(".c")

        # No built-in documentation for C.
        with self.assertRaises(KeyError):
            tuple(extract_documentation(data, "C", "default"))

        docstyle_C_doxygen = DocstyleDefinition("C",
                                                "doxygen",
                                                DOCTYPES.standard,
                                                ("/**", "*", "*/"))

        self.assertEqual(tuple(extract_documentation(data, "C", "doxygen")),
                         (DocumentationComment(
                              ("\n"
                               " This is the main function.\n"
                               "\n"
                               " @returns Your favorite number.\n"),
                              docstyle_C_doxygen,
                              (21, 95)),
                           DocumentationComment(
                              (" foobar = barfoo.\n"
                               " @param x whatever...\n"),
                              docstyle_C_doxygen,
                              (182, 230))))

    def test_extract_documentation_CPP(self):
        data = DocumentationExtractionTest.load_testdata(".cpp")

        # No built-in documentation for C++.
        with self.assertRaises(KeyError):
            tuple(extract_documentation(data, "CPP", "default"))

        docstyle_CPP_doxygen_standard = DocstyleDefinition(
            "CPP",
            "doxygen",
            DOCTYPES.standard,
            ("/**", "*", "*/"))
        docstyle_CPP_doxygen_continuous = DocstyleDefinition(
            "CPP",
            "doxygen",
            DOCTYPES.continuous,
            ("///", "///"))

        self.assertEqual(tuple(extract_documentation(data, "CPP", "doxygen")),
                         (DocumentationComment(
                              ("\n"
                               " This is the main function.\n"
                               " @returns Exit code.\n"
                               "          Or any other number.\n"),
                              docstyle_CPP_doxygen_standard,
                              (22, 115)),
                          DocumentationComment(
                              (" foobar\n"
                               " @param xyz\n"),
                              docstyle_CPP_doxygen_standard,
                              (174, 202)),
                          DocumentationComment(
                              " Some alternate style of documentation\n",
                              docstyle_CPP_doxygen_continuous,
                              (256, 298)),
                          DocumentationComment(
                              (" Should work\n"
                               "\n"
                               " even without a function standing below.\n"
                               "\n"
                               " @param foo WHAT PARAM PLEASE!?\n"),
                              docstyle_CPP_doxygen_continuous,
                              (324, 427))))

    def test_extract_documentation_PYTHON3(self):
        data = DocumentationExtractionTest.load_testdata(".py")

        docstyle_PYTHON3_default_simple = DocstyleDefinition(
            "PYTHON3",
            "default",
            DOCTYPES.simple,
            ('"""', '"""'))

        docstyle_PYTHON3_doxygen_simple = DocstyleDefinition(
            "PYTHON3",
            "doxygen",
            DOCTYPES.simple,
            ('"""', '"""'))

        docstyle_PYTHON3_doxygen_continuous = DocstyleDefinition(
            "PYTHON3",
            "doxygen",
            DOCTYPES.continuous,
            ("##", "#"))

        expected = (DocumentationComment(
                        ("\n"
                         "Module description.\n"
                         "\n"
                         "Some more foobar-like text.\n"),
                        docstyle_PYTHON3_default_simple,
                        (0, 56)),
                    DocumentationComment(
                        ("\n"
                         "A nice and neat way of documenting code.\n"
                         ":param radius: The explosion radius.\n"),
                        docstyle_PYTHON3_default_simple,
                        (92, 189)),
                    DocumentationComment(
                        ("\n"
                         "Docstring with layouted text.\n"
                         "\n"
                         "layouts inside docs are not preserved for these "
                         "documentation styles.\n"
                         "this is intended.\n"),
                        docstyle_PYTHON3_default_simple,
                        (200, 330)),
                    DocumentationComment(
                        (" Docstring directly besides triple quotes.\n"
                         "Continues here. "),
                        docstyle_PYTHON3_default_simple,
                        (332, 401)))

        self.assertEqual(
            tuple(extract_documentation(data, "PYTHON3", "default")),
            expected)

        # Change only the docstyle in expected results.
        expected = tuple(DocumentationComment(r.documentation,
                                              docstyle_PYTHON3_doxygen_simple,
                                              r.range)
                         for r in expected)
        expected += (DocumentationComment(
                         (" Alternate documentation style in doxygen.\n"
                          "  Subtext\n"
                          " More subtext (not correctly aligned)\n"
                          "      sub-sub-text\n"
                          "\n"),
                      docstyle_PYTHON3_doxygen_continuous,
                      (404, 521)),)

        self.assertEqual(
            tuple(extract_documentation(data, "PYTHON3", "doxygen")),
            expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
