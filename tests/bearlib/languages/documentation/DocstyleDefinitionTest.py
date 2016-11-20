import unittest
from unittest.mock import patch

from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)


class DocstyleDefinitionTest(unittest.TestCase):

    Metadata = DocstyleDefinition.Metadata
    dummy_metadata = Metadata(':param ', ':', ':return:')

    def test_fail_instantation(self):
        with self.assertRaises(ValueError):
            DocstyleDefinition('PYTHON', 'doxyGEN',
                               (('##', '#'),), self.dummy_metadata)

        with self.assertRaises(ValueError):
            DocstyleDefinition('WEIRD-PY',
                               'schloxygen',
                               (('##+', 'x', 'y', 'z'),),
                               self.dummy_metadata)

        with self.assertRaises(ValueError):
            DocstyleDefinition('PYTHON',
                               'doxygen',
                               (('##', '', '#'), ('"""', '"""')),
                               self.dummy_metadata)

        with self.assertRaises(TypeError):
            DocstyleDefinition(123, ['doxygen'], (('"""', '"""')),
                               self.dummy_metadata)

        with self.assertRaises(TypeError):
            DocstyleDefinition('language', ['doxygen'], (('"""', '"""')),
                               'metdata')

    def test_properties(self):
        uut = DocstyleDefinition('C', 'doxygen',
                                 (('/**', '*', '*/'),), self.dummy_metadata)

        self.assertEqual(uut.language, 'c')
        self.assertEqual(uut.docstyle, 'doxygen')
        self.assertEqual(uut.markers, (('/**', '*', '*/'),))
        self.assertEqual(uut.metadata, self.dummy_metadata)

        uut = DocstyleDefinition('PYTHON', 'doxyGEN',
                                 [('##', '', '#')], self.dummy_metadata)

        self.assertEqual(uut.language, 'python')
        self.assertEqual(uut.docstyle, 'doxygen')
        self.assertEqual(uut.markers, (('##', '', '#'),))
        self.assertEqual(uut.metadata, self.dummy_metadata)

        uut = DocstyleDefinition('I2C',
                                 'my-custom-tool',
                                 (['~~', '/~', '/~'], ('>!', '>>', '>>')),
                                 self.dummy_metadata)

        self.assertEqual(uut.language, 'i2c')
        self.assertEqual(uut.docstyle, 'my-custom-tool')
        self.assertEqual(uut.markers, (('~~', '/~', '/~'), ('>!', '>>', '>>')))
        self.assertEqual(uut.metadata, self.dummy_metadata)

        uut = DocstyleDefinition('Cpp', 'doxygen',
                                 ('~~', '/~', '/~'), self.dummy_metadata)

        self.assertEqual(uut.language, 'cpp')
        self.assertEqual(uut.docstyle, 'doxygen')
        self.assertEqual(uut.markers, (('~~', '/~', '/~'),))
        self.assertEqual(uut.metadata, self.dummy_metadata)

    def test_load(self):
        # Test unregistered docstyle.
        with self.assertRaises(FileNotFoundError):
            next(DocstyleDefinition.load('PYTHON', 'INVALID'))

        # Test unregistered language in existing docstyle.
        with self.assertRaises(KeyError):
            next(DocstyleDefinition.load('bake-a-cake', 'default'))

        # Test wrong argument type.
        with self.assertRaises(TypeError):
            next(DocstyleDefinition.load(123, ['list']))

        # Test python 3 default configuration and if everything is parsed
        # right.
        result = DocstyleDefinition.load('PYTHON3', 'default')

        self.assertEqual(result.language, 'python3')
        self.assertEqual(result.docstyle, 'default')
        self.assertEqual(result.markers, (('"""', '', '"""'),))

        self.assertEqual(result.metadata, self.dummy_metadata)

    def test_get_available_definitions(self):
        # Test if the basic supported docstyle-language pairs exist.
        expected = {('default', 'python'),
                    ('default', 'python3'),
                    ('default', 'java'),
                    ('doxygen', 'c'),
                    ('doxygen', 'cpp'),
                    ('doxygen', 'cs'),
                    ('doxygen', 'fortran'),
                    ('doxygen', 'java'),
                    ('doxygen', 'python'),
                    ('doxygen', 'python3'),
                    ('doxygen', 'tcl'),
                    ('doxygen', 'vhdl'),
                    ('doxygen', 'php'),
                    ('doxygen', 'objective-c')}

        real = set(DocstyleDefinition.get_available_definitions())

        self.assertTrue(expected.issubset(real))

    @patch('coalib.bearlib.languages.documentation.DocstyleDefinition.iglob')
    @patch('coalib.bearlib.languages.documentation.DocstyleDefinition'
           '.ConfParser')
    def test_get_available_definitions_on_wrong_files(self,
                                                      confparser_mock,
                                                      iglob_mock):
        # Test the case when a coalang was provided with uppercase letters.
        confparser_instance_mock = confparser_mock.return_value
        confparser_instance_mock.parse.return_value = ['X']
        iglob_mock.return_value = ['some/CUSTOMSTYLE.coalang',
                                   'SOME/xlang.coalang']

        self.assertEqual(list(DocstyleDefinition.get_available_definitions()),
                         [('xlang', 'x')])
