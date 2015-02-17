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
        self.default_section = None
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
            self.default_section = self.conf_parser.reparse(os.path.abspath(
                os.path.join(StringConstants.coalib_root,
                             "default_coafile")))["default"]
        except self.conf_parser.FileNotFoundError:
            self.cli_sections["default"].retrieve_logging_objects()
            self.cli_sections["default"].log_printer.err(
                _("The global default coafile for the settings was not found. "
                  "It seems your installation is broken.") + " " +
                StringConstants.THIS_IS_A_BUG)
            raise SystemExit

        # We dont want to store targets argument back to file, thus remove it
        for item in list(self.cli_sections["default"].contents.pop("targets",
                                                                   "")):
            self.targets.append(item.lower())

        for section in self.cli_sections:
            self.cli_sections[section].defaults = self.default_section

        try:
            config = os.path.abspath(
                str(self.cli_sections["default"].get("config", "./coafile")))
            self.sections = self.conf_parser.reparse(config)

            # We'll get the default section as default section for every
            # section in this dict with this. Furthermore we will have the
            # CLI Values take precedence over the conf values.
            self._merge_section_dicts()
        except self.conf_parser.FileNotFoundError:
            self.sections = self.cli_sections

    def _fill_settings(self):
        for section_name in self.sections:
            section = self.sections[section_name]
            section.retrieve_logging_objects()

            bear_dirs = path_list(section["bear_dirs"])
            bear_dirs.append(os.path.join(StringConstants.coalib_bears_root,
                                          "**"))
            local_bears = collect_bears(bear_dirs,
                                        list(section["bears"]),
                                        [BEAR_KIND.LOCAL])
            global_bears = collect_bears(bear_dirs,
                                         list(section["bears"]),
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
            if bool(default_section["save"]):
                self.conf_writer = ConfWriter(str(default_section["config"]))
        except ValueError:
            self.conf_writer = ConfWriter(str(default_section["save"]))

        if self.conf_writer is not None:
            self.conf_writer.write_sections(self.sections)

    def _merge_section_dicts(self):
        for name in self.cli_sections:
            if name in self.sections:
                self.sections[name].update(
                    self.cli_sections[name],
                    ignore_defaults=(name != "default"))
            else:
                # no deep copy needed
                self.sections[name] = self.cli_sections[name]

    def _warn_nonexistent_targets(self):
        for target in self.targets:
            if target not in self.sections:
                self.sections["default"].log_printer.warn(
                    _("No section matches the target '{target}'. Thus it "
                      "cannot be executed.").format(target=target))
