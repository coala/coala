"""
The coalib package is a collection of various subpackages regarding
writing, executing and editing bears. Various other packages such as
formatting and settings are also included in coalib.
"""


import sys
from os.path import join, dirname


VERSION_FILE = join(dirname(__file__), 'VERSION')


def get_version():
    with open(VERSION_FILE, 'r') as ver:
        return ver.readline().strip()


VERSION = get_version()
__version__ = VERSION


def assert_supported_version():
    if sys.version_info < (3, 4):
        print('coala supports only python 3.4 or later.')
        exit(4)
