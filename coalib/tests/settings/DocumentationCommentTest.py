import unittest

from coalib.settings.DocumentationComment import DocumentationComment


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

    def test_str(self):
        uut = DocumentationComment.from_docstring(
            '''
            Description of something. No params.
            ''')

        self.assertEqual(str(uut), "Description of something. No params.")

        uut = DocumentationComment.from_docstring(
            '''
            Description of something with params.

            :param x: Imagine something.
            :param y: x^2
            ''')

        self.assertEqual(str(uut), "Description of something with params.")

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
