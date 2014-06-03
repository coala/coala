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
        self.Settings = settings.Settings('-v DEBUG'.split())
        if os.path.isfile('first_file'):
            os.remove('first_file')
        if os.path.isfile('second_file'):
            os.remove('second_file')
        if os.path.isfile('sample_config'):
            os.remove('sample_config')

    def tearDown(self):
        #cleanup test_configuration_parsing
        if os.path.isfile('first_file'):
            os.remove('first_file')
        if os.path.isfile('second_file'):
            os.remove('second_file')
        if os.path.isfile('sample_config'):
            os.remove('sample_config')

    @unittest.skipIf(sys.version_info < (3, 4), "This test is not supported by python < 3.4")
    def test_accept_possible_cli_arguments(self):

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
         'ConfigFile':["/home/fabian/codec.conf"],
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
         'Save':[True],
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
         'Save':['Hallo'],
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
         'ConfigFile':['k'],
         'Save':[True],
         'JobCount':[5]}
        ]

        # the result should be equal to the expected result in any of these cases
        for i in range(len(argument_list)):
            with self.subTest(i=i):
                self.assertEqual(self.Settings.parse_args(argument_list[i].split()), expected_result_list[i])

    @unittest.skipIf(sys.version_info < (3, 4), "This test is not supported by python < 3.4")
    def test_reject_impossible_cli_arguments(self):

        argument_list = [
        "-d",
        "-l SOMETHING",
        "-l TXT HTML",
        "-c b a",
        "-v SOMETHING",
        "-j h",
        " ",
        "WEIRD",
        "-c"
        ]

        # A SystemExit with code 2 should be raised in any of these cases
        for i in range(len(argument_list)):
            with self.subTest(i=i):
                with self.assertRaises(SystemExit) as SE:
                    args = self.Settings.parse_args(argument_list[i].split())
                self.assertEqual(SE.exception.code, 2)

    def test_configuration_parsing(self):

        # set up config files
        first_file = """TaRgEtDiReCtOrIeS=first,second,third#comment
      FILTERS     =      moar whitespace        #     comment
save=/only/path/not/list
configfile=second_file
# this whole line is a comment...
unknown1=this stays
this is true = yup
thisisjustsomeshitwithoutmeaning
= now we have no key"""
        second_file = """configfile=first_file#no workerino
targetdirectories = this,will,not,stay
unknown2=all,of,these,will#this,not
int= 4"""
        with open('first_file','w') as f:
            f.write(first_file)
            f.close()
        with open('second_file','w') as f:
            f.write(second_file)
            f.close()

        # test read_conf():
        actual_result_dict = self.Settings.read_conf('first_file')

        expected_result_dict = {
                                "TargetDirectories":['first','second','third'],
                                "Filters":['moar whitespace'],
                                "Save":['/only/path/not/list'],
                                "ConfigFile":['second_file'],
                                "unknown1":['this stays'],
                                "this is true":[True],
                                "unknown2":['all','of','these','will'],
                                "int":[4]
                                }

        # now this is the interesting part
        self.assertEqual(actual_result_dict, expected_result_dict)

    def test_setting_class_creation(self):

        # write config
        with open('sample_config','w') as sample_config:
            config_string = """TargetDirectories = from conf, will be overwritten
IgnoredDirectories = from conf, will stay
newfiltersetting = from conf, will stay"""
            sample_config.write(config_string)
            sample_config.close()

        # create Settings
        new_settings = settings.Settings("-c sample_config -d fromcli -t fromcli".split())

        # get dict from Settings:
        new_settings_dict = {}
        for key, value in new_settings.items():
            new_settings_dict[key]=value

        # expected dict
        expected_dict ={'TargetDirectories': ['fromcli'],  # set by conf, overwritten by cli
                        'IgnoredDirectories': ['from conf','will stay'],
                        'FlatDirectories': None,  # default value
                        'TargetFileTypes': ['fromcli'],  # set by cli
                        'IgnoredFileTypes': ['.gitignore'],

                        'Filters': None,
                        'IgnoredFilters': None,
                        'RegexFilters': None,

                        'FileOkColor': ['bright red'],
                        'FileBadColor': ['bright green'],
                        'FilterColor': ['grey'],
                        'ErrorResultColor': ['red'],
                        'WarningResultColor': ['yellow'],
                        'InfoResultColor': ['normal'],
                        'DebugResultColor': ['cyan'],

                        'LogType': ['CONSOLE'],
                        'LogOutput': None,
                        'Verbosity': ['INFO'],

                        'ConfigFile':['sample_config'],
                        'Save': None,
                        'JobCount': None,

                        'newfiltersetting':['from conf','will stay']  # new value by conf
                        }

        # the fun part again.
        self.assertEqual(new_settings_dict, expected_dict)

    @unittest.skipIf(sys.version_info < (3, 3), "This test is not supported by python < 3.3")
    def test_saving_and_loading_of_configs(self):

        old_settings = settings.Settings("-s -c sample_config -d fromcli -t fromcli".split())
        new_settings = settings.Settings("-c sample_config".split())

        self.assertEqual(old_settings, new_settings)

        old_settings2 = settings.Settings("-s second_file -c sample_config -d fromcli -t fromcli".split())
        new_settings2 = settings.Settings("-c second_file".split())

        # eliminate wanted difference:
        self.assertEqual(new_settings2['ConfigFile'], ['second_file'])
        new_settings2['ConfigFile'] = ['sample_config']

        self.assertEqual(old_settings2, new_settings2)

if __name__ == "__main__":
    unittest.main()