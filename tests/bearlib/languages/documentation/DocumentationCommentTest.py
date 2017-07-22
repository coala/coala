import unittest

from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.bearlib.languages.documentation.DocBaseClass import (
    DocBaseClass)
from tests.bearlib.languages.documentation.TestUtils import (
    load_testdata)
from coalib.results.TextPosition import TextPosition


class DocumentationCommentTest(unittest.TestCase):

    Description = DocumentationComment.Description
    Parameter = DocumentationComment.Parameter
    ExceptionValue = DocumentationComment.ExceptionValue
    ReturnValue = DocumentationComment.ReturnValue

    Metadata = DocstyleDefinition.Metadata


class GeneralDocumentationCommentTest(DocumentationCommentTest):

    def test_fields(self):
        c_doxygen = DocstyleDefinition.load('C', 'doxygen')
        uut = DocumentationComment('my doc',
                                   c_doxygen,
                                   ' ',
                                   ('/**', '*', '*/'),
                                   TextPosition(3, 1))

        self.assertEqual(uut.documentation, 'my doc')
        self.assertEqual(uut.language, 'c')
        self.assertEqual(uut.docstyle, 'doxygen')
        self.assertEqual(uut.indent, ' ')
        self.assertEqual(str(uut), 'my doc')
        self.assertEqual(uut.marker, ('/**', '*', '*/'))
        self.assertEqual(uut.position, TextPosition(3, 1))

        python_doxygen = DocstyleDefinition.load('python', 'doxygen')

        python_doxygen_metadata = self.Metadata('@param ', ' ',
                                                '@raises ', ' ',
                                                '@return ')

        uut = DocumentationComment('qwertzuiop',
                                   python_doxygen,
                                   '\t',
                                   ('##', '#', '#'),
                                   None)

        self.assertEqual(uut.documentation, 'qwertzuiop')
        self.assertEqual(uut.language, 'python')
        self.assertEqual(uut.docstyle, 'doxygen')
        self.assertEqual(uut.indent, '\t')
        self.assertEqual(str(uut), 'qwertzuiop')
        self.assertEqual(uut.marker, ('##', '#', '#'))
        self.assertEqual(uut.range, None)
        self.assertEqual(uut.position, None)
        self.assertEqual(uut.metadata, python_doxygen_metadata)

    def test_not_implemented(self):
        raw_docstyle = DocstyleDefinition('nolang', 'nostyle', ('', '', ''),
                                          self.Metadata('', '', '', '', ''))
        not_implemented = DocumentationComment(
            'some docs', raw_docstyle, None, None, None)
        with self.assertRaises(NotImplementedError):
            not_implemented.parse()

    def test_from_metadata(self):
        data = load_testdata('default.py')

        original = list(DocBaseClass.extract(data, 'python', 'default'))

        parsed_docs = [(doc.parse(), doc.marker, doc.indent, doc.position)
                       for doc in original]

        docstyle_definition = DocstyleDefinition.load('python', 'default')

        assembled_docs = [DocumentationComment.from_metadata(
                          doc[0], docstyle_definition, doc[1], doc[2], doc[3])
                          for doc in parsed_docs]

        self.assertEqual(assembled_docs, original)


