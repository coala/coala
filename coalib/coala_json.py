import logging
import sys

from coalib.coala import main as coala_main


def main():
    logging.warning('Use of `coala-json` binary is deprecated, use '
                    'coala --json` instead.')

    sys.argv.append('--json')

    return coala_main()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
