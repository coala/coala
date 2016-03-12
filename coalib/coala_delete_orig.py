import os

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.output.printers.LogPrinter import LogPrinter
from coalib.parsing import Globbing
from coalib.settings.ConfigurationGathering import get_config_directory
from coalib.settings.Section import Section


def main(log_printer=None, section: Section=None):
    start_path = get_config_directory(section)
    log_printer = log_printer or LogPrinter(ConsolePrinter())

    if start_path is None:
        return 255

    orig_files = Globbing.glob(os.path.abspath(
        os.path.join(start_path, '**', '*.orig')))

    not_deleted = 0
    for ofile in orig_files:
        log_printer.info("Deleting old backup file... "
                         + os.path.relpath(ofile))
        try:
            os.remove(ofile)
        except OSError as oserror:
            not_deleted += 1
            log_printer.warn("Couldn't delete {}. {}".format(
                os.path.relpath(ofile), oserror.strerror))

    if not_deleted:
        log_printer.warn(str(not_deleted) + " .orig backup files could not be"
                         " deleted, possibly because you lack the permission"
                         " to do so. coala may not be able to create"
                         " backup files when patches are applied.")
    return 0
