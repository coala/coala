import unittest

from bears.tests.LocalBearTestHelper import verify_local_bear
from bears.c_languages.ClangBear import ClangBear


ClangBearTest = verify_local_bear(
    ClangBear,
    (["int main() {}"], ),
    (["bad things, this is no C code"],  # Has no fixit
     ["struct { int f0; } x = { f0 :1 };"],  # Has a fixit and no range
     ["int main() {int *b; return b}"]),  # Has a fixit and a range
    'test.c')


ClangBearIgnoreTest = verify_local_bear(
    ClangBear,
    # Should ignore the warning, valid!
    (["struct { int f0; } x = { f0 :1 };"],),
    (),
    'test.c',
    settings={'clang_cli_options': '-w'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
