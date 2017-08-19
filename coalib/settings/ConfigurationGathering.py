import os
import re
import sys
import logging

from coalib.collecting.Collectors import (
    collect_all_bears_from_sections, filter_section_bears_by_languages)
from coalib.bearlib.languages.Language import Language, UnknownLanguageError
from coalib.misc import Constants
from coalib.output.ConfWriter import ConfWriter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.parsing.CliParsing import parse_cli, check_conflicts
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.Section import Section, extract_aspects_from_section
from coalib.settings.SectionFilling import fill_settings
from coalib.settings.Setting import Setting, path
from string import Template

COAFILE_OUTPUT = Template('$type \'$file\' $found!\n'
                          'Here\'s what you can do:\n'
                          '* add `--save` to generate a config file with '
                          'your current options\n'
                          '* add `-I` to suppress any use of config files\n')


def aspectize_sections(sections):
    """
    Search for aspects related setting in a section, initialize it, and then
    embed the aspects information as AspectList object into the section itself.

    :param sections:  List of section that potentially contain aspects setting.
    :return:          The new sections.
    """
    for _, section in sections.items():
        if validate_aspect_config(section):
            section.aspects = extract_aspects_from_section(section)
        else:
            section.aspects = None
    return sections


def validate_aspect_config(section):
    """
    Validate if a section contain required setting to run in aspects mode.

    :param section: The section that potentially contain aspect
                    setting.
    :return:        The validity of section.
    """
    aspects = section.get('aspects')

    if not len(aspects):
        return False

    if not section.language:
        logging.warning('Setting `language` is not found in section `{}`. '
                        'Usage of aspect-based setting must include '
                        'language information.'.format(section.name))
        return False

    if len(section.get('bears')):
        logging.warning('`aspects` and `bears` setting is detected '
                        'in section `{}`. Aspect-based configuration will '
                        'takes priority and will overwrite any '
                        'explicitly listed bears.'.format(section.name))
    return True


def _set_section_language(sections):
    """
    Validate ``language`` setting and inject them to section if valid.

    :param sections: List of sections that potentially contain ``language``.
    """
    for section_name, section in sections.items():
        section_language = section.get('language')
        if not len(section_language):
            continue

        try:
            section.language = Language[section_language]
        except UnknownLanguageError as exc:
            logging.warning('Section `{}` contain invalid language setting: '
                            '{}'.format(section_name, exc))


def merge_section_dicts(lower, higher):
    """
    Merges the section dictionaries. The values of higher will take
    precedence over the ones of lower. Lower will hold the modified dict in
    the end.

    :param lower:  A section.
    :param higher: A section which values will take precedence over the ones
                   from the other.
    :return:       The merged dict.
    """
    for name in higher:
        if name in lower:
            lower[name].update(higher[name], ignore_defaults=True)
        else:
            # no deep copy needed
            lower[name] = higher[name]

    return lower


def load_config_file(filename, log_printer=None, silent=False):
    """
    Loads sections from a config file. Prints an appropriate warning if
    it doesn't exist and returns a section dict containing an empty
    default section in that case.

    It assumes that the cli_sections are available.

    :param filename:    The file to load settings from.
    :param log_printer: The log printer to log the warning/error to (in case).
    :param silent:      Whether or not to warn the user/exit if the file
                        doesn't exist.
    :raises SystemExit: Exits when the given filename is invalid and is not the
                        default coafile. Only raised when ``silent`` is
                        ``False``.
    """
    filename = os.path.abspath(filename)

    try:
        return ConfParser().parse(filename)
    except FileNotFoundError:
        if not silent:
            if os.path.basename(filename) == Constants.default_coafile:
                logging.warning(COAFILE_OUTPUT
                                .substitute(type='Default coafile',
                                            file=Constants.default_coafile,
                                            found='not found'))
            else:
                logging.error(COAFILE_OUTPUT
                              .substitute(type='Requested coafile',
                                          file=filename,
                                          found='does not exist'))
                sys.exit(2)

        return {'default': Section('default')}


def save_sections(sections):
    """
    Saves the given sections if they are to be saved.

    :param sections: A section dict.
    """
    default_section = sections['cli']
    try:
        if bool(default_section.get('save', 'false')):
            conf_writer = ConfWriter(
                str(default_section.get('config', Constants.default_coafile)))
        else:
            return
    except ValueError:
        conf_writer = ConfWriter(str(default_section.get('save', '.coafile')))

    conf_writer.write_sections(sections)
    conf_writer.close()


def warn_nonexistent_targets(targets, sections, log_printer=None):
    """
    Prints out a warning on the given log printer for all targets that are
    not existent within the given sections.

    :param targets:     The targets to check.
    :param sections:    The sections to search. (Dict.)
    :param log_printer: The log printer to warn to.
    """
    for target in targets:
        if target not in sections:
            logging.warning(
                "The requested section '{section}' is not existent. "
                'Thus it cannot be executed.'.format(section=target))

    # Can't be summarized as python will evaluate conditions lazily, those
    # functions have intended side effects though.
    files_config_absent = warn_config_absent(sections, 'files')
    bears_config_absent = warn_config_absent(sections, ['bears', 'aspects'])
    if files_config_absent or bears_config_absent:
        raise SystemExit(2)  # Invalid CLI options provided


