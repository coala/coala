import argparse

from coalib.misc.i18n import _


default_arg_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__
)

default_arg_parser.add_argument('TARGETS',
                                nargs='*',
                                help=_("Sections to be executed exclusively."))
default_arg_parser.add_argument('-f',
                                '--files',
                                nargs='+',
                                metavar='FILE',
                                help=_('Files that should be checked'))
default_arg_parser.add_argument('-b',
                                '--bears',
                                nargs='+',
                                metavar='NAME',
                                help=_('Names of bears to use'))
BEAR_DIRS_HELP = _('Additional directories where bears may lie')
default_arg_parser.add_argument('-d',
                                '--bear-dirs',
                                nargs='+',
                                metavar='DIR',
                                help=BEAR_DIRS_HELP)
LOG_TYPE_HELP = _("Type of logging (console or any filename)")
default_arg_parser.add_argument('-l',
                                '--log-type',
                                nargs=1,
                                metavar='ENUM',
                                help=LOG_TYPE_HELP)
LOG_LEVEL_HELP = _("Enum('ERR','WARN','DEBUG') to set level of log output")
default_arg_parser.add_argument('-L',
                                '--log-level',
                                nargs=1,
                                choices=['ERR', 'WARN', 'DEBUG'],
                                metavar='ENUM',
                                help=LOG_LEVEL_HELP)
OUTPUT_HELP = _('Type of output (console or any filename)')
default_arg_parser.add_argument('-o',
                                '--output',
                                nargs=1,
                                metavar='FILE',
                                help=OUTPUT_HELP)
CONFIG_HELP = _('Configuration file to be used, defaults to .coafile')
default_arg_parser.add_argument('-c',
                                '--config',
                                nargs=1,
                                metavar='FILE',
                                help=CONFIG_HELP)
SAVE_HELP = _('Filename of file to be saved to, if provided with no '
              'arguments, settings will be stored back to the config file')
default_arg_parser.add_argument('-s',
                                '--save',
                                nargs='?',
                                const=True,
                                metavar='FILE',
                                help=SAVE_HELP)
SETTINGS_HELP = _('Arbitrary settings in the form of section.key=value')
default_arg_parser.add_argument('-S',
                                '--settings',
                                nargs='+',
                                metavar='SETTING',
                                help=SETTINGS_HELP)
JOB_COUNT_HELP = _('Number of processes to be allowed to run at once')
default_arg_parser.add_argument('-j',
                                '--job-count',
                                nargs=1,
                                type=int,
                                metavar='INT',
                                help=JOB_COUNT_HELP)
APPLY_HELP = _("Enum('YES','NO','ASK') to set whether to apply changes")
default_arg_parser.add_argument('-a',
                                '--apply-changes',
                                nargs=1,
                                choices=['YES', 'NO', 'ASK'],
                                metavar='ENUM',
                                help=APPLY_HELP)
