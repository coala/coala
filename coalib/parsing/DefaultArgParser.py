import argparse

from coalib.misc.i18n import _
from coalib.misc.Constants import Constants


def default_arg_parser(formatter_class=None):
    formatter_class = formatter_class or argparse.RawDescriptionHelpFormatter
    arg_parser = argparse.ArgumentParser(
        formatter_class=formatter_class,
        prog="coala",
        description=_("coala is a simple COde AnaLysis Application. Its goal "
                      "is to make static code analysis easy and convenient "
                      "for all languages."))

    arg_parser.add_argument('TARGETS',
                            nargs='*',
                            help=_("Sections to be executed exclusively."))
    CONFIG_HELP = _('Configuration file to be used, defaults to .coafile')
    arg_parser.add_argument('-c',
                            '--config',
                            nargs=1,
                            metavar='FILE',
                            help=CONFIG_HELP)
    FIND_CONFIG_HELP = _('Attempt to find config file by checking parent '
                         'directories of the current working directory. It is '
                         'assumed that the config file is named '
                         '`.coafile`. This arg is ignored if --config is also '
                         'given')
    arg_parser.add_argument('-F',
                            '--find-config',
                            nargs='?',
                            const=True,
                            metavar='BOOL',
                            help=FIND_CONFIG_HELP)
    arg_parser.add_argument('-f',
                            '--files',
                            nargs='+',
                            metavar='FILE',
                            help=_('Files that should be checked'))
    arg_parser.add_argument('-b',
                            '--bears',
                            nargs='+',
                            metavar='NAME',
                            help=_('Names of bears to use'))
    BEAR_DIRS_HELP = _('Additional directories where bears may lie')
    arg_parser.add_argument('-d',
                            '--bear-dirs',
                            nargs='+',
                            metavar='DIR',
                            help=BEAR_DIRS_HELP)
    LOG_LEVEL_HELP = _("Enum('ERROR','WARNING','DEBUG') to set level of log "
                       "output")
    arg_parser.add_argument('-L',
                            '--log-level',
                            nargs=1,
                            choices=['ERROR', 'WARNING', 'DEBUG'],
                            metavar='ENUM',
                            help=LOG_LEVEL_HELP)
    SETTINGS_HELP = _('Arbitrary settings in the form of section.key=value')
    arg_parser.add_argument('-S',
                            '--settings',
                            nargs='+',
                            metavar='SETTING',
                            help=SETTINGS_HELP)
    SHOW_BEARS_HELP = _("Display bears and its metadata with the sections "
                        "that they belong to")
    arg_parser.add_argument('-B',
                            '--show-bears',
                            nargs='?',
                            const=True,
                            metavar='BOOL',
                            help=SHOW_BEARS_HELP)
    SAVE_HELP = _('Filename of file to be saved to, if provided with no '
                  'arguments, settings will be stored back to the file given '
                  'by -c')
    arg_parser.add_argument('-s',
                            '--save',
                            nargs='?',
                            const=True,
                            metavar='FILE',
                            help=SAVE_HELP)

    arg_parser.add_argument('-v',
                            '--version',
                            action='version',
                            version=Constants.VERSION)
    return arg_parser
