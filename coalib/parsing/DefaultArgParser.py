import argparse
import sys

from coalib.misc import Constants
from coalib.collecting.Collectors import get_all_bears_names

try:
    from argcomplete.completers import ChoicesCompleter
except ImportError:
    class ChoicesCompleter:

        def __init__(self, *args, **kwargs):
            pass


def default_arg_parser(formatter_class=None):
    """
    This function creates an ArgParser to parse command line arguments.

    :param formatter_class: Formatting the arg_parser output into a specific
                            form. For example: In the manpage format.
    """
    formatter_class = formatter_class or argparse.RawDescriptionHelpFormatter

    entry_point = sys.argv[0]
    for entry in ['coala-ci', 'coala-dbus', 'coala-format', 'coala-json',
                  'coala-delete-orig']:
        if entry_point.endswith(entry):
            parser_type = entry
            break
    else:
        parser_type = 'coala'

    arg_parser = argparse.ArgumentParser(
        formatter_class=formatter_class,
        prog="coala",
        description="coala is a simple COde AnaLysis Application. Its goal "
                    "is to make static code analysis easy and convenient "
                    "for all languages. coala uses bears, which are analysis "
                    "routines that can be combined arbitrarily.")

    arg_parser.add_argument('TARGETS',
                            nargs='*',
                            help="Sections to be executed exclusively.")
    arg_parser.add_argument('-c',
                            '--config',
                            nargs=1,
                            metavar='FILE',
                            help='Configuration file to be used, defaults to '
                                 + repr(Constants.default_coafile))
    FIND_CONFIG_HELP = ('Attempt to find config file by checking parent '
                        'directories of the current working directory. It is '
                        'assumed that the config file is named '
                        + repr(Constants.default_coafile) + '. This arg is '
                        'ignored if --config is also given')
    arg_parser.add_argument('-F',
                            '--find-config',
                            nargs='?',
                            const=True,
                            metavar='BOOL',
                            help=FIND_CONFIG_HELP)
    arg_parser.add_argument('-I',
                            '--no-config',
                            nargs='?',
                            const=True,
                            metavar='BOOL',
                            help="Run without using any config file")
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
    arg_parser.add_argument('--limit-files',
                            nargs='+',
                            metavar='FILE',
                            help='Files that will be analyzed will be '
                                 'restricted to those in the globs listed '
                                 'in this argument as well the files setting')
    arg_parser.add_argument('-b',
                            '--bears',
                            nargs='+',
                            metavar='NAME',
                            help='Names of bears to use').completer =\
        ChoicesCompleter(get_all_bears_names())
    BEAR_DIRS_HELP = 'Additional directories where bears may lie'
    arg_parser.add_argument('-d',
                            '--bear-dirs',
                            nargs='+',
                            metavar='DIR',
                            help=BEAR_DIRS_HELP)
    LOG_LEVEL_HELP = ("Enum('ERROR','INFO','WARNING','DEBUG') to set level of "
                      "log output")
    arg_parser.add_argument('-L',
                            '--log-level',
                            nargs=1,
                            choices=['ERROR', 'INFO', 'WARNING', 'DEBUG'],
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
    if parser_type == 'coala-json':
        arg_parser.add_argument('--text-logs',
                                nargs='?',
                                const=True,
                                metavar='BOOL',
                                help='Don\'t display logs as json, display '
                                     'them as we normally do in the console.')
        arg_parser.add_argument('-o',
                                '--output',
                                nargs='?',
                                const=True,
                                metavar='BOOL',
                                help='Write the logs as json to a file '
                                'where filename is specified as argument.')
    if parser_type == 'coala':
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
        arg_parser.add_argument('-l',
                                '--show-language-bears',
                                nargs='+',
                                metavar='LANG',
                                help="Display all bears for the given "
                                "languages.")
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

    arg_parser.add_argument('-n',
                            '--no-orig',
                            nargs='?',
                            const=True,
                            help="Deactivate creation of .orig files,"
                                 ".orig backup files before applying patches")
    arg_parser.add_argument('-r',
                            '--relpath',
                            nargs='?',
                            const=True,
                            help="return relative paths for files")

    try:  # pragma: no cover
        # Auto completion should be optional, because of somewhat complicated
        # setup.
        import argcomplete
        argcomplete.autocomplete(arg_parser)
    except ImportError:
        pass
    return arg_parser
