import functools
import logging
import os
import pkg_resources
import itertools
import re
from types import ModuleType

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Importers import iimport_objects
from coala_utils.decorators import yield_once
from coalib.misc.Exceptions import log_exception
from coalib.misc.IterUtilities import partition
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.parsing.Globbing import fnmatch, iglob, glob_escape
from coalib.bearlib.languages.Language import Languages
from coalib.bearlib.languages import definitions


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


def _sort_bears(bears, key=lambda x: x.name.lower(), reverse=False):
    """
    Sort the bear list according to the key provided.

    The default behaviour is to sort bears based on their names.

    :param bears:           List of bears to be sorted.
    :param key:             Key using which comparison should take place.
    :param reverse:         bool to decide order of sort.
    :return:                Sorted list of bears.
    """
    return sorted(bears, key=key, reverse=reverse)


@yield_once
def icollect(file_paths, ignored_globs=None, match_cache={},
             match_function=fnmatch):
    """
    Evaluate globs in file paths and return all matching files.

    :param file_paths:      File path or list of such that can include globs
    :param ignored_globs:   List of globs to ignore when matching files
    :param match_cache:     Dictionary to use for caching results
    :param match_function:  The function to use for glob matching
    :return:                Iterator that yields tuple of path of a matching
                            file, the glob where it was found
    """
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    if ignored_globs is None:
        ignored_globs = []
    for index, glob in enumerate(ignored_globs):
        if glob.endswith('/**') or glob.endswith('\\**'):
            logging.warning("Detected trailing globstar in ignore glob '{}'. "
                            "Please remove the unnecessary '**' from its end."
                            .format(glob))
            ignored_globs[index] = glob.rstrip('*')

    for file_path in file_paths:
        if file_path not in match_cache:
            match_cache[file_path] = list(iglob(file_path))

        for match in match_cache[file_path]:
            if not ignored_globs or not match_function(match, ignored_globs):
                yield match, file_path


def match_dir_or_file_pattern(path, ignore_patterns=None):
    """
    Tries to match the given path with the directory (substring match) or file
    (enforced full match) patterns.

    :param path:                Valid file path
    :param ignore_patterns:     List of regex patterns that match a file or a
                                directory
    :return:                    True if any of the given pattern match
    """
    def escape(pattern):
        return pattern.replace('\\', '\\\\')

    expanded_ignores = list_glob_results(ignore_patterns)

    file_patterns, dir_patterns = partition(
        expanded_ignores,
        os.path.isfile)

    return (
        any((re.match(escape(pattern), path) for pattern in dir_patterns)) or
        any((re.fullmatch(escape(pattern), path) for pattern in file_patterns)))


def list_glob_results(values=None):
    """
    Expands the globs of all given values and concatenates the results.

    :param values:  List of file-globs or files.
    :return:        List of matched files.
    """
    return functools.reduce(
        lambda seed, value: seed + list(iglob(value)),
        values if values else (),
        [])


def collect_files(file_paths, log_printer=None, ignored_file_paths=None,
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

    valid_files = list(
        filter(lambda fname: os.path.isfile(fname[0]),
               icollect(file_paths,
                        ignored_file_paths,
                        match_function=match_dir_or_file_pattern)))

    # Find globs that gave no files and warn the user
    if valid_files:
        collected_files, file_globs_with_files = zip(*valid_files)
    else:
        collected_files, file_globs_with_files = [], []

    _warn_if_unused_glob(file_paths, file_globs_with_files,
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
def icollect_bears(bear_dir_glob, bear_globs, kinds, log_printer=None):
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
                    log_exception(
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
                    log_exception(
                        'Unable to collect bears from {file}. Probably the '
                        'file is malformed or the module code raises an '
                        'exception.'.format(file=matching_file),
                        exception,
                        log_level=LOG_LEVEL.WARNING)


def collect_bears(bear_dirs, bear_globs, kinds, log_printer=None,
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
                                kind. The lists are in the same order as kinds
                                and not sorted based upon bear name.
    """
    bears_found = tuple([] for i in range(len(kinds)))
    bear_globs_with_bears = set()
    for bear, glob in icollect_bears(bear_dirs, bear_globs, kinds):
        index = kinds.index(_get_kind(bear))
        bears_found[index].append(bear)
        bear_globs_with_bears.add(glob)

    unused_globs = set(bear_globs) - set(bear_globs_with_bears)
    suffix_globs = {}

    for glob in unused_globs:
        if glob is not '**' and glob is not '*':
            if glob.endswith('bear'):  # pragma nt: no cover
                new_glob = glob[:-4] + 'B' + glob[-3:]
                suffix_globs[new_glob] = glob
            elif not glob.endswith('Bear'):
                suffix_globs[glob + 'Bear'] = glob

    for bear, glob in icollect_bears(bear_dirs,
                                     set(suffix_globs.keys()), kinds):
        index = kinds.index(_get_kind(bear))
        bears_found[index].append(bear)
        bear_globs_with_bears.add(suffix_globs[glob])

    if warn_if_unused_glob:
        _warn_if_unused_glob(bear_globs, bear_globs_with_bears,
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
                    in the same order as kinds and not sorted based upon bear
                    name.
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
    Get an unsorted ``list`` of all available bears.
    """
    from coalib.settings.Section import Section
    local_bears, global_bears = collect_bears(
        Section('').bear_dirs(),
        ['**'],
        [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL],
        warn_if_unused_glob=False)
    return list(itertools.chain(local_bears, global_bears))


def get_all_bears_names():
    """
    Get an unsorted ``list`` of names of all available bears.
    """
    return [bear.name for bear in get_all_bears()]


def _argcomplete_bears_names(*args, **kwargs):
    return get_all_bears_names()


def get_all_languages(include_unknown=False):
    """
    Get a ``tuple`` of all language instances supported by coala.

    :param include_unknown: Whether to include instance of
                            ``Unknown`` language.
    :return:                Tuple of all language instances
                            supported by coala.
    """
    languages = [
        key for key in definitions.__dict__
        if isinstance(definitions.__dict__[key], ModuleType)]
    if not include_unknown:
        languages.remove('Unknown')
    return Languages(languages)


def collect_all_bears_from_sections(sections,
                                    log_printer=None,
                                    bear_globs=('**',)):
    """
    Collect all kinds of bears from bear directories given in the sections.

    :param sections:    List of sections so bear_dirs are taken into account
    :param log_printer: Log_printer to handle logging
    :param bear_globs:  List of glob patterns.
    :return:            Tuple of dictionaries of unsorted local and
                        global bears. The dictionary key is section class and
                        dictionary value is a list of Bear classes
    """
    local_bears = {}
    global_bears = {}
    for section in sections:
        bear_dirs = sections[section].bear_dirs()
        local_bears[section], global_bears[section] = collect_bears(
            bear_dirs,
            bear_globs,
            [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL],
            warn_if_unused_glob=False)
    return local_bears, global_bears


def _warn_if_unused_glob(globs, used_globs, message):
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
        logging.warning(message.format(glob))


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
