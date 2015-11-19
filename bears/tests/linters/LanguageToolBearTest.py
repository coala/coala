import sys
import unittest

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import generate_local_bear_test
from bears.linters.LanguageToolBear import LanguageToolBear


LanguageToolBearTest = generate_local_bear_test(
    LanguageToolBear,
    valid_files=(["A correct English sentence sounds nice in everyone's "
                  "ears."], ),
    invalid_files=(["  "],
                   ["asdgaasdfgahsadf"],
                   ['"quoted"']),
    settings={'use_spaces': 'true'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
