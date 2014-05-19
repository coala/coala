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
        self.Settings = settings.Settings()

    @unittest.skipIf(sys.version_info < (3, 4), "This test is not supported by python < 3.4")
    def test_accept_possible_arguments(self):

        argument_list = [
        "-d Hallo",
        "-dHallo",
        "-d Hallo Welt",
        "-l TXT",
        "--log CONSOLE",
        "-l TXT --log CONSOLE",
        "--verbose WARN",
        "-c /home/fabian/codec.conf",
        "-s",
        "-s Hallo",
        "-j 4",
        "-d a b -id c -fd d -t .e -it .f -f g -if h -rf i -l TXT -o j -v ERR -c k -s -j 5"
        ]
        # i=0
        expected_result_list = [
        {'TargetDirectories':['Hallo'],
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':None,
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':None,
         'Save':None,
         'JobCount':None},
        # i=1
        {'TargetDirectories':['Hallo'],
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':None,
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':None,
         'Save':None,
         'JobCount':None},
        # i=2
        {'TargetDirectories':['Hallo','Welt'],
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':None,
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':None,
         'Save':None,
         'JobCount':None},
        # i=3
        {'TargetDirectories':None,
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':['TXT'],
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':None,
         'Save':None,
         'JobCount':None},
        # i=4
        {'TargetDirectories':None,
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':['CONSOLE'],
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':None,
         'Save':None,
         'JobCount':None},
        # i=5
        {'TargetDirectories':None,
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':['CONSOLE'],
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':None,
         'Save':None,
         'JobCount':None},
        # i=6
        {'TargetDirectories':None,
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':None,
         'LogOutput':None,
         'Verbosity':['WARN'],
         'ConfigFile':None,
         'Save':None,
         'JobCount':None},
        # i=7
        {'TargetDirectories':None,
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':None,
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':"/home/fabian/codec.conf",
         'Save':None,
         'JobCount':None},
        # i=8
        {'TargetDirectories':None,
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':None,
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':None,
         'Save':True,
         'JobCount':None},
        # i=9
        {'TargetDirectories':None,
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':None,
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':None,
         'Save':'Hallo',
         'JobCount':None},
        # i=10
        {'TargetDirectories':None,
         'IgnoredDirectories':None,
         'FlatDirectories':None,
         'TargetFileTypes':None,
         'IgnoredFileTypes':None,
         'Filters':None,
         'IgnoredFilters':None,
         'RegexFilters':None,
         'LogType':None,
         'LogOutput':None,
         'Verbosity':None,
         'ConfigFile':None,
         'Save':None,
         'JobCount':[4]},
        # i=11
        {'TargetDirectories':['a','b'],
         'IgnoredDirectories':['c'],
         'FlatDirectories':['d'],
         'TargetFileTypes':['.e'],
         'IgnoredFileTypes':['.f'],
         'Filters':['g'],
         'IgnoredFilters':['h'],
         'RegexFilters':['i'],
         'LogType':['TXT'],
         'LogOutput':['j'],
         'Verbosity':['ERR'],
         'ConfigFile':'k',
         'Save':True,
         'JobCount':[5]}
        ]

        # the result should be equal to the expected result in any of these cases
        for i in range(len(argument_list)):
            with self.subTest(i=i):
                self.assertEqual(self.Settings.parse_args(argument_list[i].split()), expected_result_list[i])

    @unittest.skipIf(sys.version_info < (3, 4), "This test is not supported by python < 3.4")
    def test_reject_impossible_arguments(self):

        argument_list = [
        "-d",
        "-l SOMETHING",
        "-l TXT HTML",
        "-c b a",
        "-v SOMETHING",
        "-j h",
        " ",
        "WEIRD"
        ]

        # A SystemExit with code 2 should be raised in any of these cases
        for i in range(len(argument_list)):
            with self.subTest(i=i):
                with self.assertRaises(SystemExit) as SE:
                    args = self.Settings.parse_args(argument_list[i].split())
                self.assertEqual(SE.exception.code, 2)

if __name__ == "__main__":
    unittest.main()