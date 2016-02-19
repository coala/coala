import sys


def assert_supported_version():  # pragma: no cover
    if (not sys.version_info > (3, 3) or
            (sys.version_info[:2] == (3, 3))):
        print("coala supports only python 3.3 or later.")
        exit(4)
