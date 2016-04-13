import sys
from os.path import join, dirname


VERSION_FILE = join(dirname(__file__), "VERSION")
with open(VERSION_FILE, 'r') as ver:
    VERSION = ver.readline().strip()

# Needed by setup.py and thus cannot live in Constants as it contains the
# appdirs import that will break setup if appdirs isn't available yet.
BUS_NAME = "org.coala_analyzer.v1"


def assert_supported_version():  # pragma: no cover
    if not sys.version_info > (3, 2):
        print("coala supports only python 3.3 or later.")
        exit(4)
