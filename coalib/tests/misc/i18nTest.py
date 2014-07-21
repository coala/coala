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
if sys.version_info < (3, 4):
    import imp
else:
    import importlib

import unittest
import os
from coalib.misc import i18n


class i18nTestCase(unittest.TestCase):
    @staticmethod
    def reload_i18n_lib():
        if sys.version_info < (3, 4):
            imp.reload(i18n)
        else:
            importlib.reload(i18n)

    def test_de(self):
        os.environ["LANG"] = "de_DE.UTF8"
        self.reload_i18n_lib()
        # Do not change this translation without changing it in the code also!
        self.assertEqual(i18n._("A string to test translations."), "Eine Zeichenkette um Übersetzungen zu testen.")

    def test_unknown(self):
        os.environ["LANG"] = "unknown_language.UTF8"
        self.reload_i18n_lib()
        self.assertEqual(i18n._("A string to test translations."), "A string to test translations.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
