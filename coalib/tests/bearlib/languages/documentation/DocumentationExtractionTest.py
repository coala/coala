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


if __name__ == '__main__':
    unittest.main(verbosity=2)
