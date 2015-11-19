import sys
import unittest

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import generate_local_bear_test
from bears.linters.ClangBear import ClangBear
from coalib.bearlib.parsing.clang.cindex import Index, LibclangError


ClangBearTest = generate_local_bear_test(
    ClangBear,
    (["int main() {}"], ),
    (["bad things, this is no C code"],  # Has no fixit
     ["struct { int f0; } x = { f0 :1 };"],  # Has a fixit and no range
     ["int main() {int *b; return b}"]),  # Has a fixit and a range
    'test.c')


def skip_test():
    try:
        Index.create()
        return False
    except LibclangError as error:
        return str(error)


if __name__ == '__main__':
    unittest.main(verbosity=2)
