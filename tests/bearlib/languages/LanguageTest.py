import pickle
import unittest

from coalib.bearlib.languages.Language import Language, LanguageMeta
from tests.TestUtilities import LANGUAGE_NAMES


class LanguageTest(unittest.TestCase):

    def test_class__dir__(self):
        assert set(dir(Language)) == {
            l.__name__ for l in LanguageMeta.all
        }.union(type.__dir__(Language))

    def test_pickle_ability(self):
        cpp = Language['CPP']
        cpp_str = pickle.dumps(cpp)
        cpp_unpickled = pickle.loads(cpp_str)
        self.assertEqual(str(cpp), str(cpp_unpickled))

    def test_contains_method(self):
        # Test alias
        self.assertTrue('py' in Language[Language.Python])
        # Test version
        self.assertTrue('python' in Language[Language.Python == 3])
        # Test string parse
        self.assertTrue('python' in Language['python 3'])
        # Test version exclusion
        self.assertFalse('py 2' in Language['py 3'])
        # More complex version exclusion test
        self.assertFalse('py 2.7, 3.4' in Language['py 3'])


class LanguageAttributeErrorTest(unittest.TestCase):

    def setUp(self):
        self.lang_cpp = Language['CPP']
        self.lang_unknown = Language['Unknown']

    def tearDown(self):
        pass

    def test_invalid_attribute(self):
        with self.assertRaisesRegex(AttributeError, 'not a valid attribute'):
            self.lang_cpp.not_an_attribute

    def test_attribute_list_empy(self):
        with self.assertRaisesRegex(AttributeError, 'no available attribute'):
            self.lang_unknown.not_an_attribute


class LanguageAttributeTypeTest(unittest.TestCase):

    def setUp(self):
        self.languages = []
        for language_name in LANGUAGE_NAMES:
            version = Language[language_name].get_default_version()
            self.languages.append(Language[version])

    def test_comment_delimiters_type(self):
        for language in self.languages:
            attributes = language.attributes
            if 'comment_delimiters' in attributes:
                self.assertIsInstance(language.comment_delimiters,
                                      tuple)

    def test_multiline_comment_delimiters_type(self):
        for language in self.languages:
            attributes = language.attributes
            if 'multiline_comment_delimiters' in attributes:
                self.assertIsInstance(
                    language.multiline_comment_delimiters, dict)

    def test_extensions_type(self):
        for language in self.languages:
            attributes = language.attributes
            if 'extensions' in attributes:
                self.assertIsInstance(language.extensions, tuple)

    def test_string_delimiters_type(self):
        for language in self.languages:
            attributes = language.attributes
            if 'string_delimiters' in attributes:
                self.assertIsInstance(language.string_delimiters, dict)

    def test_encapsulators_type(self):
        for language in self.languages:
            attributes = language.attributes
            if 'encapsulators' in attributes:
                self.assertIsInstance(language.encapsulators, dict)

    def test_indent_types_type(self):
        for language in self.languages:
            attributes = language.attributes
            if 'indent_types' in attributes:
                self.assertIsInstance(language.indent_types, dict)
