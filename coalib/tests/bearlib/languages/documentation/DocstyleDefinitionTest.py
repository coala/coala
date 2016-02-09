import unittest

from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)


class DocstyleDefinitionTest(unittest.TestCase):

    def test_fail_instantation(self):
        with self.assertRaises(ValueError):
            DocstyleDefinition("PYTHON", "doxyGEN", (("##", "#"),))

        with self.assertRaises(ValueError):
            DocstyleDefinition("WEIRD-PY",
                               "schloxygen",
                               (("##+", "x", "y", "z"),))

        with self.assertRaises(ValueError):
            DocstyleDefinition("PYTHON",
                               "doxygen",
                               (("##", "", "#"), ('"""', '"""')))

        with self.assertRaises(TypeError):
            DocstyleDefinition(123, ["doxygen"], (('"""', '"""')))

    def test_properties(self):
        uut = DocstyleDefinition("C", "doxygen", (("/**", "*", "*/"),))

        self.assertEqual(uut.language, "c")
        self.assertEqual(uut.docstyle, "doxygen")
        self.assertEqual(uut.markers, (("/**", "*", "*/"),))

        uut = DocstyleDefinition("PYTHON", "doxyGEN", [("##", "", "#")])

        self.assertEqual(uut.language, "python")
        self.assertEqual(uut.docstyle, "doxygen")
        self.assertEqual(uut.markers, (("##", "", "#"),))

        uut = DocstyleDefinition("I2C",
                                 "my-custom-tool",
                                 (["~~", "/~", "/~"], (">!", ">>", ">>")))

        self.assertEqual(uut.language, "i2c")
        self.assertEqual(uut.docstyle, "my-custom-tool")
        self.assertEqual(uut.markers, (("~~", "/~", "/~"), (">!", ">>", ">>")))

        uut = DocstyleDefinition("Cpp", "doxygen", ("~~", "/~", "/~"))

        self.assertEqual(uut.language, "cpp")
        self.assertEqual(uut.docstyle, "doxygen")
        self.assertEqual(uut.markers, (("~~", "/~", "/~"),))

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
