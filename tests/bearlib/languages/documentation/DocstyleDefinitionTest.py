import os.path
from tempfile import TemporaryDirectory
import unittest

from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)


class DocstyleDefinitionTest(unittest.TestCase):

    Metadata = DocstyleDefinition.Metadata
    dummy_metadata = Metadata(":param ", ":", ":return:")

    def test_fail_instantation(self):
        with self.assertRaises(ValueError):
            DocstyleDefinition("PYTHON", "doxyGEN",
                               (("##", "#"),), self.dummy_metadata)

        with self.assertRaises(ValueError):
            DocstyleDefinition("WEIRD-PY",
                               "schloxygen",
                               (("##+", "x", "y", "z"),),
                               self.dummy_metadata)

        with self.assertRaises(ValueError):
            DocstyleDefinition("PYTHON",
                               "doxygen",
                               (("##", "", "#"), ('"""', '"""')),
                               self.dummy_metadata)

        with self.assertRaises(TypeError):
            DocstyleDefinition(123, ["doxygen"], (('"""', '"""')),
                               self.dummy_metadata)

        with self.assertRaises(TypeError):
            DocstyleDefinition("language", ["doxygen"], (('"""', '"""')),
                               "metdata")

    def test_properties(self):
        uut = DocstyleDefinition("C", "doxygen",
                                 (("/**", "*", "*/"),), self.dummy_metadata)

        self.assertEqual(uut.language, "c")
        self.assertEqual(uut.docstyle, "doxygen")
        self.assertEqual(uut.markers, (("/**", "*", "*/"),))
        self.assertEqual(uut.metadata, self.dummy_metadata)

        uut = DocstyleDefinition("PYTHON", "doxyGEN",
                                 [("##", "", "#")], self.dummy_metadata)

        self.assertEqual(uut.language, "python")
        self.assertEqual(uut.docstyle, "doxygen")
        self.assertEqual(uut.markers, (("##", "", "#"),))
        self.assertEqual(uut.metadata, self.dummy_metadata)

        uut = DocstyleDefinition("I2C",
                                 "my-custom-tool",
                                 (["~~", "/~", "/~"], (">!", ">>", ">>")),
                                 self.dummy_metadata)

        self.assertEqual(uut.language, "i2c")
        self.assertEqual(uut.docstyle, "my-custom-tool")
        self.assertEqual(uut.markers, (("~~", "/~", "/~"), (">!", ">>", ">>")))
        self.assertEqual(uut.metadata, self.dummy_metadata)

        uut = DocstyleDefinition("Cpp", "doxygen",
                                 ("~~", "/~", "/~"), self.dummy_metadata)

        self.assertEqual(uut.language, "cpp")
        self.assertEqual(uut.docstyle, "doxygen")
        self.assertEqual(uut.markers, (("~~", "/~", "/~"),))
        self.assertEqual(uut.metadata, self.dummy_metadata)

    def test_load(self):
        # Test unregistered docstyle.
        with self.assertRaises(FileNotFoundError):
            next(DocstyleDefinition.load("PYTHON", "INVALID"))

        # Test unregistered language in existing docstyle.
        with self.assertRaises(KeyError):
            next(DocstyleDefinition.load("bake-a-cake", "default"))

        # Test wrong argument type.
        with self.assertRaises(TypeError):
            next(DocstyleDefinition.load(123, ["list"]))

        # Test python 3 default configuration and if everything is parsed
        # right.
        result = DocstyleDefinition.load("PYTHON3", "default")

        self.assertEqual(result.language, "python3")
        self.assertEqual(result.docstyle, "default")
        self.assertEqual(result.markers, (('"""', '', '"""'),))

        self.assertEqual(result.metadata, self.dummy_metadata)

    def test_load_external_coalang(self):
        empty_metadata = self.Metadata('', '', '')
        with TemporaryDirectory() as directory:
            coalang_file = os.path.join(directory, "custom.coalang")
            with open(coalang_file, "w") as file:
                file.write("[COOL]\ndoc-markers = @@,@@,@@\n")

            result = DocstyleDefinition.load(
                "cool", "custom", coalang_dir=directory)
            self.assertEqual(result.language, "cool")
            self.assertEqual(result.docstyle, "custom")
            self.assertEqual(result.markers, (('@@', '@@', '@@'),))
            self.assertEqual(result.metadata, empty_metadata)
