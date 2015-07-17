import sys

from coalib.misc.i18n import _


def assert_supported_version():  # pragma: no cover
    if sys.version_info < (3, 2):
        print(_("coala supports only python 3.2 or later."))
        exit(1)