class PythonDocumentationCommentTest(DocumentationCommentTest):

    def check_docstring(self, docstring, expected=[]):
        self.assertIsInstance(docstring,
                              str,
                              'expected needs to be a string for this test.')

        self.assertIsInstance(expected,
                              list,
                              'expected needs to be a list for this test.')

        python_default = DocstyleDefinition.load('python', 'default')

        doc_comment = DocumentationComment(docstring, python_default,
                                           None, None, None)
        parsed_metadata = doc_comment.parse()
        self.assertEqual(parsed_metadata, expected)

    def test_empty_docstring(self):
        self.check_docstring('', [])

    def test_description(self):
        doc = ' description only '
        self.check_docstring(
            doc, [self.Description(desc=' description only ')])

    def test_params_default(self):
        self.maxDiff = None
        doc = (' :param test:  test description1 \n'
               ' :param test:  test description2 \n')
        expected = [self.Parameter(name='test', desc='  test description1 \n'),
                    self.Parameter(name='test', desc='  test description2 \n')]
        self.check_docstring(doc, expected)

    def test_exception_default(self):
        doc = (' :raises test:  test description1\n'
               ' :raises test:  test description2\n')
        expected = [self.ExceptionValue(name='test',
                                        desc='  test description1\n'),
                    self.ExceptionValue(name='test',
                                        desc='  test description2\n')]
        self.check_docstring(doc, expected)

    def test_return_values_default(self):
        doc = (' :return: something1 \n'
               ' :return: something2 ')
        expected = [self.ReturnValue(desc=' something1 \n'),
                    self.ReturnValue(desc=' something2 ')]
        self.check_docstring(doc, expected)

    def test_python_default(self):
        data = load_testdata('default.py')

        parsed_docs = [doc.parse() for doc in
                       DocBaseClass.extract(data, 'python', 'default')]

        expected = [
            [self.Description(desc='\nModule description.\n\n'
                                   'Some more foobar-like text.\n')],
            [self.Description(desc='\nA nice and neat way of '
                                   'documenting code.\n'),
             self.Parameter(name='radius', desc=' The explosion radius. ')],
            [self.Description(desc='A function that returns 55.')],
            [self.Description(desc='\nDocstring with layouted text.\n\n    '
                                   'layouts inside docs are preserved.'
                                   '\nthis is intended.\n')],
            [self.Description(desc=' Docstring inline with triple quotes.\n'
                                   '    Continues here. ')],
            [self.Description(desc='\nThis is the best docstring ever!\n\n'),
             self.Parameter(name='param1',
                            desc='\n    Very Very Long Parameter '
                                 'description.\n'),
             self.Parameter(name='param2',
                            desc='\n    Short Param description.\n\n'),
             self.ReturnValue(desc=' Long Return Description That Makes No '
                                   'Sense And Will\n         Cut to the Next'
                                   ' Line.\n')],
            [self.Description(desc='\nThis is dummy docstring find '
                                   'function.\n\n'),
             self.Parameter(name='filename',
                            desc='\n    contains filename\n'),
             self.ExceptionValue(name='FileNotFoundError',
                                 desc='\n    raised when the given '
                                      'file name was not found\n\n'),
             self.ReturnValue(desc=' returns all possible docstrings'
                                   ' in a file\n')],
            [self.Description(desc='\nThis returns perimeter '
                                   'of a triangle.   \n\n'),
             self.Parameter(name='side_A',
                            desc='\n    length of side_A       \n'),
             self.Parameter(name='side_B',
                            desc='\n    length of side_B    \n'),
             self.Parameter(name='side_C',
                            desc='\n    length of side_C  \n\n'),
             self.ReturnValue(desc=' returns perimeter\n')],
                   ]

        self.assertEqual(parsed_docs, expected)

    def test_python_doxygen(self):
        data = load_testdata('doxygen.py')

        parsed_docs = [doc.parse() for doc in
                       DocBaseClass.extract(data, 'python', 'doxygen')]

        expected = [
            [self.Description(desc=' @package pyexample\n  Documentation for'
                                   ' this module.\n\n  More details.\n')],
            [self.Description(
                desc=' Documentation for a class.\n\n More details.\n')],
            [self.Description(desc=' The constructor.\n')],
            [self.Description(desc=' Documentation for a method.\n'),
             self.Parameter(name='self', desc='The object pointer.\n')],
            [self.Description(desc=' A class variable.\n')],
            [self.Description(desc=' @var _memVar\n  a member variable\n')],
            [self.Description(desc=' This is the best docstring ever!\n\n'),
             self.Parameter(name='param1', desc='Parameter 1\n'),
             self.Parameter(name='param2', desc='Parameter 2\n'),
             self.ReturnValue(desc='Nothing\n')],
            [self.Description(desc=' This is dummy docstring find '
                                   'function.\n\n'),
             self.Parameter(name='filename', desc='contains filename\n'),
             self.ExceptionValue(name='FileNotFoundError',
                                 desc='raises when filename is not found\n'),
             self.ReturnValue(desc='nothing\n')],
                   ]

        self.assertEqual(parsed_docs, expected)

    def test_python_missing_ending_colon(self):
        doc = (' This is a malformed docstring\n'
               ' :param abc  test description1\n'
               ' :raises xyz  test description2\n')
        expected = [self.Description(desc=' This is a malformed docstring\n'),
                    self.Parameter(name='abc',
                                   desc=' test description1\n'),
                    self.ExceptionValue(name='xyz',
                                        desc=' test description2\n')]
        self.check_docstring(doc, expected)


class JavaDocumentationCommentTest(DocumentationCommentTest):

    def test_java_default(self):
        data = load_testdata('default.java')

        parsed_docs = [doc.parse() for doc in
                       DocBaseClass.extract(data, 'java', 'default')]

        expected = [[self.Description(
                     desc='\n Returns an String that says Hello with the name'
                          ' argument.\n\n'),
                     self.Parameter(name='name',
                                    desc='the name to which to say hello\n'),
                     self.ExceptionValue(name='IOException',
                                         desc='throws IOException\n'),
                     self.ReturnValue(
                         desc='     the concatenated string\n')],
                    [self.Description(
                     desc='\n Returns Area of a square.\n\n'),
                     self.Parameter(name='side', desc='side of square\n'),
                     self.ReturnValue(desc=' area of a square\n')],
                    ]

        self.assertEqual(expected, parsed_docs)


class GoDocumentationCommentTest(DocumentationCommentTest):

    def test_go_default(self):
        data = load_testdata('default.go')

        parsed_docs = [doc.parse() for doc in
                       DocBaseClass.extract(data, 'golang', 'golang')]

        expected = [['\n',
                     'Comments may span\n',
                     'multiple lines\n'],
                    ['A class comment\n',
                     'that also spans\n',
                     'multiple lines\n'],
                    ['More documentation for everyone, but in one line\n']]

        self.assertEqual(expected, parsed_docs)


class DocumentationAssemblyTest(unittest.TestCase):

    def test_python_assembly(self):
        data = load_testdata('default.py')
        docs = ''.join(data)

        for doc in DocBaseClass.extract(data, 'python', 'default'):
            self.assertIn(doc.assemble(), docs)

    def test_doxygen_assembly(self):
        data = load_testdata('doxygen.py')
        docs = ''.join(data)

        for doc in DocBaseClass.extract(data, 'python', 'doxygen'):
            self.assertIn(doc.assemble(), docs)

    def test_c_assembly(self):
        data = load_testdata('default.c')
        docs = ''.join(data)

        for doc in DocBaseClass.extract(data, 'c', 'doxygen'):
            self.assertIn(doc.assemble(), docs)
