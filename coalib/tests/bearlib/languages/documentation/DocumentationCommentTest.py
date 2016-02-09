import unittest

from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)


class DocumentationCommentTest(unittest.TestCase):

    def test_fields(self):
        uut = DocumentationComment("my doc",
                                   ("/**", "*", "*/"),
                                   (25, 45))

        self.assertEqual(uut.documentation, "my doc")
        self.assertEqual(str(uut), "my doc")
        self.assertEqual(uut.marker, ("/**", "*", "*/"))
        self.assertEqual(uut.range, (25, 45))

        uut = DocumentationComment("qwertzuiop",
                                   ("##", "#", "#"),
                                   None)

        self.assertEqual(uut.documentation, "qwertzuiop")
        self.assertEqual(str(uut), "qwertzuiop")
        self.assertEqual(uut.marker, ("##", "#", "#"))
        self.assertEqual(uut.range, None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
