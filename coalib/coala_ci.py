import logging
import subprocess
import sys


def main():
    logging.warning('Use of `coala-ci` binary is deprecated, use '
                    '`coala --non-interactive` instead.')

    args = ['coala', '--non-interactive']

    args += sys.argv[1:]

    return subprocess.call(args, shell=True)


if __name__ == '__main__':  # pragma: no cover
    main()
