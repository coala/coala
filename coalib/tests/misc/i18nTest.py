import locale
import sys

sys.path.insert(0, ".")
if sys.version_info < (3, 4):
    import imp as importlib
else:
    import importlib

import unittest
import os
import shutil
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
        self.assertEqual(i18n._("A string to test translations."), "Eine Zeichenkette um Übersetzungen zu testen.")

    def test_unknown(self):
        self.set_lang("unknown_language")
        self.assertEqual(i18n._("A string to test translations."), "A string to test translations.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
