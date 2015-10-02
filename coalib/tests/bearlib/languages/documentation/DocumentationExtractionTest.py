import os.path
import unittest
import sys

sys.path.insert(0, ".")

from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    _get_prefixed_settings,
    extract_documentation)


class DocumentationExtractionTest(unittest.TestCase):
    def test_get_prefixed_settings(self):
        testdict = {"setting1" : "hello",
                    "setting2" : "no",
                    "pref_A" : "Q",
                    "pref_B" : "value",
                    "arbitrary" : "ABC",
                    "pref_CDE" : "FGH",
                    "super" : "+1"}

        self.assertEqual(_get_prefixed_settings(testdict, "pref"),
                         {"pref_A" : "Q",
                          "pref_B" : "value",
                          "pref_CDE" : "FGH"})

        self.assertEqual(_get_prefixed_settings(testdict, "setting"),
                         {"setting1" : "hello",
                          "setting2" : "no"})

        self.assertEqual(_get_prefixed_settings(testdict, "arbitrary"),
                         {"arbitrary" : "ABC"})

        self.assertEqual(_get_prefixed_settings(testdict, "Q"), {})

        self.assertEqual(_get_prefixed_settings(testdict, "s"),
                         {"setting1" : "hello",
                          "setting2" : "no",
                          "super" : "+1"})

    def test_extract_documentation_basic(self):
        # Test unregistered docstyle.
        with self.assertRaises(KeyError):
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

        self.assertEqual(tuple(extract_documentation(data, "C", "doxygen")),
                         (("\n"
                           " This is the main function.\n"
                           "\n"
                           " @returns Your favorite number.\n"),
                          (" foobar = barfoo.\n"
                           " @param x whatever...\n")))

    def test_extract_documentation_CPP(self):
        data = DocumentationExtractionTest.load_testdata(".cpp")

        # No built-in documentation for C++.
        with self.assertRaises(KeyError):
            tuple(extract_documentation(data, "CPP", "default"))

        self.assertEqual(tuple(extract_documentation(data, "CPP", "doxygen")),
                         (("\n"
                           " This is the main function.\n"
                           " @returns Exit code.\n"
                           "          Or any other number.\n"),
                          (" foobar\n"
                           " @param xyz\n"),
                          (" Some alternate style of documentation\n"),
                          (" Should work\n"
                           "\n"
                           " even without a function standing below.\n"
                           "\n"
                           " @param foo WHAT PARAM PLEASE!?\n")))


if __name__ == '__main__':
    unittest.main(verbosity=2)
