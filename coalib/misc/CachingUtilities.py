import calendar
import hashlib
import os
import pickle
import time

from coalib.output.Tagging import get_user_data_dir


def get_cache_data_path(log_printer, filename):
    """
    Get the full path of ``filename`` present in the user's cache directory.

    :param log_printer: A LogPrinter object to use for logging.
    :param filename:    The file whose path needs to be expanded.
    :return:            Full path of the file, assuming it's present in the
                        user's config directory.
    """
    return os.path.join(get_user_data_dir(
        log_printer, action="caching"), filename)


def delete_cache_files(log_printer, files):
    """
    Delete the cache files after displaying a warning saying the cache
    is corrupted and will be removed.

    :param log_printer: A LogPrinter object to use for logging.
    :param files:       The list of files to be deleted.
    :return:            True if all the given files were successfully deleted.
                        False otherwise.
    """
    error_files = []
    for file_name in files:
        file_path = get_cache_data_path(log_printer, file_name)
        cache_dir = os.path.dirname(file_path)
        try:
            os.remove(file_path)
        except OSError:
            error_files.append(file_name)

    if len(error_files) > 0:
        error_files = ", ".join(error_files)
        log_printer.warn("There was a problem deleting the following "
                         "files: " + error_files + ". Please delete "
                         "them manually from '" + cache_dir + "'")
        return False

    return True


def pickle_load(log_printer, filename, fallback=None):
    """
    Get the data stored in ``filename`` present in the user
    config directory. Example usage:

    >>> from pyprint.NullPrinter import NullPrinter
    >>> from coalib.output.printers.LogPrinter import LogPrinter
    >>> log_printer = LogPrinter(NullPrinter())
    >>> test_data = {"answer": 42}
    >>> pickle_dump(log_printer, "test_file", test_data)
    >>> pickle_load(log_printer, "test_file")
    {'answer': 42}
    >>> pickle_load(log_printer, "nonexistant_file")
    >>> pickle_load(log_printer, "nonexistant_file", fallback=42)
    42


    :param log_printer: A LogPrinter object to use for logging.
    :param filename:    The name of the file present in the user config
                        directory.
    :param fallback:    Return value to fallback to in case the file doesn't
                        exist.
    :return:            Data that is present in the file, if the file exists.
                        Otherwise the ``default`` value is returned.
    """
    filename = get_cache_data_path(log_printer, filename)
    if not os.path.isfile(filename):
        return fallback
    with open(filename, "rb") as f:
        try:
            return pickle.load(f)
        except (pickle.UnpicklingError, EOFError) as e:
            log_printer.warn("The caching database is corrupted and will "
                             "be removed. Each project will be re-cached "
                             "automatically in the next run time.")
            delete_cache_files(log_printer, files=[filename])
            return fallback


def pickle_dump(log_printer, filename, data):
    """
    Write ``data`` into the file ``filename`` present in the user
    config directory.

    :param log_printer: A LogPrinter object to use for logging.
    :param filename:    The name of the file present in the user config
                        directory.
    :param data:        Data to be serialized and written to the file using
                        pickle.
    """
    filename = get_cache_data_path(log_printer, filename)
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def time_consistent(log_printer, project_hash):
    """
    Verify if time is consistent with the last time was run. That is,
    verify that the last run time is in the past. Otherwise, the
    system time was changed and we need to flush the cache and rebuild.

    :param log_printer:  A LogPrinter object to use for logging.
    :param project_hash: A MD5 hash of the project directory to be used
                         as the key.
    :return:             Returns True if the time is consistent and as
                         expected; False otherwise.
    """
    time_db = pickle_load(log_printer, "time_db", {})
    if project_hash not in time_db:
        # This is the first time coala is run on this project, so the cache
        # will be new automatically.
        return True
    return time_db[project_hash] <= calendar.timegm(time.gmtime())


def update_time_db(log_printer, project_hash, current_time=None):
    """
    Update the last run time on the project.

    :param log_printer:  A LogPrinter object to use for logging.
    :param project_hash: A MD5 hash of the project directory to be used
                         as the key.
    :param current_time: Current time in epoch format. Not giving this
                         argument would imply using the current system time.
    """
    if not current_time:
        current_time = calendar.timegm(time.gmtime())
    time_db = pickle_load(log_printer, "time_db", {})
    time_db[project_hash] = current_time
    pickle_dump(log_printer, "time_db", time_db)


def get_settings_hash(sections):
    """
    Compute and return a unique hash for the settings.

    :param sections: A dict containing the settings for each section.
    :return:         A MD5 hash that is unique to the settings used.
    """
    settings = []
    for section in sections:
        settings.append(str(sections[section]))
    return hashlib.md5(str(settings).encode("utf-8")).hexdigest()


def settings_changed(log_printer, settings_hash):
    """
    Determine if the settings have changed since the last run with caching.

    :param log_printer:   A LogPrinter object to use for logging.
    :param settings_hash: A MD5 hash that is unique to the settings used.
    :return:              Return True if the settings hash has changed
                          Return False otherwise.
    """
    project_hash = hashlib.md5(os.getcwd().encode("utf-8")).hexdigest()

    settings_hash_db = pickle_load(log_printer, "settings_hash_db", {})
    if project_hash not in settings_hash_db:
        # This is the first time coala is run on this project, so the cache
        # will be flushed automatically.
        return False

    result = settings_hash_db[project_hash] != settings_hash
    if result:
        log_printer.warn("Since the configuration settings have been "
                         "changed since the last run, the "
                         "cache will be flushed and rebuilt.")

    return result


def update_settings_db(log_printer, settings_hash):
    """
    Update the config file last modification date.

    :param log_printer:   A LogPrinter object to use for logging.
    :param settings_hash: A MD5 hash that is unique to the settings used.
    """
    project_hash = hashlib.md5(os.getcwd().encode("utf-8")).hexdigest()

    settings_hash_db = pickle_load(log_printer, "settings_hash_db", {})
    settings_hash_db[project_hash] = settings_hash
    pickle_dump(log_printer, "settings_hash_db", settings_hash_db)
