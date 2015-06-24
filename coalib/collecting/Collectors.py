import os

from coalib.collecting.Importers import iimport_objects
from coalib.misc.Decorators import yield_once
from coalib.misc.i18n import _
from coalib.parsing.Globbing import iglob


def _yield_if_right_kind(bear_class, kinds):
    try:
        if bear_class.kind() in kinds:
            yield bear_class
    except NotImplementedError:
        pass


def _import_bears(file_path, kinds):
    # recursive imports:
    for bear_list in iimport_objects(file_path,
                                     names='__additional_bears__',
                                     types=list):
        for bear_class in bear_list:
            for valid_bear_class in _yield_if_right_kind(bear_class, kinds):
                yield valid_bear_class
    # normal import
    for bear_class in iimport_objects(file_path,
                                      attributes='kind',
                                      local=True):
        for valid_bear_class in _yield_if_right_kind(bear_class, kinds):
            yield valid_bear_class


@yield_once
def icollect(file_paths):
    """
    Evaluate globs in file paths and return all matching files.

    :param file_paths:  list of file paths that can include globs
    :return:            iterator that yields paths of all matching files
    """
    for file_path in file_paths:
        for match in iglob(file_path):
            yield match


def collect_files(file_paths):
    """
    Evaluate globs in file paths and return all matching files

    :param file_paths: list of file paths that can include globs
    :return:           list of paths of all matching files
    """
    return list(filter(os.path.isfile, icollect(file_paths)))


def collect_dirs(dir_paths):
    """
    Evaluate globs in directory paths and return all matching directories

    :param dir_paths: list of file paths that can include globs
    :return:          list of paths of all matching directories
    """
    return list(filter(os.path.isdir, icollect(dir_paths)))


@yield_once
def icollect_bears(bear_dirs, bear_names, kinds, log_printer):
    """
    Collect all bears from bear directories that have a matching kind.

    :param bear_dirs:   directories that can contain bears
    :param bear_names:  names of bears
    :param kinds:       list of bear kinds to be collected
    :param log_printer: log_printer to handle logging
    :return:            iterator that yields bear classes
    """
    for bear_dir in filter(os.path.isdir, icollect(bear_dirs)):
        for bear_name in bear_names:
            for matching_file in iglob(
                    os.path.join(bear_dir, bear_name + '.py')):

                try:
                    for bear in _import_bears(matching_file, kinds):
                        yield bear
                except:
                    log_printer.warn(_("Unable to collect bears from {file}. "
                                       "Probably the file is malformed or "
                                       "the module code raises an exception.")
                                     .format(file=matching_file))


def collect_bears(bear_dirs, bear_names, kinds, log_printer):
    """
    Collect all bears from bear directories that have a matching kind.

    :param bear_dirs:   directories that can contain bears
    :param bear_names:  names of bears
    :param kinds: list  of bear kinds to be collected
    :param log_printer: log_printer to handle logging
    :return:            list of matching bear classes
    """
    return list(icollect_bears(bear_dirs, bear_names, kinds, log_printer))
