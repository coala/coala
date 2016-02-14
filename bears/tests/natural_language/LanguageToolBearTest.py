from bears.tests.LocalBearTestHelper import verify_local_bear
from bears.natural_language.LanguageToolBear import LanguageToolBear


LanguageToolBearTest = verify_local_bear(
    LanguageToolBear,
    valid_files=(["A correct English sentence sounds nice to everyone."],),
    invalid_files=(["  "],
                   ["asdgaasdfgahsadf"],
                   ['"quoted"']))
