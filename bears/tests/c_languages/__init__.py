from unittest.case import skip, skipIf

from clang.cindex import Index, LibclangError


def skip_if_no_clang():
    """
    Decorate your test with this to skip it if clang isn't present.
    """
    try:
        Index.create()
        return skipIf(False, '')
    except LibclangError as error:
        return skip(str(error))
