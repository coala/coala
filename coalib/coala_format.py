import logging
import sys

from coalib.coala import main as coala_main


def main():
    logging.warning('Use of `coala-format` binary is deprecated, use '
                    '`coala --format` instead.')

    sys.argv = ['coala', '--format'] + sys.argv[1:]

    return coala_main()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
