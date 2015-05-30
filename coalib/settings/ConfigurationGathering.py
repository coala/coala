import os
import sys

from coalib.misc.StringConstants import StringConstants
from coalib.misc.i18n import _
from coalib.output.ConfWriter import ConfWriter
from coalib.output.NullInteractor import NullInteractor
from coalib.output.ClosableObject import close_objects
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.output.printers.FilePrinter import FilePrinter
from coalib.output.printers.NullPrinter import NullPrinter
from coalib.output.ConsoleInteractor import ConsoleInteractor
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
                _("The requested coafile '{filename}' does not exist. "
                  "Thus it will not be used.").format(filename=filename))

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


def retrieve_logging_objects(section):
    """
    Creates an appropriate log printer and interactor according to the
    settings.

    :param section: The section to get the logging objects for.
    :return:        A tuple holding (interactor, log_printer).
    """
    log_type = str(section.get("log_type", "console")).lower()
    output_type = str(section.get("output", "console")).lower()
    str_log_level = str(section.get("log_level", "")).upper()
    log_level = LOG_LEVEL.str_dict.get(str_log_level, LOG_LEVEL.WARNING)

    if log_type == "console":
        log_printer = ConsolePrinter(log_level=log_level)
    else:
        try:
            # ConsolePrinter is the only printer which may not throw an
            # exception (if we have no bugs though) so well fallback to him
            # if some other printer fails
            if log_type == "none":
                log_printer = NullPrinter()
            else:
                log_printer = FilePrinter(filename=log_type,
                                          log_level=log_level)
        except:
            log_printer = ConsolePrinter(log_level=log_level)
            log_printer.log(
                LOG_LEVEL.WARNING,
                _("Failed to instantiate the logging method '{}'. Falling "
                  "back to console output.").format(log_type))

    if output_type == "none":
        interactor = NullInteractor(log_printer=log_printer)
    else:
        interactor = ConsoleInteractor.from_section(
            section,
            log_printer=log_printer)

    return interactor, log_printer


def load_configuration(arg_list):
    """
    Parses the CLI args and loads the config file accordingly, taking
    default_coafile and the users .coarc into account.

    :param arg_list: The list of command line arguments.
    :return:         A tuple holding (interactor: Interactor, log_printer:
                     LogPrinter, sections: dict(str, Section),
                     targets: list(str)). (Types indicated after colon.)
    """
    cli_sections = parse_cli(arg_list=arg_list)
    interactor, log_printer = retrieve_logging_objects(cli_sections["default"])

    targets = []
    # We don't want to store targets argument back to file, thus remove it
    for item in list(cli_sections["default"].contents.pop("targets", "")):
        targets.append(item.lower())

    default_sections = load_config_file(StringConstants.system_coafile,
                                        log_printer)

    user_sections = load_config_file(
        StringConstants.user_coafile,
        log_printer,
        silent=True)

    default_config = str(default_sections["default"].get("config", ".coafile"))
    user_config = str(user_sections["default"].get("config", default_config))
    config = os.path.abspath(
        str(cli_sections["default"].get("config", user_config)))

    coafile_sections = load_config_file(config, log_printer)

    sections = merge_section_dicts(default_sections, user_sections)

    sections = merge_section_dicts(sections, coafile_sections)

    sections = merge_section_dicts(sections, cli_sections)

    for section in sections:
        if section != "default":
            sections[section].defaults = sections["default"]

    close_objects(interactor, log_printer)
    interactor, log_printer = retrieve_logging_objects(sections["default"])

    return interactor, log_printer, sections, targets


def gather_configuration(arg_list=sys.argv[1:]):
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

    :param arg_list: CLI args to use
    :return:         A tuple with the following contents:
                      * A dictionary with the sections
                      * Dictionary of list of local bears for each section
                      * Dictionary of list of global bears for each section
                      * The targets list
                      * The interactor (needs to be closed!)
                      * The log printer (needs to be closed!)
    """
    interactor, log_printer, sections, targets = (
        load_configuration(arg_list))
    local_bears, global_bears = fill_settings(sections,
                                              interactor,
                                              log_printer)
    save_sections(sections)
    warn_nonexistent_targets(targets, sections, log_printer)

    return (sections,
            local_bears,
            global_bears,
            targets,
            interactor,
            log_printer)
