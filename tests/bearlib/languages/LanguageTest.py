import pickle
import unittest

from collections import abc

from coalib.bearlib.languages.Language import Language, Languages, LanguageMeta


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


class LanguagesCollectionDataTypeTest(unittest.TestCase):

    def setUp(self):
        self.expected_langs = (Language['CPP'], Language['Python'])
        self.langs = Languages(self.expected_langs)

    def tearDown(self):
        pass

    def test_collection_data_types(self):
        self.assertTrue(isinstance(self.langs, abc.Mapping))
        self.assertTrue(isinstance(self.langs, abc.Iterable))

    def test_languages_apis(self):
        self.assertEqual(len(self.langs), 2)
        self.assertEqual(self.langs.keys(), [0, 1])
        self.assertIn('CPP', self.langs)
        values = self.langs.values()
        self.assertIn('CPP', values[0])
        self.assertIn('Python', values[1])
        self.assertEqual(len(values), 2)
        items = self.langs.items()
        self.assertEqual(len(items), 2)
        self.assertIn('CPP', self.langs[0])
        self.assertIn('Python', self.langs[1])
        reverse = list(reversed(self.langs))
        self.assertIn('CPP', reverse[1])
        self.assertIn('Python', reverse[0])
        self.assertEqual(self.langs, self.expected_langs)
        langs2 = Languages(self.expected_langs)
        self.assertTrue(self.langs == langs2)
        self.assertFalse(self.langs != langs2)
        self.assertFalse(self.langs == [])
        cnt = 0
        for e in self.langs:
            cnt += 1
        it = iter(self.langs)
        it_cnt = 0
        while True:
            try:
                next(it)
                it_cnt += 1
            except StopIteration:
                break
        self.assertEqual(cnt, 2)
        self.assertEqual(it_cnt, 2)
        self.assertEqual(str(self.langs),
                         '(CPP, Python 2.7, 3.3, 3.4, 3.5, 3.6)')
        self.assertEqual(repr(self.langs),
                         '(CPP, Python 2.7, 3.3, 3.4, 3.5, 3.6)')
        self.assertFalse(self.langs != langs2)
        with self.assertRaises(TypeError):
            del self.langs[0]
        with self.assertRaises(TypeError):
            self.langs[3] = Language['Java']
        with self.assertRaises(TypeError):
            hash(self.langs)
