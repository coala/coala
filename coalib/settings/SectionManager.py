import copy
import os
import sys

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Collectors import collect_bears
from coalib.misc.StringConstants import StringConstants
from coalib.misc.i18n import _
from coalib.output.ConfWriter import ConfWriter
from coalib.output.NullInteractor import NullInteractor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.output.printers.FilePrinter import FilePrinter
from coalib.output.printers.NullPrinter import NullPrinter
from coalib.output.ConsoleInteractor import ConsoleInteractor
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.parsing.CliParser import CliParser
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.Section import Section
from coalib.settings.SectionFiller import SectionFiller
from coalib.settings.Setting import path_list


class SectionManager:
    """
    The SectionManager does the following things:

    - Reading all settings in sections from
        - Default config
        - CLI
        - Configuration file
    - Collecting all the bears
    - Filling up all needed settings
    - Write back the new sections to the configuration file if needed
    - Give all information back to caller

    This is done when the run() method is invoked. Anything else is just helper
    stuff and initialization.
    """
    def __init__(self):
        self.cli_sections = None
        self.default_sections = None
        self.user_sections = None
        self.coafile_sections = None
        self.sections = None

        self.cli_parser = CliParser()
        self.conf_parser = ConfParser()
        self.conf_writer = None

        self.local_bears = {}
        self.global_bears = {}

        self.log_printer = None
        self.interactor = None

        self.targets = []

    def run(self, arg_list=sys.argv[1:]):
        self._load_configuration(arg_list)
        self.retrieve_logging_objects(self.sections["default"])
        self._fill_settings()
        self._save_configuration()
        self._warn_nonexistent_targets()

        return (self.sections,
                self.local_bears,
                self.global_bears,
                self.targets,
                self.interactor,
                self.log_printer)

    def _load_configuration(self, arg_list):
        self.cli_sections = self.cli_parser.reparse(arg_list=arg_list)
        self.retrieve_logging_objects(self.cli_sections["default"])
        # We dont want to store targets argument back to file, thus remove it
        for item in list(
                self.cli_sections["default"].contents.pop("targets", "")):
            self.targets.append(item.lower())

        self.default_sections = self._load_config_file(
            StringConstants.system_coafile)

        self.user_sections = self._load_config_file(
            StringConstants.user_coafile,
            silent=True)

        default_config = str(
            self.default_sections["default"].get("config", ".coafile"))
        user_config = str(
            self.user_sections["default"].get("config", default_config))
        config = os.path.abspath(str(
            self.cli_sections["default"].get("config", user_config)))

        self.coafile_sections = self._load_config_file(config)

        self.sections = self._merge_section_dicts(self.default_sections,
                                                  self.user_sections)

        self.sections = self._merge_section_dicts(self.sections,
                                                  self.coafile_sections)

        self.sections = self._merge_section_dicts(self.sections,
                                                  self.cli_sections)

        for section in self.sections:
            if section != "default":
                self.sections[section].defaults = self.sections["default"]

    def _load_config_file(self, filename, silent=False):
        """
        Loads sections from a config file. Prints an appropriate warning if
        it doesn't exist and returns a section dict containing an empty
        default section in that case.

        It assumes that the cli_sections are available.

        :param filename: The file to load settings from.
        :param silent:   Whether or not to warn the user if the file doesn't
                         exist.
        """
        filename = os.path.abspath(filename)

        try:
            return self.conf_parser.reparse(filename)
        except self.conf_parser.FileNotFoundError:
            if not silent:
                self.log_printer.warn(
                    _("The requested coafile '{filename}' does not exist. "
                      "Thus it will not be used.").format(filename=filename))

            return {"default": Section("default")}

    def retrieve_logging_objects(self, section):
        """
        Creates an appropriate log printer and interactor according to the
        settings.
        """
        log_type = str(section.get("log_type", "console")).lower()
        output_type = str(section.get("output", "console")).lower()
        str_log_level = str(section.get("log_level", "")).upper()
        log_level = LOG_LEVEL.str_dict.get(str_log_level, LOG_LEVEL.WARNING)

        if log_type == "console":
            self.log_printer = ConsolePrinter(log_level=log_level)
        else:
            try:
                # ConsolePrinter is the only printer which may not throw an
                # exception (if we have no bugs though) so well fallback to him
                # if some other printer fails
                if log_type == "none":
                    self.log_printer = NullPrinter()
                else:
                    self.log_printer = FilePrinter(filename=log_type,
                                                   log_level=log_level)
            except:
                self.log_printer = ConsolePrinter(log_level=log_level)
                self.log_printer.log(
                    LOG_LEVEL.WARNING,
                    _("Failed to instantiate the logging method '{}'. Falling "
                      "back to console output.").format(log_type))

        if output_type == "none":
            self.interactor = NullInteractor(log_printer=self.log_printer)
        else:
            self.interactor = ConsoleInteractor.from_section(
                section,
                log_printer=self.log_printer)

    def _fill_settings(self):
        for section_name in self.sections:
            section = self.sections[section_name]

            bear_dirs = path_list(section.get("bear_dirs", ""))
            bear_dirs.append(os.path.join(StringConstants.coalib_bears_root,
                                          "**"))
            bears = list(section.get("bears", ""))
            local_bears = collect_bears(bear_dirs,
                                        bears,
                                        [BEAR_KIND.LOCAL])
            global_bears = collect_bears(bear_dirs,
                                         bears,
                                         [BEAR_KIND.GLOBAL])
            filler = SectionFiller(section, self.interactor, self.log_printer)
            all_bears = copy.deepcopy(local_bears)
            all_bears.extend(global_bears)
            filler.fill_section(all_bears)

            self.local_bears[section_name] = local_bears
            self.global_bears[section_name] = global_bears

    def _save_configuration(self):
        self.conf_writer = None
        default_section = self.sections["default"]
        try:
            if bool(default_section.get("save", "false")):
                self.conf_writer = ConfWriter(str(
                    default_section.get("config", ".coafile")))
        except ValueError:
            self.conf_writer = ConfWriter(str(default_section.get("save",
                                                                  ".coafile")))

        if self.conf_writer is not None:
            self.conf_writer.write_sections(self.sections)

    @staticmethod
    def _merge_section_dicts(lower, higher):
        """
        Merges the section dictionaries. The values of higher will take
        precedence over the ones of lower. Lower will hold the modified dict in
        the end.
        """
        for name in higher:
            if name in lower:
                lower[name].update(higher[name], ignore_defaults=True)
            else:
                # no deep copy needed
                lower[name] = higher[name]

        return lower

    def _warn_nonexistent_targets(self):
        for target in self.targets:
            if target not in self.sections:
                self.log_printer.warn(
                    _("The requested section '{section}' is not existent. "
                      "Thus it cannot be executed.").format(section=target))
