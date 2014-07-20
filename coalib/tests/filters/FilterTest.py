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
sys.path.append(".")
from coalib.misc import i18n
from coalib.filters.Filter import Filter
import unittest


class TestFilter(Filter):
    pass


class FilterTestCase(unittest.TestCase):
    @staticmethod
    def reload_i18n_lib():
        if sys.version_info < (3, 4):
            imp.reload(i18n)
        else:
            importlib.reload(i18n)

    def setUp(self):
        self.uut = TestFilter()


if __name__ == '__main__':
    unittest.main(verbosity=2)
