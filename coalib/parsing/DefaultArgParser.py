import argparse

from coalib.misc.Constants import Constants


def default_arg_parser(formatter_class=None):
    formatter_class = formatter_class or argparse.RawDescriptionHelpFormatter
    arg_parser = argparse.ArgumentParser(
        formatter_class=formatter_class,
        prog="coala",
        description="coala is a simple COde AnaLysis Application. Its goal "
                    "is to make static code analysis easy and convenient "
                    "for all languages.")

    arg_parser.add_argument('TARGETS',
                            nargs='*',
                            help="Sections to be executed exclusively.")
    arg_parser.add_argument('-c',
                            '--config',
                            nargs=1,
                            metavar='FILE',
                            help='Configuration file to be used, defaults to '
                                 '.coafile')
    FIND_CONFIG_HELP = ('Attempt to find config file by checking parent '
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
                            help='Files that should be checked')
    arg_parser.add_argument('-i',
                            '--ignore',
                            nargs='+',
                            metavar='FILE',
                            help='Files that should be ignored')
    arg_parser.add_argument('-b',
                            '--bears',
                            nargs='+',
                            metavar='NAME',
                            help='Names of bears to use')
    BEAR_DIRS_HELP = 'Additional directories where bears may lie'
    arg_parser.add_argument('-d',
                            '--bear-dirs',
                            nargs='+',
                            metavar='DIR',
                            help=BEAR_DIRS_HELP)
    LOG_LEVEL_HELP = ("Enum('ERROR','WARNING','DEBUG') to set level of log "
                      "output")
    arg_parser.add_argument('-L',
                            '--log-level',
                            nargs=1,
                            choices=['ERROR', 'WARNING', 'DEBUG'],
                            metavar='ENUM',
                            help=LOG_LEVEL_HELP)
    MIN_SEVERITY_HELP = ("Enum('INFO', 'NORMAL', 'MAJOR') to set the minimal "
                         "result severity.")
    arg_parser.add_argument('-m',
                            '--min-severity',
                            nargs=1,
                            choices=('INFO', 'NORMAL', 'MAJOR'),
                            metavar='ENUM',
                            help=MIN_SEVERITY_HELP)
    SETTINGS_HELP = 'Arbitrary settings in the form of section.key=value'
    arg_parser.add_argument('-S',
                            '--settings',
                            nargs='+',
                            metavar='SETTING',
                            help=SETTINGS_HELP)
    SHOW_BEARS_HELP = ("Display bears and its metadata with the sections "
                       "that they belong to")
    arg_parser.add_argument('-B',
                            '--show-bears',
                            nargs='?',
                            const=True,
                            metavar='BOOL',
                            help=SHOW_BEARS_HELP)
    arg_parser.add_argument('-A',
                            '--show-all-bears',
                            nargs='?',
                            const=True,
                            metavar='BOOL',
                            help="Display all bears.")
    SAVE_HELP = ('Filename of file to be saved to, if provided with no '
                 'arguments, settings will be stored back to the file given '
                 'by -c')
    arg_parser.add_argument('-s',
                            '--save',
                            nargs='?',
                            const=True,
                            metavar='FILE',
                            help=SAVE_HELP)
    TAG_HELP = ('Tag results with a specific name. You can access the results'
                ' later with that tag.')
    arg_parser.add_argument('-t',
                            '--tag',
                            nargs='?',
                            const=True,
                            metavar='STRING',
                            help=TAG_HELP)

    DELETE_TAG_HELP = 'Delete pre-tagged results with tag name.'
    arg_parser.add_argument('-g',
                            '--dtag',
                            nargs='?',
                            const=True,
                            metavar='STRING',
                            help=DELETE_TAG_HELP)

    arg_parser.add_argument("-j",
                            "--jobs",
                            type=int,
                            help="Number of jobs to use in parallel.")

    arg_parser.add_argument('-v',
                            '--version',
                            action='version',
                            version=Constants.VERSION)
    return arg_parser
