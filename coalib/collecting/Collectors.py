from coalib.misc.Decorators import yield_once
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.parsing.Glob import iglob


@yield_once
def icollect_files(file_paths):
    """
    Evaluate globs in file paths and return all matching files
    :param file_paths: list of file paths that can include globs
    :param log_printer: log_printer to handle logging
    :return: iterator that yields paths of all matching files
    """
    for file_path in file_paths:
        for match in iglob(file_path, dirs=False):
            yield match


def collect_files(file_paths, log_printer=ConsolePrinter()):
    """
    Evaluate globs in file paths and return all matching files
    :param file_paths: list of file paths that can include globs
    :param log_printer: log_printer to handle logging
    :return: list of paths of all matching files
    """
    return list(icollect_files(file_paths))