import copy

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting import Dependencies
from coalib.collecting.Collectors import collect_bears
from coalib.settings.Setting import Setting


def fill_settings(sections, acquire_settings, log_printer):
    """
    Retrieves all bears and requests missing settings via the given
    acquire_settings method.

    This will retrieve all bears and their dependencies.

    :param sections:         The sections to fill up, modified in place.
    :param acquire_settings: The method to use for requesting settings. It will
                             get a parameter which is a dictionary with the
                             settings name as key and a list containing a
                             description in [0] and the names of the bears
                             who need this setting in all following indexes.
    :param log_printer:      The log printer to use for logging.
    :return:                 A tuple containing (local_bears, global_bears),
                             each of them being a dictionary with the section
                             name as key and as value the bears as a list.
    """
    local_bears = {}
    global_bears = {}

    for section_name, section in sections.items():
        bear_dirs = section.bear_dirs()
        bears = list(section.get('bears', ''))
        section_local_bears, section_global_bears = collect_bears(
            bear_dirs,
            bears,
            [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL],
            log_printer)
        section_local_bears = Dependencies.resolve(section_local_bears)
        section_global_bears = Dependencies.resolve(section_global_bears)
        all_bears = copy.deepcopy(section_local_bears)
        all_bears.extend(section_global_bears)
        fill_section(section, acquire_settings, log_printer, all_bears)

        local_bears[section_name] = section_local_bears
        global_bears[section_name] = section_global_bears

    return local_bears, global_bears


def fill_section(section, acquire_settings, log_printer, bears):
    """
    Retrieves needed settings from given bears and asks the user for
    missing values.

    If a setting is requested by several bears, the help text from the
    latest bear will be taken.

    :param section:          A section containing available settings. Settings
                             will be added if some are missing.
    :param acquire_settings: The method to use for requesting settings. It will
                             get a parameter which is a dictionary with the
                             settings name as key and a list containing a
                             description in [0] and the names of the bears
                             who need this setting in all following indexes.
    :param log_printer:      The log printer for logging.
    :param bears:            All bear classes or instances.
    :return:                 The new section.
    """
    # Retrieve needed settings.
    prel_needed_settings = {}
    for bear in bears:
        needed = bear.get_non_optional_settings()
        for key in needed:
            if key in prel_needed_settings:
                prel_needed_settings[key].append(bear.name)
            else:
                prel_needed_settings[key] = [needed[key][0],
                                             bear.name]

    # Strip away existent settings.
    needed_settings = {}
    for setting, help_text in prel_needed_settings.items():
        if not setting in section:
            needed_settings[setting] = help_text

    # Get missing ones.
    if len(needed_settings) > 0:
        new_vals = acquire_settings(log_printer, needed_settings, section)
        for setting, help_text in new_vals.items():
            section.append(Setting(setting, help_text))

    return section
