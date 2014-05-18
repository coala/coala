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

    def setUp(self):
        # passing None will result in error because "test" from "setup.py test" will be interpreted
        self.Settings = settings.Settings(['-v'])

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
        {'TargetLocations':["Hallo"],
        'RecursiveTargetLocations':None,
        'Filters':None,
        'FilterMatches':None,
        'CheckedFileTypes':None,
        'IgnoredFileTypes':None,
        'ConfigLocation':None,
        'SaveSettings':False,
        'Verbosity':False},

        {'TargetLocations':["Hallo"],
        'RecursiveTargetLocations':None,
        'Filters':None,
        'FilterMatches':None,
        'CheckedFileTypes':None,
        'IgnoredFileTypes':None,
        'ConfigLocation':None,
        'SaveSettings':False,
        'Verbosity':False},

        {'TargetLocations':["Hallo", "Welt"],
         'RecursiveTargetLocations':None,
         'Filters':None,
         'FilterMatches':None,
         'CheckedFileTypes':None,
         'IgnoredFileTypes':None,
         'ConfigLocation':None,
         'SaveSettings':False,
         'Verbosity':False},

        {'TargetLocations':None,
         'RecursiveTargetLocations':None,
         'Filters':None,
         'FilterMatches':None,
         'CheckedFileTypes':None,
         'IgnoredFileTypes':None,
         'ConfigLocation':None,
         'SaveSettings':False,
         'Verbosity':True},

        {'TargetLocations':None,
         'RecursiveTargetLocations':None,
         'Filters':None,
         'FilterMatches':None,
         'CheckedFileTypes':None,
         'IgnoredFileTypes':None,
         'ConfigLocation':None,
         'SaveSettings':True,
         'Verbosity':True},

        {'TargetLocations':None,
         'RecursiveTargetLocations':None,
         'Filters':None,
         'FilterMatches':None,
         'CheckedFileTypes':['.dif'],
         'IgnoredFileTypes':['foo','bar'],
         'ConfigLocation':None,
         'SaveSettings':False,
         'Verbosity':False},

        {'TargetLocations':None,
         'RecursiveTargetLocations':None,
         'Filters':None,
         'FilterMatches':None,
         'CheckedFileTypes':None,
         'IgnoredFileTypes':None,
         'ConfigLocation':'/home/fabian/codec.conf',
         'SaveSettings':False,
         'Verbosity':False}
        ]

        # the result should be equal to the expected result in any of these cases
        for i in range(len(argument_list)):
            with self.subTest(i=i):
                self.assertEqual(self.Settings.parse_args(argument_list[i].split()), expected_result_list[i])

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
                    args = self.Settings.parse_args(argument_list[i].split())
                self.assertEqual(SE.exception.code, 2)

if __name__ == "__main__":
    unittest.main()