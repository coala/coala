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

import os
import inspect
import pkgutil
import argparse
import shlex


class Settings:
    def __init__(self):

        # TODO get settings
        # 1. load conf
        # 2. override with args

        # getting cli Arguments
        arg_vars = parse_args()

    def getSetting(self, key):
        pass

def parse_args(custom_arg_list = None):
    """
    Parses command line arguments and configures help output.

    :returns: parsed arguments in dictionary structure
    """
    # argparser reads given arguments and presents help on wrong input
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)

    # -d sets parameter "TargetLocations" => List of files and/or directories to be checked
    argparser.add_argument('-d', nargs='+', metavar='DIR',
                           help="Directories or files to be checked")
    # -dd sets parameter "RecursiveTargetLocations" => List of Directories to be checked including sub-directories
    argparser.add_argument('-dd', nargs='+', metavar='DIR',
                           help="Directories to be checked including sub-directories")
    # -f sets parameter "Filters" => List of filters to be used
    argparser.add_argument('-f', nargs='+', metavar='FILTER',
                           help="Filters to be applied")
    # -ff sets parameter "FilterMatch" => List of Regular Expressions, matching Filters are used
    argparser.add_argument('-ff', nargs='+', metavar='REGEX',
                           help="regular expressions matching filters to apply")
    # -t sets parameter "CheckedFileTypes" => List of file types that will be checked
    argparser.add_argument('-t', nargs='+', metavar='FILETYPE',
                           help="filetypes to be checked")
    # -i sets parameter "IgnoredFileTypes" => List of file types that will be ignored
    argparser.add_argument('-i', nargs='+', metavar='FILETYPE',
                           help="filetypes to be ignored")
    # -c sets parameter "ConfigLocation" => Location of configuration file, defaults to "ccfile"
    argparser.add_argument('-c', nargs='?', metavar='FILE',
                           default="ccfile",
                           help="Configuration file")
    # -s sets parameter "SaveSettings" => Bool that defines whether or not to save changes to ccfile
    argparser.add_argument('-s', action='store_true', help="save settings to local ccfile")
    # -v sets parameter "Verbosity" => Bool that defines whether or not to give verbose output
    argparser.add_argument('-v', action='store_true', help="enable verbosity")

    # arg_vars stores parsed arguments in form of a dictionary.
    # it reads custom_arg_string instead of sys.args if custom_arg_string is given.
    if custom_arg_list:
        arg_vars = vars(argparser.parse_args(custom_arg_list))
    else:
        arg_vars = vars(argparser.parse_args())

    return arg_vars