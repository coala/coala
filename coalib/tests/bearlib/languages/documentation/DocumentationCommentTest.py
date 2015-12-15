import unittest
import sys

sys.path.insert(0, ".")
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)


class DocumentationCommentTest(unittest.TestCase):
    def test_fields(self):
        docdef = DocstyleDefinition("C", "doxygen", (("/**", "*", "*/"),))

        uut = DocumentationComment("my doc",
                                   docdef,
                                   ("/**", "*", "*/"),
                                   (25, 45))

        self.assertEqual(uut.documentation, "my doc")
        self.assertEqual(str(uut), "my doc")
        self.assertIs(uut.docstyle, docdef)
        self.assertEqual(uut.marker, ("/**", "*", "*/"))
        self.assertEqual(uut.range, (25, 45))

        docdef = DocstyleDefinition("PYTHON", "doxygen", (("##", "#", "#"),))

        uut = DocumentationComment("qwertzuiop",
                                   docdef,
                                   ("##", "#", "#"),
                                   None)

        self.assertEqual(uut.documentation, "qwertzuiop")
        self.assertEqual(str(uut), "qwertzuiop")
        self.assertIs(uut.docstyle, docdef)
        self.assertEqual(uut.marker, ("##", "#", "#"))
        self.assertEqual(uut.range, None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
