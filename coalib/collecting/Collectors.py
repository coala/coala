import os

from coalib.collecting.Importers import iimport_objects
from coalib.misc.Decorators import yield_once
from coalib.misc.i18n import _
from coalib.parsing.Glob import iglob
from coalib.misc.StringConstants import StringConstants
from coalib.parsing.ConfParser import ConfParser

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
def icollect(file_paths, log_printer, files=True, dirs=True):
    """
    Evaluate globs in file paths and return all matching files.

    :param file_paths:  list of file paths that can include globs
    :param log_printer: where to log things that go wrong
    :param files:       True if files are to be collected
    :param dirs:        True if dirs are to be collected
    :return:            iterator that yields paths of all matching files
    :raises SystemExit: when getting an invalid pattern
    """
    for file_path in file_paths:
        try:
            for match in iglob(file_path, files=files, dirs=dirs):
                yield match
        except ValueError as exception:
            log_printer.err(
                _("The given glob '{glob}' contains an invalid pattern. "
                  "Detailed error is: {error_message}").format(
                    glob=file_path,
                    error_message=str(_(exception))))
            raise SystemExit(3)


def collect_files(file_paths, log_printer):
    """
    Evaluate globs in file paths and return all matching files

    :param file_paths: list of file paths that can include globs
    :return:           list of paths of all matching files
    """
    return list(icollect(file_paths, log_printer, dirs=False))


def collect_dirs(dir_paths, log_printer):
    """
    Evaluate globs in directory paths and return all matching directories

    :param dir_paths: list of file paths that can include globs
    :return:          list of paths of all matching directories
    """
    return list(icollect(dir_paths, log_printer, files=False))


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
    for bear_dir in icollect(bear_dirs, log_printer, files=False):
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


def _find_section_in_file(file_path, config_file):
    file_path = os.path.normpath(os.path.expanduser(file_path))
    config_file = os.path.normpath(os.path.expanduser(config_file))
    base_dir = os.path.dirname(config_file)

    conf_parser = ConfParser()
    applicable_sections = []
    try:
        all_sections = conf_parser.reparse(config_file)
    except conf_parser.FileNotFoundError:
        return False

    for section_name in all_sections:
        section = all_sections[section_name]
        if "files" in section:
            for file_pattern in section["files"]:
                abs_file_pattern = os.path.abspath(os.path.join(
                    base_dir, file_pattern))
                if file_path in iglob(abs_file_pattern):
                    applicable_sections.append(section_name)

    return applicable_sections


def collect_config_files(file_path, base_dir=None):
    """
    Uses the filepath to find all suitable config files and sections that
    can be used for the file, and gives it in the order of preference.

    :param file_path: The path of the file whose configs need to be
                      found
    :param base_dir:  The path from which coala will handle relative
                      paths
    :return:          A list of tuples containing the config file's
                      path and the Section which is applicable to
                      the given file
    """
    file_path = os.path.abspath(os.path.expanduser(file_path))
    possible_configs = []

    if not base_dir:
        base_dir = os.path.dirname(file_path)

    # Project config - Find the closest config in the parent directories
    old_dir = None
    next_dir = os.path.dirname(file_path)

    while not(next_dir == old_dir or old_dir == os.path.expanduser("~")):
        config_file = os.path.join(next_dir, ".coafile")
        sections = _find_section_in_file(file_path, config_file)
        if sections:
            possible_configs.append(config_file)

        old_dir = next_dir
        next_dir = os.path.dirname(next_dir)

    # User config - Find the user coafile
    config_file = StringConstants.user_coafile
    sections = _find_section_in_file(file_path, config_file)
    if sections:
        possible_configs.append(config_file)

    # System config - Find the system coafile
    config_file = StringConstants.system_coafile
    sections = _find_section_in_file(file_path, config_file)
    if sections:
        possible_configs.append(config_file)

    return possible_configs
