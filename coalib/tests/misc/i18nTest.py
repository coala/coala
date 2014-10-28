"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import sys

sys.path.insert(0, ".")
if sys.version_info < (3, 4):
    import imp
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
        os.environ["LANG"] = lang
        if sys.version_info < (3, 4):
            imp.reload(i18n)
        else:
            importlib.reload(i18n)

    def test_de(self):
        self.set_lang("de_DE.UTF8")
        # Do not change this translation without changing it in the code also!
        self.assertEqual(i18n._("A string to test translations."), "Eine Zeichenkette um Übersetzungen zu testen.")

    def test_unknown(self):
        self.set_lang("unknown_language.UTF8")
        self.assertEqual(i18n._("A string to test translations."), "A string to test translations.")

    def test_get_locale(self):
        self.set_lang("unknown_language")
        self.assertEqual(i18n.get_locale(), "en_US")


if __name__ == '__main__':
    unittest.main(verbosity=2)
