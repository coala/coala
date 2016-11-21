import logging
import sys

from coalib.coala import main as coala_main


def main():
    logging.warning('Use of `coala-format` binary is deprecated, use '
                    '`coala --format` instead.')

    sys.argv.append('--format')

    return coala_main()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
