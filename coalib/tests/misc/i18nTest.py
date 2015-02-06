import gettext
import sys
import unittest
import os
import shutil

sys.path.insert(0, ".")
if sys.version_info < (3, 4):
    import imp as importlib
else:
    import importlib

# Only use non-installed locales, do this before importing i18n
gettext._default_localedir = os.path.abspath(os.path.join("build", "locale"))
from coalib.misc import i18n

print("Testing translation building...")
shutil.rmtree("build", ignore_errors=True)
i18n.compile_translations(True)
i18n.compile_translations(False)


class i18nTestCase(unittest.TestCase):
    @staticmethod
    def set_lang(lang):
        os.environ["LANGUAGE"] = lang
        os.environ["LC_ALL"] = lang
        os.environ["LC_MESSAGES"] = lang
        os.environ["LANG"] = lang

        importlib.reload(i18n)

    def test_de(self):
        self.set_lang("de_DE.UTF8")
        # Do not change this translation without changing it in the code also!
        self.assertEqual(i18n._("A string to test translations."),
                         "Eine Zeichenkette um Übersetzungen zu testen.")

    def test_unknown(self):
        self.set_lang("unknown_language")
        self.assertEqual(i18n._("A string to test translations."),
                         "A string to test translations.")

    def test_translation_marking(self):
        self.set_lang("de_DE.UTF8")
        string = "A not directly translated test string."
        self.assertEqual(i18n.N_("A not directly translated test string."),
                         string)
        self.assertEqual(i18n._(string),
                         "Ein indirekt übersetzter test String.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
