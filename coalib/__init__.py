import sys


def assert_supported_version():  # pragma: no cover
    if not sys.version_info > (3, 2):
        print("coala supports only python 3.3 or later.")
        exit(4)
