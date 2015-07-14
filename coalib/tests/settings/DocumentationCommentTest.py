import sys
import unittest
import subprocess

sys.path.insert(0, ".")

from coalib.settings.DocumentationComment import DocumentationComment
from coalib.tests.misc.i18nTest import i18nTest


class DocumentationCommentParserTest(unittest.TestCase):
    def test_from_docstring(self):
        self.check_from_docstring_dataset("")
        self.check_from_docstring_dataset(" description only ",
                                          desc="description only")
        self.check_from_docstring_dataset(" :param test:  test description ",
                                          param_dict={
            "test": "test description"})
        self.check_from_docstring_dataset(" @param test:  test description ",
                                          param_dict={
            "test": "test description"})
        self.check_from_docstring_dataset(" :return: something ",
                                          retval_desc="something")
        self.check_from_docstring_dataset(" @return: something ",
                                          retval_desc="something")
        self.check_from_docstring_dataset("""
        Main description

        @param p1: this is
        a multiline desc for p1

        main description continues.
        :param p2: p2 description

        @return: retval description
        :return: retval description
        override
        """, desc="Main description main description continues.", param_dict={
            "p1": "this is a multiline desc for p1",
            "p2": "p2 description"
        }, retval_desc="retval description override")

    def test_translation(self):
        i18nTest.set_lang("de_DE.UTF8")
        self.check_from_docstring_dataset(
            '''
            Test description. Do not translate except german.

            @param p1: A param.
            ''',
            desc="Testbeschreibung. Nicht in Sprachen außer Deutsch "
                 "übersetzen.",
            param_dict={"p1": "Ein parameter."})

    def check_from_docstring_dataset(self,
                                     docstring,
                                     desc="",
                                     param_dict=None,
                                     retval_desc=""):
        param_dict = param_dict or {}

        self.assertIsInstance(docstring,
                              str,
                              "docstring needs to be a string for this test.")
        doc_comment = DocumentationComment.from_docstring(docstring)
        self.assertEqual(doc_comment.desc, desc)
        self.assertEqual(doc_comment.param_dict, param_dict)
        self.assertEqual(doc_comment.retval_desc, retval_desc)


def skip_test():
    try:
        subprocess.Popen(['msgfmt'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "msgfmt is not installed."


if __name__ == '__main__':
    unittest.main(verbosity=2)
