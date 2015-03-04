import copy
import os
import sys

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Collectors import collect_bears
from coalib.misc.StringConstants import StringConstants
from coalib.misc.i18n import _
from coalib.output.ConfWriter import ConfWriter
from coalib.parsing.CliParser import CliParser
from coalib.parsing.ConfParser import ConfParser
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
        self.coafile_sections = None
        self.sections = None

        self.cli_parser = CliParser()
        self.conf_parser = ConfParser()
        self.conf_writer = None

        self.local_bears = {}
        self.global_bears = {}

        self.targets = []

    def run(self, arg_list=sys.argv[1:]):
        self._load_configuration(arg_list)
        self._fill_settings()
        self._save_configuration()
        self._warn_nonexistent_targets()

        return self.sections, self.local_bears, self.global_bears, self.targets

    def _load_configuration(self, arg_list):
        self.cli_sections = self.cli_parser.reparse(arg_list=arg_list)

        try:
            self.default_sections = self.conf_parser.reparse(os.path.abspath(
                StringConstants.system_coafile))
        except self.conf_parser.FileNotFoundError:
            self.cli_sections["default"].retrieve_logging_objects()
            self.cli_sections["default"].log_printer.warn(
                _("The global default coafile for the settings was not found. "
                  "It seems your installation is broken.") + " " +
                StringConstants.THIS_IS_A_BUG)

        try:
            config = os.path.abspath(
                str(self.cli_sections["default"].get("config", ".coafile")))
            self.coafile_sections = self.conf_parser.reparse(config)
        except self.conf_parser.FileNotFoundError:
            self.cli_sections["default"].log_printer.warn(
                _("The requested coafile '{filename}' does not exist. "
                  "Thus it will not be used.").format(filename=config))

        # We dont want to store targets argument back to file, thus remove it
        for item in list(self.cli_sections["default"].contents.pop("targets",
                                                                   "")):
            self.targets.append(item.lower())

        self.sections = self._merge_section_dicts(self.default_sections,
                                                  self.coafile_sections)

        self.sections = self._merge_section_dicts(self.sections,
                                                  self.cli_sections)

        for section in self.sections:
            if section != "default":
                self.sections[section].defaults = self.sections["default"]

    def _fill_settings(self):
        for section_name in self.sections:
            section = self.sections[section_name]
            section.retrieve_logging_objects()

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
            filler = SectionFiller(section)
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
        if lower is None:
            return higher
        if higher is None:
            return lower

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
                self.sections["default"].log_printer.warn(
                    _("The requested section '{section}' is not existent. "
                      "Thus it cannot be executed.").format(section=target))
