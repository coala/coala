import argparse

from coalib.misc.i18n import _


default_arg_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)

default_arg_parser.add_argument('-f', '--files', nargs='+', metavar='FILE',
                                dest='files',
                                help=_('Files that should be checked'))
default_arg_parser.add_argument('-d', '--bear-dirs', nargs='+', metavar='DIR',
                                dest='bear_dirs',
                                help=_('Directories where bears may lie'))
default_arg_parser.add_argument('-b', '--bears', nargs='+', metavar='NAME',
                                dest='bears',
                                help=_('Names of bears to use'))
default_arg_parser.add_argument('-l', '--log', nargs=1, metavar='ENUM',
                                dest='log_type',
                                help=_("Type of logging "
                                       "(console or any filename)"))
default_arg_parser.add_argument('-L', '--log-level', nargs=1,
                                choices=['ERR', 'WARN', 'DEBUG'],
                                metavar='ENUM', dest='log_level',
                                help=_("Enum('ERR','WARN','DEBUG') "
                                       "to set level of log output"))
default_arg_parser.add_argument('-o', '--output', nargs=1, metavar='FILE',
                                dest='output',
                                help=_('Type of output '
                                       '(console or any filename)'))
default_arg_parser.add_argument('-c', '--config', nargs='+', metavar='FILE',
                                dest='config',
                                help=_('Configuration file to be used'))
default_arg_parser.add_argument('-s', '--save', nargs='?', const=True,
                                metavar='FILE', dest='save',
                                help=_('Filename of file to be saved to, '
                                       'defaults to config file'))
default_arg_parser.add_argument('-S', '--settings', nargs='+',
                                metavar='SETTING', dest='settings',
                                help=_('Arbitrary settings '
                                       'in the form of section.key=value'))
default_arg_parser.add_argument('-j', '--job-count', nargs=1, type=int,
                                metavar='INT', dest='job_count',
                                help=_('Number of processes to be allowed to '
                                       'run at once'))
default_arg_parser.add_argument('-a', '--apply-changes', nargs=1,
                                choices=['YES', 'NO', 'ASK'], metavar='ENUM',
                                dest='apply_changes',
                                help=_("Enum('YES','NO','ASK') "
                                       "to set whether to apply changes"))
