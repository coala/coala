import functools
import os

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Importers import iimport_objects
from coalib.misc.Decorators import yield_once
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.parsing.Globbing import iglob, fnmatch


def _get_kind(bear_class):
    try:
        return bear_class.kind()
    except NotImplementedError:
        return None


def _import_bears(file_path, kinds):
    # recursive imports:
    for bear_list in iimport_objects(file_path,
                                     names='__additional_bears__',
                                     types=list):
        for bear_class in bear_list:
            if _get_kind(bear_class) in kinds:
                yield bear_class
    # normal import
    for bear_class in iimport_objects(file_path,
                                      attributes='kind',
                                      local=True):
        if _get_kind(bear_class) in kinds:
            yield bear_class


@yield_once
def icollect(file_paths):
    """
    Evaluate globs in file paths and return all matching files.

    :param file_paths:  file path or list of such that can include globs
    :return:            iterator that yields paths of all matching files
    """
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    for file_path in file_paths:
        for match in iglob(file_path):
            yield match


def collect_files(file_paths, ignored_file_paths=None, limit_file_paths=None):
    """
    Evaluate globs in file paths and return all matching files

    :param file_paths:         file path or list of such that can include globs
    :param ignored_file_paths: list of globs that match to-be-ignored files
    :param limit_file_paths:   list of globs that the files are limited to
    :return:                   list of paths of all matching files
    """
    ignore_fnmatch = (functools.partial(fnmatch, patterns=ignored_file_paths)
                      if ignored_file_paths else lambda fname: False)

    limit_fnmatch = (functools.partial(fnmatch, patterns=limit_file_paths)
                     if limit_file_paths else lambda fname: True)

    valid_files = list(filter(
        lambda fname: (os.path.isfile(fname) and
                       not ignore_fnmatch(fname) and limit_fnmatch(fname)),
        icollect(file_paths)))

    return valid_files


def collect_dirs(dir_paths, ignored_dir_paths=None):
    """
    Evaluate globs in directory paths and return all matching directories

    :param dir_paths:         file path or list of such that can include globs
    :param ignored_dir_paths: list of globs that match to-be-ignored dirs
    :return:                  list of paths of all matching directories
    """
    ignore_fnmatch = (functools.partial(fnmatch, patterns=ignored_dir_paths)
                      if ignored_dir_paths else lambda fname: False)
    valid_dirs = list(filter(
        lambda fname: os.path.isdir(fname) and not ignore_fnmatch(fname),
        icollect(dir_paths)))
    return valid_dirs


@yield_once
def icollect_bears(bear_dirs, bear_globs, kinds, log_printer):
    """
    Collect all bears from bear directories that have a matching kind.

    :param bear_dirs:   directory name or list of such that can contain bears
    :param bear_globs:  globs of bears to collect
    :param kinds:       list of bear kinds to be collected
    :param log_printer: log_printer to handle logging
    :return:            iterator that yields a tuple with bear class and
                        which bear_glob was used to find that bear class.
    """
    for bear_dir in filter(os.path.isdir, icollect(bear_dirs)):
        for bear_glob in bear_globs:
            for matching_file in iglob(
                    os.path.join(bear_dir, bear_glob + '.py')):

                try:
                    for bear in _import_bears(matching_file, kinds):
                        yield bear, bear_glob
                except BaseException as exception:
                    log_printer.log_exception(
                        "Unable to collect bears from {file}. Probably the "
                        "file is malformed or the module code raises an "
                        "exception.".format(file=matching_file),
                        exception,
                        log_level=LOG_LEVEL.WARNING)


def collect_bears(bear_dirs, bear_globs, kinds, log_printer):
    """
    Collect all bears from bear directories that have a matching kind
    matching the given globs.

    :param bear_dirs:   directory name or list of such that can contain bears
    :param bear_globs:  globs of bears to collect
    :param kinds:       list of bear kinds to be collected
    :param log_printer: log_printer to handle logging
    :return:            tuple of list of matching bear classes based on kind.
                        The lists are in the same order as `kinds`
    """
    bears_found = tuple([] for i in range(len(kinds)))
    bear_globs_with_bears = set()
    for bear, glob in icollect_bears(bear_dirs, bear_globs, kinds, log_printer):
        index = kinds.index(_get_kind(bear))
        bears_found[index].append(bear)
        bear_globs_with_bears.add(glob)

    empty_bear_globs = set(bear_globs) - set(bear_globs_with_bears)
    for glob in empty_bear_globs:
        log_printer.warn("No bears were found matching '{}'.".format(glob))

    return bears_found


def collect_all_bears_from_sections(sections, log_printer):
    """
    Collect all kinds of bears from bear directories given in the sections.

    :param bear_dirs:   directory name or list of such that can contain bears
    :param log_printer: log_printer to handle logging
    """
    local_bears = {}
    global_bears = {}
    for section in sections:
        bear_dirs = sections[section].bear_dirs()
        local_bears[section], global_bears[section] = collect_bears(
            bear_dirs,
            ["**"],
            [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL],
            log_printer)
    return local_bears, global_bears
