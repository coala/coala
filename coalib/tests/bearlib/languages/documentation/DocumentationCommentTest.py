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


if __name__ == '__main__':
    unittest.main(verbosity=2)