def warn_config_absent(sections, argument, log_printer=None):
    """
    Checks if at least 1 of the given arguments is present somewhere in the
    sections and emits a warning that code analysis can not be run without it.

    :param sections:    A dictionary of sections.
    :param argument:    An argument OR a list of arguments that at least 1
                        should present.
    :param log_printer: A log printer to emit the warning to.
    :return:            Returns a boolean True if the given argument
                        is present in the sections, else returns False.
    """
    if isinstance(argument, str):
        argument = [argument]
    for section in sections.values():
        if any(arg in section for arg in argument):
            return False

    formatted_args = ' or '.join('`--{}`'.format(arg) for arg in argument)
    logging.warning('coala will not run any analysis. Did you forget '
                    'to give the {} argument?'.format(formatted_args))
    return True


def load_configuration(arg_list,
                       log_printer=None,
                       arg_parser=None,
                       args=None,
                       silent=False):
    """
    Parses the CLI args and loads the config file accordingly, taking
    default_coafile and the users .coarc into account.

    :param arg_list:    The list of CLI arguments.
    :param log_printer: The LogPrinter object for logging.
    :param arg_parser:  An ``argparse.ArgumentParser`` instance used for
                        parsing the CLI arguments.
    :param args:        Alternative pre-parsed CLI arguments.
    :param silent:      Whether or not to display warnings, ignored if ``save``
                        is enabled.
    :return:            A tuple holding (log_printer: LogPrinter, sections:
                        dict(str, Section), targets: list(str)). (Types
                        indicated after colon.)
    """
    cli_sections = parse_cli(arg_list=arg_list, arg_parser=arg_parser,
                             args=args)
    check_conflicts(cli_sections)

    if (
            bool(cli_sections['cli'].get('find_config', 'False')) and
            str(cli_sections['cli'].get('config')) == ''):
        cli_sections['cli'].add_or_create_setting(
            Setting('config', re.escape(find_user_config(os.getcwd()))))

    targets = []
    # We don't want to store targets argument back to file, thus remove it
    for item in list(cli_sections['cli'].contents.pop('targets', '')):
        targets.append(item.lower())

    if bool(cli_sections['cli'].get('no_config', 'False')):
        sections = cli_sections
    else:
        base_sections = load_config_file(Constants.system_coafile,
                                         silent=silent)
        user_sections = load_config_file(
            Constants.user_coafile, silent=True)

        default_config = str(base_sections['default'].get('config', '.coafile'))
        user_config = str(user_sections['default'].get(
            'config', default_config))
        config = os.path.abspath(
            str(cli_sections['cli'].get('config', user_config)))

        try:
            save = bool(cli_sections['cli'].get('save', 'False'))
        except ValueError:
            # A file is deposited for the save parameter, means we want to save
            # but to a specific file.
            save = True

        coafile_sections = load_config_file(config,
                                            silent=save or silent)

        sections = merge_section_dicts(base_sections, user_sections)

        sections = merge_section_dicts(sections, coafile_sections)

        if 'cli' in sections:
            logging.warning('\'cli\' is an internally reserved section name. '
                            'It may have been generated into your coafile '
                            'while running coala with `--save`. The settings '
                            'in that section will inherit implicitly to all '
                            'sections as defaults just like CLI args do. '
                            'Please change the name of that section in your '
                            'coafile to avoid any unexpected behavior.')

        sections = merge_section_dicts(sections, cli_sections)

    for name, section in list(sections.items()):
        section.set_default_section(sections)
        if name == 'default':
            if section.contents:
                logging.warning('Implicit \'Default\' section inheritance is '
                                'deprecated. It will be removed soon. To '
                                'silence this warning remove settings in the '
                                '\'Default\' section from your coafile. You '
                                'can use dots to specify inheritance: the '
                                'section \'all.python\' will inherit all '
                                'settings from \'all\'.')
                sections['default'].update(sections['cli'])
                sections['default'].name = 'cli'
                sections['cli'] = sections['default']
            del sections['default']

    str_log_level = str(sections['cli'].get('log_level', '')).upper()
    logging.getLogger().setLevel(LOG_LEVEL.str_dict.get(str_log_level,
                                                        LOG_LEVEL.INFO))

    return sections, targets


def find_user_config(file_path, max_trials=10):
    """
    Uses the filepath to find the most suitable user config file for the file
    by going down one directory at a time and finding config files there.

    :param file_path:  The path of the file whose user config needs to be found
    :param max_trials: The maximum number of directories to go down to.
    :return:           The config file's path, empty string if none was found
    """
    file_path = os.path.normpath(os.path.abspath(os.path.expanduser(
        file_path)))
    old_dir = None
    base_dir = (file_path if os.path.isdir(file_path)
                else os.path.dirname(file_path))
    home_dir = os.path.expanduser('~')

    while base_dir != old_dir and old_dir != home_dir and max_trials != 0:
        config_file = os.path.join(base_dir, '.coafile')
        if os.path.isfile(config_file):
            return config_file

        old_dir = base_dir
        base_dir = os.path.dirname(old_dir)
        max_trials = max_trials - 1

    return ''


