import argparse

from coalib.misc import Constants
from coalib.collecting.Collectors import get_all_bears_names


class CustomFormatter(argparse.RawDescriptionHelpFormatter):
    """
    A Custom Formatter that will keep the metavars in the usage but remove them
    in the more detailed arguments section.
    """

    def _format_action_invocation(self, action):
        if not action.option_strings:
            # For arguments that don't have options strings
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
    formatter_class = (CustomFormatter if formatter_class is None
                       else formatter_class)

    description = """
coala provides a common command-line interface for linting and fixing all your
code, regardless of the programming languages you use.

To find out what kind of analysis coala offers for the languages you use, visit
<https://github.com/coala/bear-docs/blob/master/README.rst#supported-languages>
or run:

    $ coala --show-bears --filter-by-language C Python

To perform code analysis, simply specify the analysis routines (bears) and the
files you want it to run on, for example:

    spaceBear::

            $ coala --bears SpaceConsistencyBear --files **.py

coala can also automatically fix your code:

    spacePatchBear::

            $ coala --bears SpaceConsistencyBear --files **.py --apply-patches

To run coala without user interaction, run the `coala --non-interactive`,
`coala --json` and `coala --format` commands.
"""

    arg_parser = argparse.ArgumentParser(
        formatter_class=formatter_class,
        prog='coala',
        description=description,
        # Use our own help so that we can put it in the group we want
        add_help=False)

    arg_parser.add_argument('TARGETS',
                            nargs='*',
                            help='sections to be executed exclusively')

    info_group = arg_parser.add_argument_group('Info')

    info_group.add_argument('-h',
                            '--help',
                            action='help',
                            help='show this help message and exit')

    info_group.add_argument('-v',
                            '--version',
                            action='version',
                            version=Constants.VERSION)

    mode_group = arg_parser.add_argument_group('Mode')

    mode_group.add_argument(
        '-C', '--non-interactive', const=True, action='store_const',
        help='run coala in non interactive mode')

    mode_group.add_argument(
        '--ci', action='store_const', dest='non_interactive', const=True,
        help='continuous integration run, alias for `--non-interactive`')

    mode_group.add_argument(
        '--json', const=True, action='store_const',
        help='mode in which coala will display output as json')

    mode_group.add_argument(
        '--format', const=True, nargs='?', metavar='STR',
        help='output results with a custom format string, e.g. '
             '"Message: {message}"; possible placeholders: '
             'id, origin, file, line, end_line, column, end_column, '
             'severity, severity_str, message')

    config_group = arg_parser.add_argument_group('Configuration')

    config_group.add_argument(
        '-c', '--config', nargs=1, metavar='FILE',
        help='configuration file to be used, defaults to {}'.format(
            Constants.default_coafile))

    config_group.add_argument(
        '-F', '--find-config', action='store_const', const=True,
        help='find {} in ancestors of the working directory'.format(
            Constants.default_coafile))

    config_group.add_argument(
        '-I', '--no-config', const=True, action='store_const',
        help='run without using any config file')

    config_group.add_argument(
        '-s', '--save', nargs='?', const=True, metavar='FILE',
        help='save used arguments to a config file to a {}, the given path, '
             'or at the value of -c'.format(Constants.default_coafile))

    config_group.add_argument(
        '--disable-caching', const=True, action='store_const',
        help='run on all files even if unchanged')
    config_group.add_argument(
        '--flush-cache', const=True, action='store_const',
        help='rebuild the file cache')

    inputs_group = arg_parser.add_argument_group('Inputs')

    inputs_group.add_argument(
        '-b', '--bears', nargs='+', metavar='NAME',
        help='names of bears to use').completer = (
            lambda *args, **kwargs: get_all_bears_names())  # pragma: no cover

    inputs_group.add_argument(
        '-f', '--files', nargs='+', metavar='FILE',
        help='files that should be checked')

    inputs_group.add_argument(
        '-i', '--ignore', nargs='+', metavar='FILE',
        help='files that should be ignored')

    inputs_group.add_argument(
        '--limit-files', nargs='+', metavar='FILE',
        help="filter the `--files` argument's matches further")

    inputs_group.add_argument(
        '-d', '--bear-dirs', nargs='+', metavar='DIR',
        help='additional directories which may contain bears')

    outputs_group = arg_parser.add_argument_group('Outputs')

    outputs_group.add_argument(
        '-V', '--verbose', action='store_const',
        dest='log_level', const='DEBUG',
        help='alias for `-L DEBUG`')

    outputs_group.add_argument(
        '-L', '--log-level', nargs=1,
        choices=['ERROR', 'INFO', 'WARNING', 'DEBUG'], metavar='ENUM',
        help='set log output level to ERROR/INFO/WARNING/DEBUG')

    outputs_group.add_argument(
        '-m', '--min-severity', nargs=1,
        choices=('INFO', 'NORMAL', 'MAJOR'), metavar='ENUM',
        help='set minimal result severity to INFO/NORMAL/MAJOR')

    outputs_group.add_argument(
        '-N', '--no-color', const=True, action='store_const',
        help='display output without coloring (excluding logs)')

    outputs_group.add_argument(
        '-B', '--show-bears', const=True, action='store_const',
        help='list all bears')

    outputs_group.add_argument(
        '-l', '--filter-by-language', nargs='+', metavar='LANG',
        help='filters `--show-bears` by the given languages')

    outputs_group.add_argument(
        '-p', '--show-capabilities', nargs='+', metavar='LANG',
        help='show what coala can fix and detect for the given languages')

    outputs_group.add_argument(
        '-D', '--show-description', const=True, action='store_const',
        help='show bear descriptions for `--show-bears`')

    outputs_group.add_argument(
        '--show-details', const=True, action='store_const',
        help='show bear details for `--show-bears`')

    outputs_group.add_argument(
        '-o', '--output', nargs=1, metavar='FILE',
        help='write JSON logs to the given file (must be called with --json)')

    outputs_group.add_argument(
        '-r', '--relpath', nargs='?', const=True,
        help='return relative paths for files (must be called with --json)')

    misc_group = arg_parser.add_argument_group('Miscellaneous')

    misc_group.add_argument(
        '-S', '--settings', nargs='+', metavar='SETTING',
        help='arbitrary settings in the form of section.key=value')

    misc_group.add_argument(
        '-a', '--apply-patches', action='store_const',
        dest='default_actions', const='*: ApplyPatchAction',
        help='apply all patches automatically if possible')

    misc_group.add_argument(
        '-j', '--jobs', type=int,
        help='number of jobs to use in parallel')

    misc_group.add_argument(
        '-n', '--no-orig', const=True, action='store_const',
        help="don't create .orig backup files before patching")

    try:  # pragma: no cover
        # Auto completion should be optional, because of somewhat complicated
        # setup.
        import argcomplete
        argcomplete.autocomplete(arg_parser)
    except ImportError:
        pass
    return arg_parser
