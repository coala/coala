import logging
import subprocess
import sys


def main():
    logging.warning('Use of `coala-json` binary is deprecated, use '
                    'coala --json` instead.')

    args = ['coala', '--json']

    args += sys.argv[1:]

    return subprocess.call(args, shell=True)


if __name__ == '__main__':  # pragma: no cover
    main()
