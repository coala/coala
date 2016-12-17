import unittest

from coalib.bearlib.languages.Language import Language, LanguageMeta


class LanguageTest(unittest.TestCase):

    def test_class__dir__(self):
        assert set(dir(Language)) == {
            l.__name__ for l in LanguageMeta.all
        }.union(type.__dir__(Language))


class LanguageAttributeErrorTest(unittest.TestCase):

    def setUp(self):
        self.lang_cpp = Language['CPP']
        self.lang_unknown = Language['Unknown']

    def tearDown(self):
        pass

    def test_invalid_attribute(self):
        with self.assertRaisesRegexp(AttributeError, 'not a valid attribute'):
            self.lang_cpp.not_an_attribute

    def test_attribute_list_empy(self):
        with self.assertRaisesRegexp(AttributeError, 'no available attribute'):
            self.lang_unknown.not_an_attribute
