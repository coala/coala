import os
import sys

from coalib.misc.i18n import _

# We use circleci for doing dev releases continuously from master to pypi
build_num = os.getenv('CIRCLE_BUILD_NUM')
if build_num is None:  # pragma: no cover
    build_num = 0

version = (0, 1, 1, "dev"+str(build_num))
version_str = ".".join(str(part) for part in version)


def assert_supported_version():  # pragma: no cover
    if sys.version_info < (3, 2):
        print(_("coala supports only python 3.2 or later."))
        exit(1)
