import os
import copy

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Collectors import collect_bears
from coalib.misc.StringConstants import StringConstants
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.settings.Setting import Setting, path_list
from coalib.misc.i18n import _


def fill_settings(sections, interactor, log_printer):
    """
    Retrieves all bears and requests missing settings via the given interactor.

    :param sections:    The sections to fill up, will be modified in place.
    :param interactor:  The interactor to request the missing settings from.
    :param log_printer: The log printer to use for logging.
    :return:            A tuple containing (local_bears, global_bears), each
                        of them being a dictionary with the section name as
                        key and as value the bears as a list.
    """
    local_bears = {}
    global_bears = {}

    for section_name, section in sections.items():
        bear_dirs = path_list(section.get("bear_dirs", ""))
        bear_dirs.append(os.path.join(StringConstants.coalib_bears_root,
                                      "**"))
        bears = list(section.get("bears", ""))
        section_local_bears = collect_bears(bear_dirs,
                                            bears,
                                            [BEAR_KIND.LOCAL],
                                            log_printer)
        section_global_bears = collect_bears(bear_dirs,
                                             bears,
                                             [BEAR_KIND.GLOBAL],
                                             log_printer)
        all_bears = copy.deepcopy(section_local_bears)
        all_bears.extend(section_global_bears)
        fill_section(section, interactor, log_printer, all_bears)

        local_bears[section_name] = section_local_bears
        global_bears[section_name] = section_global_bears

    return local_bears, global_bears


def fill_section(section, interactor, log_printer, bears):
    """
    Retrieves needed settings from given bears and asks the user for
    missing values.

    If a setting is requested by several bears, the help text from the
    latest bear will be taken.


    :param section:     A section containing available settings. Settings
                        will be added if some are missing.
    :param interactor:  The interactor to use for requesting settings.
    :param log_printer: The log printer for logging.
    :param bears:       All bear classes or instances.
    :return:            The new section
    """
    # Retrieve needed settings.
    prel_needed_settings = {}
    for bear in bears:
        if not hasattr(bear, "get_non_optional_settings"):
            log_printer.log(
                LOG_LEVEL.WARNING,
                _("One of the given bears ({}) has no attribute "
                  "get_non_optional_settings.").format(str(bear)))
        else:
            needed = bear.get_non_optional_settings()
            for key in needed:
                if key in prel_needed_settings:
                    prel_needed_settings[key].append(bear.__name__)
                else:
                    prel_needed_settings[key] = [needed[key][0],
                                                 bear.__name__]

    # Strip away existent settings.
    needed_settings = {}
    for setting, help_text in prel_needed_settings.items():
        if not setting in section:
            needed_settings[setting] = help_text

    # Get missing ones.
    if len(needed_settings) > 0:
        new_vals = interactor.acquire_settings(needed_settings)
        for setting, help_text in new_vals.items():
            section.append(Setting(setting, help_text))

    return section
