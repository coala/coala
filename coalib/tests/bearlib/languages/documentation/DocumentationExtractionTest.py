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


if __name__ == '__main__':
    unittest.main(verbosity=2)
