import logging

from coalib.core import Core


def run():
    # TODO Process program arguments. Pass them as parameter?


    # TODO run bears branch

    # TODO get sections
    sections = None

    filenames_per_section = {section: get_files_from_section(section)
                             for section in sections}

    all_filenames = {filename
                     for filenames in filenames_per_section.values()
                     for filename in filenames}

    master_filedict = load_files(all_filenames)

    for section in sections:
        filedict = {filename: master_filedict[filename]
                    for filename in filenames_per_section[section]}

        bear_classes = get_bear_classes_from_section(section)
        bears = instantiate_bears(bear_classes, section, filedict)

        Core.run(bears, on_result)


def get_files_from_section(section):
    # TODO
    return section['files']


def get_bear_classes_from_section(section):
    bear_names = section['bears']
    # TODO collect bears
    return set()


def instantiate_bears(bear_classes, section, file_dict):
    """
    Instantiates each bear with the arguments it needs.

    :param bear_classes:
        An iterable of bear classes/types that shall be instantiated.
    :param section:
        The section the bears belong to.
    :param file_dict:
        Dictionary containing filenames and their contents.
    :return:
        A set of instantiated bears.
    """
    # TODO merge local and global bear list to instantiate.

    bears = set()

    # TODO What about other exceptions? Shall the core run?
    for bear_class in bear_classes:
        try:
            bears.add(bear_class(section, file_dict))
        # TODO Shall we introduce an own exception? In this case I dislike
        # TODO   using a built-in for prerequisite checking...
        except RuntimeError:
            pass

    return bears


def load_files(filenames):
    """
    Loads all files specified and arranges them inside a file-dictionary, where
    the keys are the filenames and the values the contents of the file
    (line-split including return characters).

    Files that fail to load are ignored and emit a log-warning.

    :param filenames:
        The names of the files to load.
    :return:
        A dictionary containing the filenames as keys and maps to the according
        file-contents.
    """
    file_dict = {}

    for filename in filenames:
        try:
            with open(filename, 'r', encoding='utf-8') as fl:
                lines = tuple(fl.readlines())

            file_dict[filename] = lines

        except UnicodeDecodeError:
            logging.warning(
                "Failed to read file '{}'. It seems to contain non-unicode "
                'characters. Leaving it out.'.format(filename))
        except OSError as ex:  # pragma: no cover
            logging.warning(
                "Failed to read file '{}' because of an unknown error. "
                'Leaving it out.'.format(filename), exc_info=ex)

    logging.debug('Following files loaded:\n' + '\n'.join(file_dict.keys()))

    return file_dict


def on_result(result):
    pass
