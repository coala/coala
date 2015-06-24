import argparse

from coalib.misc.i18n import _
from coalib import version_str


default_arg_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=_("coala is a simple COde AnaLysis Application. Its goal is "
                  "to make static code analysis easy and convenient for all "
                  "languages."))

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
LOG_LEVEL_HELP = _("Enum('ERROR','WARNING','DEBUG') to set level of log "
                   "output")
default_arg_parser.add_argument('-L',
                                '--log-level',
                                nargs=1,
                                choices=['ERROR', 'WARNING', 'DEBUG'],
                                metavar='ENUM',
                                help=LOG_LEVEL_HELP)
CONFIG_HELP = _('Configuration file to be used, defaults to .coafile')
default_arg_parser.add_argument('-c',
                                '--config',
                                nargs=1,
                                metavar='FILE',
                                help=CONFIG_HELP)
SAVE_HELP = _('Filename of file to be saved to, if provided with no arguments,'
              ' settings will be stored back to the file given by -c')
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
APPLY_HELP = _("Enum('YES','NO','ASK') to set whether to apply changes")
default_arg_parser.add_argument('-a',
                                '--apply-changes',
                                nargs=1,
                                choices=['YES', 'NO', 'ASK'],
                                metavar='ENUM',
                                help=APPLY_HELP)
default_arg_parser.add_argument('-v',
                                '--version',
                                action='version',
                                version=version_str)
SHOW_BEARS_HELP = _("Display bears and its metadata with the sections that "
                    "they belong to")
default_arg_parser.add_argument('-B',
                                '--show-bears',
                                nargs='?',
                                const=True,
                                metavar='BOOL',
                                help=SHOW_BEARS_HELP)
