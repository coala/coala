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
import argparse
from coalib.misc.i18n import _

default_arg_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)

default_arg_parser.add_argument('-f', '--files', nargs='+', metavar='FILE', dest='allowed_files',
                                help=_('Files that should be checked'))
default_arg_parser.add_argument('-D', '--flat-dirs', nargs='+', metavar='DIR', dest='flat_directories',
                                help=_('Directories of files that should be checked, excluding sub directories'))
default_arg_parser.add_argument('-d', '--rec-dirs', nargs='+', metavar='DIR', dest='recursive_directories',
                                help=_('Directories of files that should be checked, including sub directories'))
default_arg_parser.add_argument('-t', '--allowed', nargs='+', metavar='TYPE', dest='allowed_file_types',
                                help=_('File types of files to be checked'))
default_arg_parser.add_argument('-F', '--forbidden', nargs='+', metavar='TYPE', dest='forbidden_file_types',
                                help=_('File types not to be checked'))
default_arg_parser.add_argument('-i', '--ignored-files', nargs='+', metavar='PATH', dest='ignored_files',
                                help=_('Files that should be ignored'))
default_arg_parser.add_argument('-p', '--ignored-dirs', nargs='+', metavar='PATH', dest='ignored_dirs',
                                help=_('Directories that should be ignored'))
default_arg_parser.add_argument('-B', '--bear-dirs', nargs='+', metavar='DIR', dest='bear-directories',
                                help=_('Directories to look in for bears'))
default_arg_parser.add_argument('-b', '--bears', nargs='+', metavar='NAME', dest='bears',
                                help=_('Names of bears to use'))
default_arg_parser.add_argument('-I', '--ignored_bears', nargs='+', metavar='REGEX', dest='ignored_bears',
                                help=_('Names of bears not to use'))
default_arg_parser.add_argument('-r', '--regex-bears', nargs='+', metavar='REGEX', dest='regex_bears',
                                help=_('Regular expressions matching bears to use'))
default_arg_parser.add_argument('-l', '--log', nargs=1, choices=['CONSOLE', 'TXT', 'HTML'], metavar='ENUM',
                                dest='log_type', help=_("Enum('CONSOLE','TXT','HTML') to determine type of logging"))
default_arg_parser.add_argument('-L', '--log_level', nargs=1, choices=['ERR', 'WARN', 'INFO', 'DEBUG'],
                                metavar='ENUM', dest='log_level',
                                help=_("Enum('ERR','WARN','INFO','DEBUG') to set level of log output"))
default_arg_parser.add_argument('-o', '--output', nargs=1, metavar='FILE', dest='output',
                                help=_('Location of lot output'))
default_arg_parser.add_argument('-c', '--config', nargs='+', metavar='FILE', dest='config',
                                help=_('Configuration file to be used'))
default_arg_parser.add_argument('-s', '--save', nargs='?', const=True, metavar='FILE', dest='save',
                                help=_('Filename of file to be saved to, defaults to config file'))
default_arg_parser.add_argument('-j', '--job-count', nargs=1, type=int, metavar='INT', dest='job_count',
                                help=_('Number of processes to be allowed to run at once'))
default_arg_parser.add_argument('-C', '--apply-changes', nargs=1, choices=['YES', 'NO', 'ASK'], metavar='ENUM',
                                dest='apply_changes', help=_("Enum('YES','NO','ASK') to set whether to apply changes"))
