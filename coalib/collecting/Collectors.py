import functools
import logging
import os
import pkg_resources
import itertools

from pyprint.NullPrinter import NullPrinter

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Importers import iimport_objects
from coala_utils.decorators import yield_once
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.parsing.Globbing import fnmatch, iglob, glob_escape
from coalib.output.printers.LogPrinter import LogPrinter


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
def icollect(file_paths, ignored_globs=None, match_cache={}):
    """
    Evaluate globs in file paths and return all matching files.

    :param file_paths:    File path or list of such that can include globs
    :param ignored_globs: List of globs to ignore when matching files
    :param match_cache:   Dictionary to use for caching results
    :return:              Iterator that yields tuple of path of a matching
                          file, the glob where it was found
    """
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    for file_path in file_paths:
        if file_path not in match_cache:
            match_cache[file_path] = list(iglob(file_path))

        for match in match_cache[file_path]:
            if not ignored_globs or not fnmatch(match, ignored_globs):
                yield match, file_path


def collect_files(file_paths, log_printer, ignored_file_paths=None,
                  limit_file_paths=None, section_name=''):
    """
    Evaluate globs in file paths and return all matching files

    :param file_paths:         File path or list of such that can include globs
    :param ignored_file_paths: List of globs that match to-be-ignored files
    :param limit_file_paths:   List of globs that the files are limited to
    :param section_name:       Name of currently executing section
    :return:                   List of paths of all matching files
    """
    limit_fnmatch = (functools.partial(fnmatch, globs=limit_file_paths)
                     if limit_file_paths else lambda fname: True)

    valid_files = list(filter(lambda fname: os.path.isfile(fname[0]),
                              icollect(file_paths, ignored_file_paths)))

    # Find globs that gave no files and warn the user
    if valid_files:
        collected_files, file_globs_with_files = zip(*valid_files)
    else:
        collected_files, file_globs_with_files = [], []

    _warn_if_unused_glob(log_printer, file_paths, file_globs_with_files,
                         'No files matching \'{}\' were found. '
                         'If this rule is not required, you can remove it '
                         'from section [' + section_name + '] in your '
                         '.coafile to deactivate this warning.')
    limited_files = list(filter(limit_fnmatch, collected_files))
    return limited_files


def collect_dirs(dir_paths, ignored_dir_paths=None):
    """
    Evaluate globs in directory paths and return all matching directories

    :param dir_paths:         File path or list of such that can include globs
    :param ignored_dir_paths: List of globs that match to-be-ignored dirs
    :return:                  List of paths of all matching directories
    """
    valid_dirs = list(filter(lambda fname: os.path.isdir(fname[0]),
                             icollect(dir_paths, ignored_dir_paths)))
    if valid_dirs:
        collected_dirs, _ = zip(*valid_dirs)
        return list(collected_dirs)
    else:
        return []


@yield_once
def icollect_bears(bear_dir_glob, bear_globs, kinds, log_printer):
    """
    Collect all bears from bear directories that have a matching kind.

    :param bear_dir_glob: Directory globs or list of such that can contain bears
    :param bear_globs:    Globs of bears to collect
    :param kinds:         List of bear kinds to be collected
    :param log_printer:   Log_printer to handle logging
    :return:              Iterator that yields a tuple with bear class and
                          which bear_glob was used to find that bear class.
    """
    for bear_dir, dir_glob in filter(lambda x: os.path.isdir(x[0]),
                                     icollect(bear_dir_glob)):
        # Since we get a real directory here and since we
        # pass this later to iglob, we need to escape this.
        bear_dir = glob_escape(bear_dir)
        for bear_glob in bear_globs:
            matching_files = iglob(os.path.join(bear_dir, bear_glob + '.py'))

            matching_files = sorted(matching_files)

            for matching_file in matching_files:
                try:
                    for bear in _import_bears(matching_file, kinds):
                        yield bear, bear_glob
                except pkg_resources.VersionConflict as exception:
                    log_printer.log_exception(
                        ('Unable to collect bears from {file} because there '
                         'is a conflict with the version of a dependency '
                         'you have installed. This may be resolved by '
                         'creating a separate virtual environment for coala '
                         'or running `pip3 install \"{pkg}\"`. Be aware that '
                         'the latter solution might break other python '
                         'packages that depend on the currently installed '
                         'version.').format(file=matching_file,
                                            pkg=exception.req),
                        exception, log_level=LOG_LEVEL.WARNING)
                except BaseException as exception:
                    log_printer.log_exception(
                        'Unable to collect bears from {file}. Probably the '
                        'file is malformed or the module code raises an '
                        'exception.'.format(file=matching_file),
                        exception,
                        log_level=LOG_LEVEL.WARNING)


def collect_bears(bear_dirs, bear_globs, kinds, log_printer,
                  warn_if_unused_glob=True):
    """
    Collect all bears from bear directories that have a matching kind
    matching the given globs.

    :param bear_dirs:           Directory name or list of such that can contain
                                bears.
    :param bear_globs:          Globs of bears to collect.
    :param kinds:               List of bear kinds to be collected.
    :param log_printer:         log_printer to handle logging.
    :param warn_if_unused_glob: True if warning message should be shown if a
                                glob didn't give any bears.
    :return:                    Tuple of list of matching bear classes based on
                                kind. The lists are in the same order as kinds.
    """
    bears_found = tuple([] for i in range(len(kinds)))
    bear_globs_with_bears = set()
    for bear, glob in icollect_bears(bear_dirs, bear_globs, kinds, log_printer):
        index = kinds.index(_get_kind(bear))
        bears_found[index].append(bear)
        bear_globs_with_bears.add(glob)

    if warn_if_unused_glob:
        _warn_if_unused_glob(log_printer, bear_globs, bear_globs_with_bears,
                             'No bears matching \'{}\' were found. Make sure '
                             'you have coala-bears installed or you have typed '
                             'the name correctly.')
    return bears_found


