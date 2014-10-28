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
from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.output.LogPrinter import LogPrinter
from coalib.output.Outputter import Outputter
from coalib.settings.Setting import Setting
from coalib.settings.Settings import Settings
from coalib.misc.i18n import _


class SettingsFiller:
    def __init__(self, settings, outputter, log_printer):
        """
        A SettingsFiller object probes all bears for needed settings. It then prompts the user for those values and
        stores them in the original settings given.

        :param settings: The settings which are available. They will be modified if some are missing.
        :param outputter: An outputter to ask the user things.
        :param log_printer: A log printer for warning messages.
        """
        if not isinstance(settings, Settings):
            raise TypeError("The settings parameter has to be of type Settings.")
        if not isinstance(outputter, Outputter):
            raise TypeError("The outputter parameter has to be of type Outputter.")
        if not isinstance(log_printer, LogPrinter):
            raise TypeError("The outputter parameter has to be of type LogPrinter.")

        self.settings = settings
        self.outputter = outputter
        self.log_printer = log_printer

    def fill_settings(self, bears):
        """
        Retrieves needed settings from given bears and asks the user for missing values.

        If a setting is requested by several bears, the help text from the latest bear will be taken.

        :param bears: All bear classes or instances.
        :return: self.settings
        """
        if not isinstance(bears, list):
            raise TypeError("The bears parameter has to be a list of bear classes or instances.")

        # Retrieve needed settings.
        prel_needed_settings = {}
        for bear in bears:
            if not hasattr(bear, "get_needed_settings"):
                self.log_printer.log(LOG_LEVEL.WARNING,
                                     _("One of the given bears ({}) has no attribute get_needed_settings.")
                                     .format(str(bear)))
            else:
                needed = bear.get_needed_settings()
                for key in needed:
                    if key in prel_needed_settings:
                        prel_needed_settings[key].append(bear.__name__)
                    else:
                        prel_needed_settings[key] = [needed[key], bear.__name__]

        # Strip away existent settings.
        needed_settings = {}
        for setting, help_text in prel_needed_settings.items():
            if not setting in self.settings:
                needed_settings[setting] = help_text

        # Get missing ones.
        if len(needed_settings) > 0:
            new_vals = self.outputter.acquire_settings(needed_settings)
            for setting, help_text in new_vals.items():
                self.settings.append(Setting(setting, help_text))

        return self.settings
