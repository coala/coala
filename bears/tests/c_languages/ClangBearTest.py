import sys
import unittest

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import generate_local_bear_test
from bears.c_languages.ClangBear import ClangBear
from clang.cindex import Index, LibclangError


ClangBearTest = generate_local_bear_test(
    ClangBear,
    (["int main() {}"], ),
    (["bad things, this is no C code"],  # Has no fixit
     ["struct { int f0; } x = { f0 :1 };"],  # Has a fixit and no range
     ["int main() {int *b; return b}"]),  # Has a fixit and a range
    'test.c')


ClangBearIgnoreTest = generate_local_bear_test(
    ClangBear,
    # Should ignore the warning, valid!
    (["struct { int f0; } x = { f0 :1 };"],),
    (),
    'test.c',
    settings={'clang_cli_options': '-w'})


def skip_test():
    try:
        Index.create()
        return False
    except LibclangError as error:
        return str(error)


if __name__ == '__main__':
    unittest.main(verbosity=2)
