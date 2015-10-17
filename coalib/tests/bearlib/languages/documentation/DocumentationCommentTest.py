import unittest
import sys

sys.path.insert(0, ".")
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition,
    DOCTYPES)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)


class DocumentationCommentTest(unittest.TestCase):
    def test_fields(self):
        docdef = DocstyleDefinition("C",
                                    "doxygen",
                                    DOCTYPES.standard,
                                    ("/**", "*", "*/"))

        uut = DocumentationComment("my doc", docdef, (25, 45))

        self.assertEqual(uut.documentation, "my doc")
        self.assertEqual(str(uut), "my doc")
        self.assertEqual(uut.docstyle, docdef)
        self.assertEqual(uut.range, (25, 45))

        docdef = DocstyleDefinition("PYTHON",
                                    "doxygen",
                                    DOCTYPES.continuous,
                                    ("##", "#"))

        uut = DocumentationComment("qwertzuiop", docdef, None)

        self.assertEqual(uut.documentation, "qwertzuiop")
        self.assertEqual(str(uut), "qwertzuiop")
        self.assertEqual(uut.docstyle, docdef)
        self.assertEqual(uut.range, None)

    def test_equal(self):
        docdef = DocstyleDefinition("C",
                                    "super-linter-tool",
                                    DOCTYPES.continuous,
                                    ("///", "//"))
        uut = DocumentationComment("documentation", docdef, (12, 44))
        uut2 = DocumentationComment("documentation", docdef, (12, 44))

        self.assertNotEqual(uut, None)
        self.assertEqual(uut, uut)
        self.assertEqual(uut, uut2)
        self.assertEqual(uut2, uut)

        uut2 = DocumentationComment("X", docdef, (12, 44))

        self.assertNotEqual(uut, uut2)
        self.assertNotEqual(uut2, uut)

        uut2 = DocumentationComment("documentation", None, (12, 44))

        self.assertNotEqual(uut, uut2)
        self.assertNotEqual(uut2, uut)

        uut2 = DocumentationComment("documentation", docdef, (3, 17))

        self.assertNotEqual(uut, uut2)
        self.assertNotEqual(uut2, uut)


if __name__ == '__main__':
    unittest.main(verbosity=2)
