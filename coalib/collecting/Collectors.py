from coalib.misc.Decorators import yield_once
from coalib.parsing.Glob import iglob


@yield_once
def icollect_files(file_paths):
    """
    Evaluate globs in file paths and return all matching files
    :param file_paths: list of file paths that can include globs
    :return: iterator that yields paths of all matching files
    """
    for file_path in file_paths:
        for match in iglob(file_path, dirs=False):
            yield match


def collect_files(file_paths):
    """
    Evaluate globs in file paths and return all matching files
    :param file_paths: list of file paths that can include globs
    :return: list of paths of all matching files
    """
    return list(icollect_files(file_paths))


@yield_once
def icollect_dirs(dir_paths):
    """
    Evaluate globs in directory paths and return all matching directories
    :param dir_paths: list of file paths that can include globs
    :return: iterator that yields paths of all matching directories
    """
    for file_path in dir_paths:
        for match in iglob(file_path, files=False):
            yield match


def collect_dirs(dir_paths):
    """
    Evaluate globs in directory paths and return all matching directories
    :param dir_paths: list of file paths that can include globs
    :return: list of paths of all matching directories
    """

    return list(icollect_dirs(dir_paths))


@yield_once
def icollect_bears(bear_dirs, bear_names, kinds, log_printer=ConsolePrinter()):
    """
    Collect all bears from bear directories that have a matching kind.
    :param bear_dirs: directories that can contain bears
    :param bear_names: names of bears
    :param kinds: list of bear kinds to be collected
    :param log_printer: log_printer to handle logging
    :return: iterator that yields bear classes
    """
    for bear_dir in icollect_dirs(bear_dirs):
        for bear_name in bear_names:
            for matching_file in iglob(
                    os.path.join(bear_dir, bear_name + '.py')):

                try:
                    for bear in _import_bears(matching_file, kinds):
                        yield bear
                except:
                    log_printer.warn(_("unable to import bears from {}")
                                     .format(matching_file))


def collect_bears(bear_dirs, bear_names, kinds, log_printer=ConsolePrinter()):
    """
    Collect all bears from bear directories that have a matching kind.
    :param bear_dirs: directories that can contain bears
    :param bear_names: names of bears
    :param kinds: list of bear kinds to be collected
    :param log_printer: log_printer to handle logging
    :return: list of matching bear classes
    """
    return list(icollect_bears(bear_dirs, bear_names, kinds, log_printer))
