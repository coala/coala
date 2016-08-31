from coalib.files.Fileproxy import Fileproxy
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL


def get_file_dict(filename_list, log_printer):
    """
    Reads all files into a dictionary.

    :param filename_list: List of names of paths to files to get contents of.
    :param log_printer:   The logger which logs errors.
    :return:              Reads the content of each file into a dictionary
                          with filenames as keys.
    """
    file_dict = {}
    for filename in filename_list:
        try:
            file_dict[filename] = Fileproxy(filename)
        except UnicodeDecodeError:
            log_printer.warn("Failed to read file '{}'. It seems to contain "
                             "non-unicode characters. Leaving it "
                             "out.".format(filename))
        except OSError as exception:  # pragma: no cover
            log_printer.log_exception("Failed to read file '{}' because of "
                                      "an unknown error. Leaving it "
                                      "out.".format(filename),
                                      exception,
                                      log_level=LOG_LEVEL.WARNING)

    log_printer.debug("Files that will be checked:\n" +
                      "\n".join(file_dict.keys()))
    return file_dict
