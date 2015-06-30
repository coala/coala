import os
import sys

from coalib.misc.i18n import _

# We use circleci for doing dev releases continuously from master to pypi
BUILD_NUM = os.getenv('CIRCLE_BUILD_NUM')
if BUILD_NUM is None:  # pragma: no cover
    BUILD_NUM = 0

VERSION = (0, 1, 1, "dev"+str(BUILD_NUM))
VERSION_STR = ".".join(str(part) for part in VERSION)


def assert_supported_version():  # pragma: no cover
    if sys.version_info < (3, 2):
        print(_("coala supports only python 3.2 or later."))
        exit(1)
