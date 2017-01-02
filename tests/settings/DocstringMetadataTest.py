import unittest

from coalib.settings.DocstringMetadata import DocstringMetadata
from collections import OrderedDict


class DocstringMetadataTest(unittest.TestCase):

    def test_from_docstring(self):
        self.check_from_docstring_dataset('')
        self.check_from_docstring_dataset(' description only ',
                                          desc='description only')
        self.check_from_docstring_dataset(' :param test:  test description ',
                                          param_dict={
                                              'test': 'test description'})
        self.check_from_docstring_dataset(' @param test:  test description ',
                                          param_dict={
                                              'test': 'test description'})
        self.check_from_docstring_dataset(' :return: something ',
                                          retval_desc='something')
        self.check_from_docstring_dataset(' @return: something ',
                                          retval_desc='something')
        self.check_from_docstring_dataset("""
        Main description

        @param p1: this is

        a multiline desc for p1

        :param p2: p2 description

        @return: retval description
        :return: retval description
        override
        """, desc='Main description', param_dict={
            'p1': 'this is\na multiline desc for p1\n',
            'p2': 'p2 description\n'
        }, retval_desc='retval description override')

    def test_str(self):
        uut = DocstringMetadata.from_docstring(
            '''
            Description of something. No params.
            ''')

        self.assertEqual(str(uut), 'Description of something. No params.')

        uut = DocstringMetadata.from_docstring(
            '''
            Description of something with params.

            :param x: Imagine something.
            :param y: x^2
            ''')

        self.assertEqual(str(uut), 'Description of something with params.')

    def test_unneeded_docstring_space(self):
        uut = DocstringMetadata.from_docstring(
            """
            This is a description about some bear which does some amazing
            things. This is a multiline description for this testcase.

            :param language:
                The programming language.
            :param coalang_dir:
                External directory for coalang file.
            """)

        expected_output = OrderedDict([('language', ('The programming '
                                                     'language.')),
                                       ('coalang_dir', ('External directory '
                                                        'for coalang file.'))])

        self.assertEqual(uut.param_dict, expected_output)

    def check_from_docstring_dataset(self,
                                     docstring,
                                     desc='',
                                     param_dict=None,
                                     retval_desc=''):
        param_dict = param_dict or {}

        self.assertIsInstance(docstring,
                              str,
                              'docstring needs to be a string for this test.')
        doc_comment = DocstringMetadata.from_docstring(docstring)
        self.assertEqual(doc_comment.desc, desc)
        self.assertEqual(doc_comment.param_dict, param_dict)

        self.assertEqual(doc_comment.retval_desc, retval_desc)
