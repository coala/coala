import logging
import sys

from coalib.coala import main as coala_main


def main():
    logging.warning('Use of `coala-ci` binary is deprecated, use '
                    '`coala --non-interactive` instead.')

    sys.argv.append('--non-interactive')

    return coala_main()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
