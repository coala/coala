import os

# We use circleci for doing dev releases continuously from master to pypi
build_num = os.getenv('CIRCLE_BUILD_NUM')
if build_num is None:  # pragma: no cover
    build_num = 0

version = (0, 1, 1, "dev"+str(build_num))
version_str = ".".join(str(part) for part in version)
