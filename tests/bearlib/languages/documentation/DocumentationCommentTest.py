import unittest

from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)


class DocumentationCommentTest(unittest.TestCase):

    def test_fields(self):
        uut = DocumentationComment("my doc",
                                   "c",
                                   "default",
                                   " ",
                                   ("/**", "*", "*/"),
                                   (25, 45))

        self.assertEqual(uut.documentation, "my doc")
        self.assertEqual(uut.language, "c")
        self.assertEqual(uut.docstyle, "default")
        self.assertEqual(uut.indent, " ")
        self.assertEqual(str(uut), "my doc")
        self.assertEqual(uut.marker, ("/**", "*", "*/"))
        self.assertEqual(uut.range, (25, 45))

        uut = DocumentationComment("qwertzuiop",
                                   "python",
                                   "doxygen",
                                   "\t",
                                   ("##", "#", "#"),
                                   None)

        self.assertEqual(uut.documentation, "qwertzuiop")
        self.assertEqual(uut.language, "python")
        self.assertEqual(uut.docstyle, "doxygen")
        self.assertEqual(uut.indent, "\t")
        self.assertEqual(str(uut), "qwertzuiop")
        self.assertEqual(uut.marker, ("##", "#", "#"))
        self.assertEqual(uut.range, None)
