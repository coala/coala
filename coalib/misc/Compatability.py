import sys


if sys.version_info < (3, 3):  # pragma: no cover
    FileNotFoundError = (IOError, OSError)
else:
    FileNotFoundError = FileNotFoundError
