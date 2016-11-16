import logging
import subprocess
import sys


def main():
    logging.warning('Use of `coala-format` binary is deprecated, use '
                    '`coala --format` instead.')

    args = ['coala', '--format']

    args += sys.argv[1:]

    return subprocess.call(args, shell=True)


if __name__ == '__main__':  # pragma: no cover
    main()
