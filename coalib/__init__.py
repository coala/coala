import sys
from os.path import join, dirname


VERSION_FILE = join(dirname(__file__), "VERSION")
with open(VERSION_FILE, 'r') as ver:
    VERSION = ver.readline().strip()


def assert_supported_version():  # pragma: no cover
    if not sys.version_info > (3, 2):
        print("coala supports only python 3.3 or later.")
        exit(4)
