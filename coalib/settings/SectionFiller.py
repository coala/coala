from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.output.LogPrinter import LogPrinter
from coalib.output.Interactor import Interactor
from coalib.settings.Setting import Setting
from coalib.settings.Section import Section
from coalib.misc.i18n import _


class SectionFiller:
    def __init__(self, section):
        """
        A SectionFiller object probes all bears for needed settings. It then prompts the user for those values and
        stores them in the original section given.

        :param section: A section containing available settings. Settings will be added if some are missing.
        """
        if not isinstance(section, Section):
            raise TypeError("The section parameter has to be of type Section.")

        self.section = section

    def fill_section(self, bears):
        """
        Retrieves needed settings from given bears and asks the user for missing values.

        If a setting is requested by several bears, the help text from the latest bear will be taken.

        :param bears: All bear classes or instances.
        :return: the new section
        """
        if not isinstance(bears, list):
            raise TypeError("The bears parameter has to be a list of bear classes or instances.")

        # Retrieve needed settings.
        prel_needed_settings = {}
        for bear in bears:
            if not hasattr(bear, "get_non_optional_settings"):
                self.section.log_printer.log(LOG_LEVEL.WARNING,
                                             _("One of the given bears ({}) has no attribute "
                                               "get_non_optional_settings.").format(str(bear)))
            else:
                needed = bear.get_non_optional_settings()
                for key in needed:
                    if key in prel_needed_settings:
                        prel_needed_settings[key].append(bear.__name__)
                    else:
                        prel_needed_settings[key] = [needed[key][0], bear.__name__]

        # Strip away existent settings.
        needed_settings = {}
        for setting, help_text in prel_needed_settings.items():
            if not setting in self.section:
                needed_settings[setting] = help_text

        # Get missing ones.
        if len(needed_settings) > 0:
            new_vals = self.section.interactor.acquire_settings(needed_settings)
            for setting, help_text in new_vals.items():
                self.section.append(Setting(setting, help_text))

        return self.section
