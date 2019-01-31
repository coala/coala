import copy
from inspect import signature
import logging

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting import Dependencies
from coalib.collecting.Collectors import (
    collect_bears, collect_bears_by_aspects)
from coalib.settings.Setting import Setting


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
    prel_needed_settings, _ = get_required_and_optional_settings(bears)

    # Strip away existent settings.
    needed_settings = {}
    for setting, help_text in prel_needed_settings.items():
        if setting not in section:
            needed_settings[setting] = help_text

    # Get missing ones.
    if len(needed_settings) > 0:
        if len(signature(acquire_settings).parameters) == 2:
            new_vals = acquire_settings(None, needed_settings)
        else:
            logging.warning('acquire_settings: section parameter is '
                            'deprecated.')
            new_vals = acquire_settings(None, needed_settings, section)

        for setting, help_text in new_vals.items():
            section.append(Setting(setting, help_text))

    return section


def get_required_and_optional_settings(bears):
    """
    Given a list of bears, retrieves the required and optional settings for
    each bear, and returns as a dict.

    :param bears: All bear classes or instances.
    :return:      A tuple with a dict for required and a dict for optional
                  settings. Each dict of settings has keys representing the
                  setting name, and the value is a list of bear names for
                  which that setting is required or optional.
    """
    required_settings = {}
    optional_settings = {}
    for bear in bears:
        needed = bear.get_non_optional_settings()
        optional = bear.get_optional_settings()
        for key in needed:
            if key in required_settings:
                required_settings[key].append(bear.name)
            else:
                required_settings[key] = [needed[key][0],
                                          bear.name]
        for key in optional:
            if key in optional_settings:
                optional_settings[key].append(bear.name)
            else:
                optional_settings[key] = [optional[key][0],
                                          bear.name]
    return (required_settings, optional_settings)


def warn_extraneous_settings(bears, parsed_settings):
    """
    Warns the user if any of the settings are not used by any of the
    given bears.

    :param bears:           All bear classes or instances.
    :param parsed_settings: List of dicts, where each dict has a setting
                            and value key, corresponding to each custom
                            setting.
    """
    (required_settings,
        optional_settings) = get_required_and_optional_settings(bears)
    for setting_definition in parsed_settings:
        if (setting_definition['setting'] not in required_settings and
                setting_definition['setting'] not in optional_settings):
            logging.warning('Setting \'{}\' is not used by any bear, '
                            'ignoring'.format(setting_definition['setting']))


def get_section_bears(section):
    """
    Returns all local and global bears from a given section.

    :param section: Section from which to get local and global bears.
    :return:        A tuple containing a list of local bears in the section,
                    and a list of the global bears in the section.
    """
    bear_dirs = section.bear_dirs()
    if getattr(section, 'aspects', None):
        section_local_bears, section_global_bears = (
            collect_bears_by_aspects(
                section.aspects,
                [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL]))
    else:
        bears = list(section.get('bears', ''))
        section_local_bears, section_global_bears = collect_bears(
            bear_dirs,
            bears,
            [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL])
    section_local_bears = Dependencies.resolve(section_local_bears)
    section_global_bears = Dependencies.resolve(section_global_bears)
    return section_local_bears, section_global_bears


def get_all_bears_from_sections(sections):
    """
    Returns a list of all bears from a a list of sections.

    :param sections: Sections with bears to get.
    :return:         A list of all bears in the sections.
    """
    all_bears_from_sections = []
    for _, section in sections.items():
        section_local_bears, section_global_bears = get_section_bears(section)
        all_bears_from_sections.extend(section_local_bears)
        all_bears_from_sections.extend(section_global_bears)
    return all_bears_from_sections


def fill_settings(sections,
                  acquire_settings,
                  log_printer=None,
                  fill_section_method=fill_section,
                  targets=None,
                  **kwargs):
    """
    Retrieves all bears and requests missing settings via the given
    acquire_settings method.

    This will retrieve all bears and their dependencies.

    :param sections:            The sections to fill up, modified in place.
    :param acquire_settings:    The method to use for requesting settings. It
                                will get a parameter which is a dictionary with
                                the settings name as key and a list containing
                                a description in [0] and the names of the bears
                                who need this setting in all following indexes.
    :param log_printer:         The log printer to use for logging.
    :param fill_section_method: Method to be used to fill the section settings.
    :param targets:             List of section names to be executed which are
                                passed from cli.
    :param kwargs:              Any other arguments for the fill_section_method
                                can be supplied via kwargs, which are passed
                                directly to the fill_section_method.
    :return:                    A tuple containing (local_bears, global_bears),
                                each of them being a dictionary with the
                                section name as key and as value the bears as a
                                list.
    """
    local_bears = {}
    global_bears = {}

    for section_name, section in sections.items():
        section_local_bears, section_global_bears = get_section_bears(section)
        all_bears = copy.deepcopy(section_local_bears)
        all_bears.extend(section_global_bears)
        if targets is None or section.is_enabled(targets):
            fill_section_method(section,
                                acquire_settings,
                                None,
                                all_bears,
                                **kwargs)

        local_bears[section_name] = section_local_bears
        global_bears[section_name] = section_global_bears

    return local_bears, global_bears
