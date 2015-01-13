"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import copy
import os
import sys
from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.BearCollector import BearCollector
from coalib.misc.StringConstants import StringConstants
from coalib.misc.i18n import _
from coalib.output.ConfWriter import ConfWriter
from coalib.parsing.CliParser import CliParser
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.SectionFiller import SectionFiller


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

    This is done when the run() method is invoked. Anything else is just helper stuff and initialization.
    """
    def __init__(self):
        self.cli_sections = None
        self.default_section = None
        self.conf_sections = None

        self.cli_parser = CliParser()
        self.conf_parser = ConfParser()
        self.conf_writer = None

        self.local_bears = {}
        self.global_bears = {}

    def run(self, arg_list=sys.argv[1:]):
        self._load_configuration(arg_list)
        self._fill_settings()
        self._save_configuration()

        return self.conf_sections, self.local_bears, self.global_bears

    def _load_configuration(self, arg_list):
        self.cli_sections = self.cli_parser.reparse(arg_list=arg_list)

        try:
            self.default_section = self.conf_parser.reparse(os.path.abspath(os.path.join(StringConstants.coalib_root,
                                                                                         "default_coafile")))["default"]
        except self.conf_parser.FileNotFoundError:
            self.cli_sections["default"].retrieve_logging_objects()
            self.cli_sections["default"].log_printer.err(_("The global default coafile for the settings was not found. "
                                                           "It seems your installation is broken.") + " " +
                                                         StringConstants.THIS_IS_A_BUG)
            raise SystemExit

        for section in self.cli_sections:
            self.cli_sections[section].defaults = self.default_section

        try:
            config = os.path.abspath(str(self.cli_sections["default"].get("config", "./coafile")))
            self.conf_sections = self.conf_parser.reparse(config)

            # We'll get the default section as default section for every section in this dict with this
            # Furthermore we will have the CLI Values take precedence over the conf values.
            self._merge_section_dicts()
        except self.conf_parser.FileNotFoundError:
            self.conf_sections = self.cli_sections

    def _fill_settings(self):
        for section_name in self.conf_sections:
            section = self.conf_sections[section_name]
            section.retrieve_logging_objects()
            local_bears = BearCollector.from_section([BEAR_KIND.LOCAL], section).collect()
            global_bears = BearCollector.from_section([BEAR_KIND.GLOBAL], section).collect()
            filler = SectionFiller(section)
            all_bears = copy.deepcopy(local_bears)
            all_bears.extend(global_bears)
            filler.fill_section(all_bears)

            self.local_bears[section_name] = local_bears
            self.global_bears[section_name] = global_bears

    def _save_configuration(self):
        self.conf_writer = None
        try:
            if bool(self.conf_sections["default"]["save"]):
                self.conf_writer = ConfWriter(str(self.conf_sections["default"]["config"]))
        except ValueError:
            self.conf_writer = ConfWriter(str(self.conf_sections["default"]["save"]))

        if self.conf_writer is not None:
            self.conf_writer.write_sections(self.conf_sections)

    def _merge_section_dicts(self):
        for section_name in self.cli_sections:
            if section_name in self.conf_sections:
                self.conf_sections[section_name].update(self.cli_sections[section_name])
            else:
                self.conf_sections[section_name] = self.cli_sections[section_name]  # no deep copy needed
