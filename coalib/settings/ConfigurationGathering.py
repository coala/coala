import os
import re
import sys

from coalib.misc import Constants
from coalib.output.ConfWriter import ConfWriter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.parsing.CliParsing import parse_cli, check_conflicts
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.Section import Section
from coalib.settings.SectionFilling import fill_settings
from coalib.settings.Setting import Setting, path


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


def load_config_file(filename, log_printer, silent=False):
    """
    Loads sections from a config file. Prints an appropriate warning if
    it doesn't exist and returns a section dict containing an empty
    default section in that case.

    It assumes that the cli_sections are available.

    :param filename:    The file to load settings from.
    :param log_printer: The log printer to log the warning/error to (in case).
    :param silent:      Whether or not to warn the user/exit if the file
                        doesn't exist.
    :raises SystemExit: Exits when given filename is invalid and is not the
                        default coafile. Only raised when ``silent`` is
                        ``False``.
    """
    filename = os.path.abspath(filename)

    try:
        return ConfParser().parse(filename)
    except FileNotFoundError:
        if not silent:
            if os.path.basename(filename) == Constants.default_coafile:
                log_printer.warn("The default coafile " +
                                 repr(Constants.default_coafile) + " was not "
                                 "found. Ignoring it.")
            else:
                log_printer.err("The requested coafile " + repr(filename) +
                                " does not exist.")
                sys.exit(2)

        return {"default": Section("default")}


def save_sections(sections):
    """
    Saves the given sections if they are to be saved.

    :param sections: A section dict.
    """
    default_section = sections["default"]
    try:
        if bool(default_section.get("save", "false")):
            conf_writer = ConfWriter(
                str(default_section.get("config", Constants.default_coafile)))
        else:
            return
    except ValueError:
        conf_writer = ConfWriter(str(default_section.get("save", ".coafile")))

    conf_writer.write_sections(sections)
    conf_writer.close()


def warn_nonexistent_targets(targets, sections, log_printer):
    """
    Prints out a warning on the given log printer for all targets that are
    not existent within the given sections.

    :param targets:     The targets to check.
    :param sections:    The sections to search. (Dict.)
    :param log_printer: The log printer to warn to.
    """
    for target in targets:
        if target not in sections:
            log_printer.warn(
                "The requested section '{section}' is not existent. "
                "Thus it cannot be executed.".format(section=target))


def load_configuration(arg_list, log_printer):
    """
    Parses the CLI args and loads the config file accordingly, taking
    default_coafile and the users .coarc into account.

    :param arg_list:    The list of command line arguments.
    :param log_printer: The LogPrinter object for logging.
    :return:            A tuple holding (log_printer: LogPrinter, sections:
                        dict(str, Section), targets: list(str)). (Types
                        indicated after colon.)
    """
    cli_sections = parse_cli(arg_list=arg_list)
    check_conflicts(cli_sections)

    if (
            bool(cli_sections["default"].get("find_config", "False")) and
            str(cli_sections["default"].get("config")) == ""):
        cli_sections["default"].add_or_create_setting(
            Setting("config", re.escape(find_user_config(os.getcwd()))))

    targets = []
    # We don't want to store targets argument back to file, thus remove it
    for item in list(cli_sections["default"].contents.pop("targets", "")):
        targets.append(item.lower())

    if bool(cli_sections["default"].get("no_config", "False")):
        sections = cli_sections
    else:
        default_sections = load_config_file(Constants.system_coafile,
                                            log_printer)
        user_sections = load_config_file(
            Constants.user_coafile,
            log_printer,
            silent=True)

        default_config = str(
            default_sections["default"].get("config", ".coafile"))
        user_config = str(user_sections["default"].get(
            "config", default_config))
        config = os.path.abspath(
            str(cli_sections["default"].get("config", user_config)))

        try:
            save = bool(cli_sections["default"].get("save", "False"))
        except ValueError:
            # A file is deposited for the save parameter, means we want to save
            # but to a specific file.
            save = True

        coafile_sections = load_config_file(config, log_printer, silent=save)

        sections = merge_section_dicts(default_sections, user_sections)

        sections = merge_section_dicts(sections, coafile_sections)

        sections = merge_section_dicts(sections, cli_sections)

    for section in sections:
        if section != "default":
            sections[section].defaults = sections["default"]

    str_log_level = str(sections["default"].get("log_level", "")).upper()
    log_printer.log_level = LOG_LEVEL.str_dict.get(str_log_level,
                                                   LOG_LEVEL.INFO)

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
    home_dir = os.path.expanduser("~")

    while base_dir != old_dir and old_dir != home_dir and max_trials != 0:
        config_file = os.path.join(base_dir, ".coafile")
        if os.path.isfile(config_file):
            return config_file

        old_dir = base_dir
        base_dir = os.path.dirname(old_dir)
        max_trials = max_trials - 1

    return ""


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

    >>> section['files'].origin = os.path.abspath('/tmp/dir/')
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


def gather_configuration(acquire_settings,
                         log_printer,
                         autoapply=None,
                         arg_list=None):
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
    :param autoapply:        Set whether to autoapply patches. This is
                             overridable via any configuration file/CLI.
    :param arg_list:         CLI args to use
    :return:                 A tuple with the following contents:

                             -  A dictionary with the sections
                             -  Dictionary of list of local bears for each
                                section
                             -  Dictionary of list of global bears for each
                                section
                             -  The targets list
    """
    # Note: arg_list can also be []. Hence we cannot use
    # `arg_list = arg_list or default_list`
    arg_list = sys.argv[1:] if arg_list is None else arg_list
    sections, targets = load_configuration(arg_list, log_printer)
    local_bears, global_bears = fill_settings(sections,
                                              acquire_settings,
                                              log_printer)
    save_sections(sections)
    warn_nonexistent_targets(targets, sections, log_printer)

    if autoapply is not None:
        if not autoapply and 'autoapply' not in sections['default']:
            sections['default']['autoapply'] = "False"

    return (sections,
            local_bears,
            global_bears,
            targets)
