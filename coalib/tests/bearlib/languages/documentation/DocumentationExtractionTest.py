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


if __name__ == '__main__':
    unittest.main(verbosity=2)
