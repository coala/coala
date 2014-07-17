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
sys.path.append(".")
from coalib.fillib.misc.LogMessage import LogMessage, LOG_LEVEL
import unittest


class LogMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = LogMessage()

    def test_to_str(self):
        self.uut.message = "test message änd umlauts!"
        self.uut.log_level = LOG_LEVEL.ERROR
        self.assertEqual(str(self.uut), "[ERROR] test message änd umlauts!")


if __name__ == '__main__':
    unittest.main()
