#! /bin/python3

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

import unittest, sys, os
from codeclib.fillib.util import settings

class TestSettings(unittest.TestCase):

    @unittest.skipIf(sys.version_info < (3, 4), "This test is not supported by python < 3.4")
    def test_accept_possible_arguments(self):

        argument_list = [
        "-d Hallo",
        "-dHallo",
        "-d Hallo Welt",
        "-v",
        "-vs",
        "-t .dif -i foo bar",
        "-c /home/fabian/codec.conf"
        ]

        expected_result_list = [
        {'d':["Hallo"], 'dd':None, 'f':None, 'ff':None, 't':None, 'i':None, 'c':'ccfile', 's':False, 'v':False},
        {'d':["Hallo"], 'dd':None, 'f':None, 'ff':None, 't':None, 'i':None, 'c':'ccfile', 's':False, 'v':False},
        {'d':["Hallo", "Welt"], 'dd':None, 'f':None, 'ff':None, 't':None, 'i':None, 'c':'ccfile', 's':False, 'v':False},
        {'d':None, 'dd':None, 'f':None, 'ff':None, 't':None, 'i':None, 'c':'ccfile', 's':False, 'v':True},
        {'d':None, 'dd':None, 'f':None, 'ff':None, 't':None, 'i':None, 'c':'ccfile', 's':True, 'v':True},
        {'d':None, 'dd':None, 'f':None, 'ff':None, 't':['.dif'], 'i':['foo','bar'], 'c':'ccfile', 's':False, 'v':False},
        {'d':None, 'dd':None, 'f':None, 'ff':None, 't':None, 'i':None, 'c':'/home/fabian/codec.conf', 's':False, 'v':False}
        ]

        # the result should be equal to the expected result in any of these cases
        for i in range(len(argument_list)):
            with self.subTest(i=i):
                self.assertEqual(settings.parse_args(argument_list[i].split()), expected_result_list[i])

    @unittest.skipIf(sys.version_info < (3, 4), "This test is not supported by python < 3.4")
    def test_reject_impossible_arguments(self):

        argument_list = [
        "ti dif",
        "-d",
        "-x",
        "argument",
        "--vs",
        "v"
        ]

        # A SystemExit with code 2 should be raised in any of these cases
        for i in range(len(argument_list)):
            with self.subTest(i=i):
                with self.assertRaises(SystemExit) as SE:
                    args = settings.parse_args(argument_list[i].split())
                self.assertEqual(SE.exception.code, 2)

if __name__ == "__main__":
    unittest.main()