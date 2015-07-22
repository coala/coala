import os
import sys

from coalib.settings.Setting import Setting
from coalib.misc.Constants import Constants
from coalib.misc.i18n import _
from coalib.output.ConfWriter import ConfWriter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.parsing.CliParsing import parse_cli
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.Section import Section
from coalib.settings.SectionFilling import fill_settings


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
    :param log_printer: The log printer to log the warning to (in case).
    :param silent:      Whether or not to warn the user if the file doesn't
                        exist.
    """
    filename = os.path.abspath(filename)

    try:
        return ConfParser().parse(filename)
    except ConfParser.FileNotFoundError:
        if not silent:
            log_printer.warn(
                _("The requested coafile '{filename}' does not exist.")
                .format(filename=filename))

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
                str(default_section.get("config", ".coafile")))
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
                _("The requested section '{section}' is not existent. "
                  "Thus it cannot be executed.").format(section=target))


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

    if (
            bool(cli_sections["default"].get("find_config", "False")) and
            str(cli_sections["default"].get("config")) == ""):
        cli_sections["default"].add_or_create_setting(
            Setting("config", find_user_config(os.getcwd())))

    targets = []
    # We don't want to store targets argument back to file, thus remove it
    for item in list(cli_sections["default"].contents.pop("targets", "")):
        targets.append(item.lower())

    default_sections = load_config_file(Constants.system_coafile,
                                        log_printer)

    user_sections = load_config_file(
        Constants.user_coafile,
        log_printer,
        silent=True)

    default_config = str(default_sections["default"].get("config", ".coafile"))
    user_config = str(user_sections["default"].get("config", default_config))
    config = os.path.abspath(
        str(cli_sections["default"].get("config", user_config)))

    try:
        save = bool(cli_sections["default"].get("save", "False"))
    except ValueError:
        # A file is deposited for the save parameter, means we want to save but
        # to a specific file.
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
                                                   LOG_LEVEL.WARNING)

    return sections, targets


def find_user_config(file_path, max_trials=10):
    """
    Uses the filepath to find the most suitable user config file for the file
    by going down one directory at a time and finding config files there.

    :param file_path:  The path of the file whose user config needs to be found
    :param max_trials: The maximum number of directories to go down to.
    :return:           The config file's path
    """
    file_path = os.path.normpath(os.path.abspath(os.path.expanduser(file_path)))
    old_dir = None
    base_dir = os.path.dirname(file_path)
    home_dir = os.path.expanduser("~")

    while base_dir != old_dir and old_dir != home_dir and max_trials != 0:
        config_file = os.path.join(base_dir, ".coafile")
        if os.path.isfile(config_file):
            return config_file

        old_dir = base_dir
        base_dir = os.path.dirname(old_dir)
        max_trials = max_trials - 1

    return ""


def gather_configuration(acquire_settings, log_printer, arg_list=sys.argv[1:]):
    """
    Loads all configuration files, retrieves bears and all needed
    settings, saves back if needed and warns about non-existent targets.

    This function:
    - Reads and merges all settings in sections from
        - Default config
        - User config
        - Configuration file
        - CLI
    - Collects all the bears
    - Fills up all needed settings
    - Writes back the new sections to the configuration file if needed
    - Gives all information back to caller

    :param acquire_settings: The method to use for requesting settings. It will
                             get a parameter which is a dictionary with the
                             settings name as key and a list containing a
                             description in [0] and the names of the bears
                             who need this setting in all following indexes.
    :param log_printer:      The log printer to use for logging. The log level
                             will be adjusted to the one given by the section.
    :param arg_list:         CLI args to use
    :return:                 A tuple with the following contents:
                              * A dictionary with the sections
                              * Dictionary of list of local bears for each
                                section
                              * Dictionary of list of global bears for each
                                section
                              * The targets list
    """
    sections, targets = load_configuration(arg_list, log_printer)
    local_bears, global_bears = fill_settings(sections,
                                              acquire_settings,
                                              log_printer)
    save_sections(sections)
    warn_nonexistent_targets(targets, sections, log_printer)

    return (sections,
            local_bears,
            global_bears,
            targets)
