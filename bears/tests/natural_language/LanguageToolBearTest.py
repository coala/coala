import unittest

from bears.tests.LocalBearTestHelper import verify_local_bear
from bears.natural_language.LanguageToolBear import LanguageToolBear


LanguageToolBearTest = verify_local_bear(
    LanguageToolBear,
    valid_files=(["A correct English sentence sounds nice in everyone's "
                  "ears."], ),
    invalid_files=(["  "],
                   ["asdgaasdfgahsadf"],
                   ['"quoted"']),
    settings={'use_spaces': 'true'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