def get_config_directory(section):
    """
    Retrieves the configuration directory for the given section.

    Given an empty section:

    >>> section = Section("name")

    The configuration directory is not defined and will therefore fallback to
    the current directory:

    >>> get_config_directory(section) == os.path.abspath(".")
    True

    If the ``files`` setting is given with an originating coafile, the directory
    of the coafile will be assumed the configuration directory:

    >>> section.append(Setting("files", "**", origin="/tmp/.coafile"))
    >>> get_config_directory(section) == os.path.abspath('/tmp/')
    True

    However if its origin is already a directory this will be preserved:

    >>> files = section['files']
    >>> files.origin = os.path.abspath('/tmp/dir/')
    >>> section.append(files)
    >>> os.makedirs(section['files'].origin, exist_ok=True)
    >>> get_config_directory(section) == section['files'].origin
    True

    The user can manually set a project directory with the ``project_dir``
    setting:

    >>> section.append(Setting('project_dir', os.path.abspath('/tmp'), '/'))
    >>> get_config_directory(section) == os.path.abspath('/tmp')
    True

    If no section is given, the current directory is returned:

    >>> get_config_directory(None) == os.path.abspath(".")
    True

    To summarize, the config directory will be chosen by the following
    priorities if possible in that order:

    - the ``project_dir`` setting
    - the origin of the ``files`` setting, if it's a directory
    - the directory of the origin of the ``files`` setting
    - the current directory

    :param section: The section to inspect.
    :return: The directory where the project is lying.
    """
    if section is None:
        return os.getcwd()

    if 'project_dir' in section:
        return path(section.get('project_dir'))

    config = os.path.abspath(section.get('files', '').origin)
    return config if os.path.isdir(config) else os.path.dirname(config)


def get_all_bears(log_printer=None,
                  arg_parser=None,
                  silent=True,
                  bear_globs=('**',)):
    """
    :param log_printer: The log_printer to handle logging.
    :param arg_parser:  An ``ArgParser`` object.
    :param silent:      Whether or not to display warnings.
    :param bear_globs:  List of glob patterns.
    :return:            Tuple containing dictionaries of local bears
                        and global bears.
    """
    sections, _ = load_configuration(arg_list=None,
                                     arg_parser=arg_parser,
                                     silent=silent)
    local_bears, global_bears = collect_all_bears_from_sections(
        sections, bear_globs=bear_globs)
    return local_bears, global_bears


def get_filtered_bears(languages,
                       log_printer=None,
                       arg_parser=None,
                       silent=True):
    """
    :param languages:   List of languages.
    :param log_printer: The log_printer to handle logging.
    :param arg_parser:  An ``ArgParser`` object.
    :param silent:      Whether or not to display warnings.
    :return:            Tuple containing dictionaries of local bears
                        and global bears.
    """
    local_bears, global_bears = get_all_bears(arg_parser=arg_parser,
                                              silent=silent)
    if languages:
        local_bears = filter_section_bears_by_languages(
            local_bears, languages)
        global_bears = filter_section_bears_by_languages(
            global_bears, languages)
    return local_bears, global_bears


def gather_configuration(acquire_settings,
                         log_printer=None,
                         arg_list=None,
                         arg_parser=None,
                         args=None):
    """
    Loads all configuration files, retrieves bears and all needed
    settings, saves back if needed and warns about non-existent targets.

    This function:

    -  Reads and merges all settings in sections from

       -  Default config
       -  User config
       -  Configuration file
       -  CLI

    -  Collects all the bears
    -  Fills up all needed settings
    -  Writes back the new sections to the configuration file if needed
    -  Gives all information back to caller

    :param acquire_settings: The method to use for requesting settings. It will
                             get a parameter which is a dictionary with the
                             settings name as key and a list containing a
                             description in [0] and the names of the bears
                             who need this setting in all following indexes.
    :param log_printer:      The log printer to use for logging. The log level
                             will be adjusted to the one given by the section.
    :param arg_list:         CLI args to use
    :param arg_parser:       Instance of ArgParser that is used to parse
                             none-setting arguments.
    :param args:             Alternative pre-parsed CLI arguments.
    :return:                 A tuple with the following contents:

                             -  A dictionary with the sections
                             -  Dictionary of list of local bears for each
                                section
                             -  Dictionary of list of global bears for each
                                section
                             -  The targets list
    """
    if args is None:
        # Note: arg_list can also be []. Hence we cannot use
        # `arg_list = arg_list or default_list`
        arg_list = sys.argv[1:] if arg_list is None else arg_list
    sections, targets = load_configuration(arg_list, arg_parser=arg_parser,
                                           args=args)
    _set_section_language(sections)
    aspectize_sections(sections)
    local_bears, global_bears = fill_settings(sections,
                                              acquire_settings)
    save_sections(sections)
    warn_nonexistent_targets(targets, sections)

    return (sections,
            local_bears,
            global_bears,
            targets)
