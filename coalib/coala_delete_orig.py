import logging
import os

from coalib.output.Logging import configure_logging
from coalib.parsing import Globbing
from coalib.parsing.Globbing import glob_escape
from coalib.settings.ConfigurationGathering import get_config_directory
from coalib.settings.Section import Section


def main(log_printer=None, section: Section=None):
    configure_logging()
    if log_printer is not None:
        logging.warning('Using log_printer is deprecated, '
                        'use python inbuilt logging instead.')

    start_path = get_config_directory(section)

    if start_path is None:
        return 255

    # start_path may have unintended glob characters
    orig_files = Globbing.glob(os.path.join(
        glob_escape(start_path), '**', '*.orig'))

    not_deleted = 0
    for ofile in orig_files:
        logging.info('Deleting old backup file... '
                     + os.path.relpath(ofile))
        try:
            os.remove(ofile)
        except OSError as oserror:
            not_deleted += 1
            logging.warn("Couldn't delete {}. {}".format(
                os.path.relpath(ofile), oserror.strerror))

    if not_deleted:
        logging.warn(str(not_deleted) + ' .orig backup files could not be'
                     ' deleted, possibly because you lack the permission'
                     ' to do so. coala may not be able to create'
                     ' backup files when patches are applied.')
    return 0


if __name__ == '__main__':  # pragma: no cover
    main()
