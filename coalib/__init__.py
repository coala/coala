import sys


def assert_supported_version():  # pragma: no cover
    if (not sys.version_info > (3, 2) or
            (sys.version_info[:2] == (3, 2) and
             '__pypy__' not in sys.builtin_module_names)):
        print("coala supports only pypy3 and python 3.3 or later.")
        exit(1)
