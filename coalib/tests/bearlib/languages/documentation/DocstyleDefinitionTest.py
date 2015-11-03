import unittest
import sys

sys.path.insert(0, ".")

from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition,
    DOCTYPES)
from coalib.misc.Compatability import FileNotFoundError
from coalib.settings.Setting import Setting


class DocstyleDefinitionTest(unittest.TestCase):
    def test_get_prefixed_settings(self):
        _get_prefixed_settings = DocstyleDefinition._get_prefixed_settings

        testdict = {"setting1" : Setting("1", "hello"),
                    "setting2" : Setting("2", "no"),
                    "pref_A" : Setting("3", "Q"),
                    "pref_B" : Setting("4", "value"),
                    "arbitrary" : Setting("5", "ABC"),
                    "pref_CDE" : Setting("6", "FGH"),
                    "super" : Setting("7", "+1")}

        self.assertEqual(_get_prefixed_settings(testdict, "pref"),
                         {"pref_A" : Setting("3", "Q"),
                          "pref_B" : Setting("4", "value"),
                          "pref_CDE" : Setting("6", "FGH")})

        self.assertEqual(_get_prefixed_settings(testdict, "setting"),
                         {"setting1" : Setting("1", "hello"),
                          "setting2" : Setting("2", "no")})

        self.assertEqual(_get_prefixed_settings(testdict, "arbitrary"),
                         {"arbitrary" : Setting("5", "ABC")})

        self.assertEqual(_get_prefixed_settings(testdict, "Q"), {})

        self.assertEqual(_get_prefixed_settings(testdict, "s"),
                         {"setting1" : Setting("1", "hello"),
                          "setting2" : Setting("2", "no"),
                          "super" : Setting("7", "+1")})

    def test_properties(self):
        uut = DocstyleDefinition("C",
                                 "doxygen",
                                 DOCTYPES.standard,
                                 ("/**", "*", "*/"))

        self.assertEqual(uut.language, "c")
        self.assertEqual(uut.docstyle, "doxygen")
        self.assertEqual(uut.doctype, DOCTYPES.standard)
        self.assertEqual(uut.markers, ("/**", "*", "*/"))

        uut = DocstyleDefinition("PYTHON",
                                 "doxyGEN",
                                 DOCTYPES.continuous,
                                 ("##", "#"))

        self.assertEqual(uut.language, "python")
        self.assertEqual(uut.docstyle, "doxygen")
        self.assertEqual(uut.doctype, DOCTYPES.continuous)
        self.assertEqual(uut.markers, ("##", "#"))

        uut = DocstyleDefinition("I2C",
                                 "my-custom-tool",
                                 DOCTYPES.simple,
                                 ("~~", "/~"))

        self.assertEqual(uut.language, "i2c")
        self.assertEqual(uut.docstyle, "my-custom-tool")
        self.assertEqual(uut.doctype, DOCTYPES.simple)
        self.assertEqual(uut.markers, ("~~", "/~"))

    def test_load(self):
        # Test unregistered docstyle.
        with self.assertRaises(FileNotFoundError):
            next(DocstyleDefinition.load("PYTHON", "INVALID"))

        # Test unregistered language in existing docstyle.
        with self.assertRaises(KeyError):
            next(DocstyleDefinition.load("bake-a-cake", "default"))

        # Test python 3 default configuration and if everything is parsed
        # right.
        result = tuple(DocstyleDefinition.load("PYTHON3", "default"))
        self.assertEqual(len(result), 1)

        self.assertEqual(result[0].language, "python3")
        self.assertEqual(result[0].docstyle, "default")
        self.assertEqual(result[0].doctype, DOCTYPES.simple)
        self.assertEqual(result[0].markers, ('"""', '"""'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
