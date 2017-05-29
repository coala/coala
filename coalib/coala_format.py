import logging
import sys

from coalib.coala import main as coala_main


def main(debug=False):
    logging.warning('Use of `coala-format` executable is deprecated, use '
                    '`coala --format` instead.')

    sys.argv.append('--format')

    return coala_main(debug=debug)


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
