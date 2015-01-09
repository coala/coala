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

default_arg_parser.add_argument('-f', '--files', nargs='+', metavar='FILE', dest='files',
                                help=_('Files that should be checked'))
default_arg_parser.add_argument('-r', '--files-regex', nargs='+', metavar='FILE', dest='files_regex',
                                help=_('Regex for additional filenames (only the tail of the whole path)'))
default_arg_parser.add_argument('-d', '--flat-dirs', nargs='+', metavar='DIR', dest='flat_dirs',
                                help=_('Directories where files may lie that will be checked, '
                                       'excluding sub directories'))
default_arg_parser.add_argument('-D', '--rec-dirs', nargs='+', metavar='DIR', dest='rec_dirs',
                                help=_('Directories where files may lie that will be checked, '
                                       'including sub directories'))
default_arg_parser.add_argument('-i', '--ignored-dirs', nargs='+', metavar='PATH', dest='ignored_dirs',
                                help=_('Directories that should be ignored'))
default_arg_parser.add_argument('-F', '--flat-bear-dirs', nargs='+', metavar='DIR', dest='flat_bear_dirs',
                                help=_('Directories where bears may lie, excluding subdirectories'))
default_arg_parser.add_argument('-B', '--rec-bear-dirs', nargs='+', metavar='DIR', dest='rec_bear_dirs',
                                help=_('Directories where bears may lie, including subdirectories'))
default_arg_parser.add_argument('-I', '--ignored-bear-dirs', nargs='+', metavar='DIR', dest='ignored_bear_dirs',
                                help=_('Directories to ignore when searching for bears'))
default_arg_parser.add_argument('-b', '--bears', nargs='+', metavar='NAME', dest='bears',
                                help=_('Names of bears to use'))
default_arg_parser.add_argument('-R', '--bears-regex', nargs='+', metavar='REGEX', dest='bears_regex',
                                help=_('Regular expression for bears to use'))
default_arg_parser.add_argument('-l', '--log', nargs=1, metavar='ENUM', dest='log_type',
                                help=_("Type of logging (console or any filename)"))
default_arg_parser.add_argument('-L', '--log-level', nargs=1, choices=['ERR', 'WARN', 'DEBUG'],
                                metavar='ENUM', dest='log_level',
                                help=_("Enum('ERR','WARN','DEBUG') to set level of log output"))
default_arg_parser.add_argument('-o', '--output', nargs=1, metavar='FILE', dest='output',
                                help=_('Type of output (console or any filename)'))
default_arg_parser.add_argument('-c', '--config', nargs='+', metavar='FILE', dest='config',
                                help=_('Configuration file to be used'))
default_arg_parser.add_argument('-s', '--save', nargs='?', const=True, metavar='FILE', dest='save',
                                help=_('Filename of file to be saved to, defaults to config file'))
default_arg_parser.add_argument('-j', '--job-count', nargs=1, type=int, metavar='INT', dest='job_count',
                                help=_('Number of processes to be allowed to run at once'))
default_arg_parser.add_argument('-a', '--apply-changes', nargs=1, choices=['YES', 'NO', 'ASK'], metavar='ENUM',
                                dest='apply_changes', help=_("Enum('YES','NO','ASK') to set whether to apply changes"))
