import calendar
import hashlib
import os
import pickle
import time

from coalib.output.Tagging import get_user_data_dir


def get_data_path(log_printer, identifier):
    """
    TODO, update

    :param log_printer: A LogPrinter object to use for logging.
    :param identifier:  Any string identifier to get the data path to.
    :return:            Full path of the file, assuming it's present in the
                        user's config directory.
    """
    return os.path.join(get_user_data_dir(
        log_printer, action="caching"), hash_id(identifier))


def delete_cache_files(log_printer, identifiers):
    """
    Delete the cache files after displaying a warning saying the cache
    is corrupted and will be removed.

    :param log_printer: A LogPrinter object to use for logging.
    :param files:       The list of files to be deleted.
    :return:            True if all the given files were successfully deleted.
                        False otherwise.
    """
    error_files = []
    for identifier in identifiers:
        file_path = get_cache_data_path(log_printer, identifier)
        try:
            os.remove(file_path)
        except OSError:
            error_files.append(file_path)

    if len(error_files) > 0:
        error_files = ", ".join(repr(file) for file in error_files)
        log_printer.warn("There was a problem deleting the following "
                         "files: {}. Please delete them "
                         "manually.".format(error_files))
        return False

    return True

def hash_id(identifier):
    """
    Hashes the given identifier.

    :param identifier:
    :return:
    """
    return hashlib.md5(identifier.encode("utf-8")).hexdigest()


def pickle_load(log_printer, identifier, fallback=None):
    """
    Get the data stored for the given identifier. Example usage:

    >>> from pyprint.NullPrinter import NullPrinter
    >>> from coalib.output.printers.LogPrinter import LogPrinter
    >>> log_printer = LogPrinter(NullPrinter())
    >>> test_data = {"answer": 42}
    >>> pickle_dump(log_printer, "test project", test_data)
    >>> pickle_load(log_printer, "test project")
    {'answer': 42}
    >>> pickle_load(log_printer, "nonexistant project")
    >>> pickle_load(log_printer, "nonexistant project", fallback=42)
    42


    :param log_printer: A LogPrinter object to use for logging.
    :param identifier:    The name of the file present in the user config
                        directory.
    :param fallback:    Return value to fallback to in case the file doesn't
                        exist.
    :return:            Data that is present in the file, if the file exists.
                        Otherwise the ``default`` value is returned.
    """
    filename = get_cache_data_path(log_printer, identifier)
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


def pickle_dump(log_printer, identifier, data):
    """
    Write ``data`` for the given identifier. It can be retrieved with pickle_load.

    :param log_printer: A LogPrinter object to use for logging.
    :param identifier:  TODO
    :param data:        Data to be serialized and written to the file using
                        pickle.
    """
    filename = get_cache_data_path(log_printer, identifier)
    with open(filename, "wb") as f:
        pickle.dump(data, f)


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
