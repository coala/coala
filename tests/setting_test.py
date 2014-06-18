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
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest
from codeclib.fillib.util.setting import Setting


class SettingTest(unittest.TestCase):
    def setUp(self):
        self.test_instance = Setting('TestKey',
                                     ['TestValue', ''],
                                     trailing_comment="testcomment",
                                     comments_before=["beforecomment", ""])

    def test_line_generation(self):
        lines = self.test_instance.generate_lines()
        self.assertEqual(lines, [
            '# beforecomment',
            '',
            'TestKey = TestValue,  # testcomment'
        ], "Line generation does not work!")
