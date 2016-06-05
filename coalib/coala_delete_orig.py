import os
import pathlib

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.output.printers.LogPrinter import LogPrinter
from coalib.parsing import Globbing
from coalib.settings.ConfigurationGathering import get_config_directory
from coalib.settings.Section import Section
from coalib.parsing.Globbing import glob_escape


def main(log_printer=None, section: Section=None):
    start_path = get_config_directory(section)
    log_printer = log_printer or LogPrinter(ConsolePrinter())

    if start_path is None:
        return 255

    path = pathlib.Path(start_path)

    # start_path may have unintended glob characters
    pathlib_orig_files = path.glob("**/*.orig")


    not_deleted = 0
    for ofile in pathlib_orig_files:
        log_printer.info("Deleting old backup file... "
                         + str(ofile))
        try:
            ofile.unlink()
        except (FileNotFoundError, PermissionError, OSError) as error:
            not_deleted += 1
            log_printer.warn("Couldn't delete {}. {}".format(
                str(ofile), error.strerror))

    if not_deleted:
        log_printer.warn(str(not_deleted) + " .orig backup files could not be"
                         " deleted, possibly because you lack the permission"
                         " to do so. coala may not be able to create"
                         " backup files when patches are applied.")
    return 0


if __name__ == '__main__':  # pragma: no cover
    main()
