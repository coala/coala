import logging


def load_files(sections):
    """
    Loads all files specified in the given sections and arranges them inside
    a file-dictionary, where the keys are the filenames and the values the
    contents of the file (line-split including return characters).

    Files that fail to load are ignored and emit a log-warning.

    :param sections:
        The sections to load the specified files from.
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

    for section in sections:
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


def on_result(result):
    pass
