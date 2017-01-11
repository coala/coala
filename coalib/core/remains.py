# TODO THESE ARE REMAINS FROM MY WORK, EXCLUDE FROM MERGE!

import logging

from coalib.settings.Setting import glob_list
from coalib.collecting.Collectors import collect_files


def get_filenames_from_section(section):
    """
    Returns all filenames that are requested for analysis in the given
    ``section``.

    :param section:
        The section to load the filenames from.
    :return:
        An iterable of filenames.
    """
    # TODO Deprecate log-printer on collect_files
    return collect_files(
        glob_list(section.get('files', '')),
        None,
        ignored_file_paths=glob_list(section.get('ignore', '')),
        limit_file_paths=glob_list(section.get('limit_files', '')))


# TODO Test this. Especially with multi-section setup.
# This is useful for the later parallel multi-section execution.
# TODO need to adjust it to take in multiple sections instead of bears, as
# TODO   bears already require a populated file-dict. (Okay it can be empty
# TODO   and populated later, though this is not a nice approach.)

# TODO OKAY! This has to be core independent, the user is responsible for
# TODO   correctly initializing bears. As this also allows for virtual
# TODO   files or improves speed for plugins, these could grab the already
# TODO   loaded contents from RAM instead of reloading them from file.
def load_files(bears):
    """
    Loads all files specified in the sections of the bears and arranges them
    inside a file-dictionary, where the keys are the filenames and the values
    the contents of the file (line-split including return characters).

    Files that fail to load are ignored and emit a log-warning.

    :param bears:
        The bears to load the specified files from.
    :return:
        A dictionary containing as keys the section instances mapping to the
        according file-dictionary, which contains filenames as keys and maps
        to the according file-contents.
    """
    section_to_file_dict = {}
    master_file_dict = {}
    # Use this list to not load corrupt/erroring files twice, as this produces
    # doubled log messages.
    corrupt_files = set()

    for section, bears_per_section in groupby(bears,
                                              key=lambda bear: bear.section):
        filenames = get_filenames_from_section(section)

        file_dict = {}
        for filename in filenames:
            try:
                if filename in master_file_dict:
                    file_dict[filename] = master_file_dict[filename]
                elif filename in corrupt_files:
                    # Ignore corrupt files that were already tried to load.
                    pass
                else:
                    with open(filename, 'r', encoding='utf-8') as fl:
                        lines = tuple(fl.readlines())
                    file_dict[filename] = lines
                    master_file_dict[filename] = lines
            except UnicodeDecodeError:
                logging.warning(
                    "Failed to read file '{}'. It seems to contain non-"
                    'unicode characters. Leaving it out.'.format(filename))
                corrupt_files.add(filename)
            except OSError as ex:  # pragma: no cover
                logging.warning(
                    "Failed to read file '{}' because of an unknown error. "
                    'Leaving it out.'.format(filename), exc_info=ex)
                corrupt_files.add(filename)

    logging.debug('Following files loaded:\n' + '\n'.join(
        master_file_dict.keys()))

    return section_to_file_dict
