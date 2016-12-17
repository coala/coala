import unittest

from coalib.bearlib.languages.Language import Language, LanguageMeta


class LanguageTest(unittest.TestCase):

    def test_class__dir__(self):
        assert set(dir(Language)) == {
            l.__name__ for l in LanguageMeta.all
        }.union(type.__dir__(Language))
