from coalib.files.Fileproxy import Fileproxy
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.collecting.Collectors import collect_files
from coalib.settings.Setting import glob_list


def get_file_dict(section, cache, log_printer):
    """
    Reads all files into a dictionary.

    :param section:     The section the bears belong to.
    :param cache:       List of names of paths to files to get contents of.
    :param log_printer: The logger which logs errors.
    :return:            Reads the content of each file into a dictionary
                        with filenames as keys.
    """
    filename_list = collect_files(
        glob_list(section.get('files', "")),
        log_printer,
        ignored_file_paths=glob_list(section.get('ignore', "")),
        limit_file_paths=glob_list(section.get('limit_files', "")))

    # This stores all matched files irrespective of whether coala is run
    # only on changed files or not. Global bears require all the files
    complete_filename_list = filename_list

    # Start tracking all the files
    if cache:
        print(cache.data)
        cache.track_files(set(complete_filename_list))
        print(cache.data)
        changed_files = cache.get_uncached_files(
            set(filename_list)) if cache else filename_list

        # If caching is enabled then the local bears should process only the
        # changed files.
        log_printer.debug("coala is run only on changed files, bears' log "
                          "messages from previous runs may not appear. You may "
                          "use the `--flush-cache` flag to see them.")
        filename_list = changed_files

    complete_file_dict = {}
    for filename in filename_list:
        try:
            complete_file_dict[filename] = Fileproxy(filename)
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
                      "\n".join(complete_file_dict.keys()))

    file_dict = {filename: complete_file_dict[filename]
                 for filename in filename_list
                 if filename in complete_file_dict}

    return complete_file_dict, file_dict