def filter_section_bears_by_languages(bears, languages):
    """
    Filters the bears by languages.

    :param bears:       The dictionary of the sections as keys and list of
                        bears as values.
    :param languages:   Languages that bears are being filtered on.
    :return:            New dictionary with filtered out bears that don't match
                        any language from languages.
    """
    new_bears = {}
    # All bears with "all" languages supported shall be shown
    languages = set(language.lower() for language in languages) | {'all'}
    for section in bears.keys():
        new_bears[section] = tuple(
            bear for bear in bears[section]
            if {language.lower() for language in bear.LANGUAGES} & languages)
    return new_bears


def collect_bears_by_aspects(aspects, kinds):
    """
    Collect bear based on aspects.

    Return a list of bears that have capability to analyze all aspects from
    given AspectList requirement.

    :param aspects: An AspectList that need to be covered.
    :param kinds:   List of bear kinds to be collected.
    :return:        Tuple of list of bear classes based on kind. The lists are
                    in the same order as kinds.
    """
    all_bears = get_all_bears()
    bears_found = tuple([] for i in range(len(kinds)))
    unfulfilled_aspects = []
    for aspect in aspects.get_leaf_aspects():
        for bear in all_bears:
            if (aspect in bear.aspects['detect'] or
                    aspect in bear.aspects['fix']):
                index = kinds.index(_get_kind(bear))
                # Avoid duplicate
                if bear not in bears_found[index]:
                    bears_found[index].append(bear)
                break
        else:
            unfulfilled_aspects.append(type(aspect).__qualname__)

    if unfulfilled_aspects:
        logging.warning('coala cannot find bear that could analyze the '
                        'following aspects: {}'.format(unfulfilled_aspects))
    return bears_found


def filter_capabilities_by_languages(bears, languages):
    """
    Filters the bears capabilities by languages.

    :param bears:       Dictionary with sections as keys and list of bears as
                        values.
    :param languages:   Languages that bears are being filtered on.
    :return:            New dictionary with languages as keys and their bears
                        capabilities as values. The capabilities are stored in a
                        tuple of two elements where the first one represents
                        what the bears can detect, and the second one what they
                        can fix.
    """
    languages = set(language.lower() for language in languages)
    language_bears_capabilities = {language: (
        set(), set()) for language in languages}
    for section_bears in bears.values():
        for bear in section_bears:
            bear_language = (
                ({language.lower() for language in bear.LANGUAGES} | {'all'}) &
                languages)
            language = bear_language.pop() if bear_language else ''
            capabilities = (language_bears_capabilities[language]
                            if language else tuple())
            language_bears_capabilities.update(
                {language: (capabilities[0] | bear.can_detect,
                            capabilities[1] | bear.CAN_FIX)}
                if language else {})
    return language_bears_capabilities


def get_all_bears():
    """
    Get a ``list`` of all available bears.
    """
    from coalib.settings.Section import Section
    printer = LogPrinter(NullPrinter())
    local_bears, global_bears = collect_bears(
        Section('').bear_dirs(),
        ['**'],
        [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL],
        printer,
        warn_if_unused_glob=False)
    return list(itertools.chain(local_bears, global_bears))


def get_all_bears_names():
    """
    Get a ``list`` of names of all available bears.
    """
    return [bear.name for bear in get_all_bears()]


def collect_all_bears_from_sections(sections, log_printer):
    """
    Collect all kinds of bears from bear directories given in the sections.

    :param sections:    List of sections so bear_dirs are taken into account
    :param log_printer: Log_printer to handle logging
    :return:            Tuple of dictionaries of local and global bears.
                        The dictionary key is section class and
                        dictionary value is a list of Bear classes
    """
    local_bears = {}
    global_bears = {}
    for section in sections:
        bear_dirs = sections[section].bear_dirs()
        local_bears[section], global_bears[section] = collect_bears(
            bear_dirs,
            ['**'],
            [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL],
            log_printer,
            warn_if_unused_glob=False)
    return local_bears, global_bears


def _warn_if_unused_glob(log_printer, globs, used_globs, message):
    """
    Warn if a glob has not been used.

    :param log_printer: The log_printer to handle logging.
    :param globs:       List of globs that were expected to be used.
    :param used_globs:  List of globs that were actually used.
    :param message:     Warning message to display if a glob is unused.
                        The glob which was unused will be added using
                        .format()
    """
    unused_globs = set(globs) - set(used_globs)
    for glob in unused_globs:
        log_printer.warn(message.format(glob))


def collect_registered_bears_dirs(entrypoint):
    """
    Searches setuptools for the entrypoint and returns the bear
    directories given by the module.

    :param entrypoint: The entrypoint to find packages with.
    :return:           List of bear directories.
    """
    collected_dirs = []
    for ep in pkg_resources.iter_entry_points(entrypoint):
        registered_package = None
        try:
            registered_package = ep.load()
        except pkg_resources.DistributionNotFound:
            continue
        collected_dirs.append(os.path.abspath(
            os.path.dirname(registered_package.__file__)))
    return collected_dirs
