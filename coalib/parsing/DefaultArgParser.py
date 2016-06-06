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


class CustomFormatter(argparse.RawDescriptionHelpFormatter):
    """
    A Custom Formatter that will keep the metavars in the usage but remove them
    in the more detailed arguments section.
    """

    def _format_action_invocation(self, action):
        if not action.option_strings:
            # For arguemnts that don't have options strings
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            # Option string arguments (like "-f, --files")
            parts = action.option_strings
            return ', '.join(parts)


def default_arg_parser(formatter_class=None):
    """
    This function creates an ArgParser to parse command line arguments.

    :param formatter_class: Formatting the arg_parser output into a specific
                            form. For example: In the manpage format.
    """
    formatter_class = formatter_class or CustomFormatter

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
                    "routines that can be combined arbitrarily.",
        # Use our own help so that we can put it in the group we want
        add_help=False)

    arg_parser.add_argument('TARGETS',
                            nargs='*',
                            help="Sections to be executed exclusively.")

    info_group = arg_parser.add_argument_group('Info')

    info_group.add_argument('-h',
                            '--help',
                            action='help',
                            help='show this help message and exit')

    info_group.add_argument('-v',
                            '--version',
                            action='version',
                            version=Constants.VERSION)

    config_group = arg_parser.add_argument_group('Configuration')

    CONFIG_HELP = ('Configuration file to be used, defaults to '
                   + repr(Constants.default_coafile))
    config_group.add_argument('-c',
                              '--config',
                              nargs=1,
                              metavar='FILE',
                              help=CONFIG_HELP)

    FIND_CONFIG_HELP = ('Attempt to find config file by checking parent '
                        'directories of the current working directory. It is '
                        'assumed that the config file is named '
                        + repr(Constants.default_coafile) + '. This arg is '
                        'ignored if --config is also given')
    config_group.add_argument('-F',
                              '--find-config',
                              action='store_const',
                              const=True,
                              help=FIND_CONFIG_HELP)

    config_group.add_argument('-I',
                              '--no-config',
                              const=True,
                              action='store_const',
                              help="Run without using any config file")

    SAVE_HELP = ('Save the used arguments to a config file at the given path, '
                 "or at the value of -c, which is '.coafile' by default.")
    config_group.add_argument('-s',
                              '--save',
                              nargs='?',
                              const=True,
                              metavar='FILE',
                              help=SAVE_HELP)

    inputs_group = arg_parser.add_argument_group('Inputs')

    inputs_group.add_argument('-b',
                              '--bears',
                              nargs='+',
                              metavar='NAME',
                              help='Names of bears to use').completer =\
        ChoicesCompleter(get_all_bears_names())

    inputs_group.add_argument('-f',
                              '--files',
                              nargs='+',
                              metavar='FILE',
                              help='Files that should be checked')

    inputs_group.add_argument('-i',
                              '--ignore',
                              nargs='+',
                              metavar='FILE',
                              help='Files that should be ignored')

    LIMIT_FILES_HELP = ('Files that will be analyzed will be restricted to '
                        'those in the globs listed in this argument as well '
                        'the files setting')
    inputs_group.add_argument('--limit-files',
                              nargs='+',
                              metavar='FILE',
                              help=LIMIT_FILES_HELP)

    BEAR_DIRS_HELP = 'Additional directories where bears may lie'
    inputs_group.add_argument('-d',
                              '--bear-dirs',
                              nargs='+',
                              metavar='DIR',
                              help=BEAR_DIRS_HELP)

    outputs_group = arg_parser.add_argument_group('Outputs')

    outputs_group.add_argument('-V',
                               '--verbose',
                               action='store_const',
                               dest='log_level',
                               const='DEBUG',
                               help="Alias for `-L DEBUG`.")
    LOG_LEVEL_HELP = ("Enum('ERROR','INFO','WARNING','DEBUG') to set level of "
                      "log output")
    outputs_group.add_argument('-L',
                               '--log-level',
                               nargs=1,
                               choices=['ERROR', 'INFO', 'WARNING', 'DEBUG'],
                               metavar='ENUM',
                               help=LOG_LEVEL_HELP)

    MIN_SEVERITY_HELP = ("Enum('INFO', 'NORMAL', 'MAJOR') to set the minimal "
                         "result severity.")
    outputs_group.add_argument('-m',
                               '--min-severity',
                               nargs=1,
                               choices=('INFO', 'NORMAL', 'MAJOR'),
                               metavar='ENUM',
                               help=MIN_SEVERITY_HELP)

    # The following are "coala" specific arguments
    if parser_type == 'coala':
        SHOW_BEARS_HELP = ("Display bears and its metadata with the sections "
                           "that they belong to")
        outputs_group.add_argument('-B',
                                   '--show-bears',
                                   const=True,
                                   action='store_const',
                                   help=SHOW_BEARS_HELP)

        outputs_group.add_argument('-A',
                                   '--show-all-bears',
                                   const=True,
                                   action='store_const',
                                   help="Display all bears.")

        SHOW_LANGUAGE_BEARS = ("Display all bears for the given languages.")
        outputs_group.add_argument('-l',
                                   '--show-language-bears',
                                   nargs='+',
                                   metavar='LANG',
                                   help=SHOW_LANGUAGE_BEARS)

    # The following are "coala-json" specific arguments
    if parser_type == 'coala-json':
        TEXT_LOGS_HELP = ("Don't display logs as json, display them as we "
                          "normally do in the console.")
        outputs_group.add_argument('--text-logs',
                                   nargs='?',
                                   const=True,
                                   metavar='BOOL',
                                   help=TEXT_LOGS_HELP)

        OUTPUT_HELP = ('Write the logs as json to a file where filename is '
                       'specified as argument.')
        outputs_group.add_argument('-o',
                                   '--output',
                                   nargs=1,
                                   metavar='FILE',
                                   help=OUTPUT_HELP)

        outputs_group.add_argument('-r',
                                   '--relpath',
                                   nargs='?',
                                   const=True,
                                   help="Return relative paths for files")

    misc_group = arg_parser.add_argument_group('Miscellaneous')

    SETTINGS_HELP = 'Arbitrary settings in the form of section.key=value'
    misc_group.add_argument('-S',
                            '--settings',
                            nargs='+',
                            metavar='SETTING',
                            help=SETTINGS_HELP)

    misc_group.add_argument('-a',
                            '--apply-patches',
                            action='store_const',
                            dest='default_actions',
                            const='*: ApplyPatchAction',
                            help='Applies all patches automatically if '
                                 'possible.')

    misc_group.add_argument("-j",
                            "--jobs",
                            type=int,
                            help="Number of jobs to use in parallel.")

    NO_ORIG_HELP = ('Deactivate creation of .orig files and .orig backup '
                    'files before applying patches')
    misc_group.add_argument('-n',
                            '--no-orig',
                            const=True,
                            action='store_const',
                            help=NO_ORIG_HELP)

    deprecated_group = arg_parser.add_argument_group('Deprecated')

    TAG_HELP = ('Tag results with a specific name. You can access the results '
                'later with that tag.')
    deprecated_group.add_argument('-t',
                                  '--tag',
                                  nargs='?',
                                  const=True,
                                  metavar='STRING',
                                  help=TAG_HELP)

    DELETE_TAG_HELP = 'Delete pre-tagged results with tag name.'
    deprecated_group.add_argument('-g',
                                  '--dtag',
                                  nargs='?',
                                  const=True,
                                  metavar='STRING',
                                  help=DELETE_TAG_HELP)

    try:  # pragma: no cover
        # Auto completion should be optional, because of somewhat complicated
        # setup.
        import argcomplete
        argcomplete.autocomplete(arg_parser)
    except ImportError:
        pass
    return arg_parser
