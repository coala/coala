from bears.natural_language.ProseLintBear import ProseLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear


good_file = ["The 50s were swell."]
bad_file = ["The 50's were swell."]


ProseLintBearTest = verify_local_bear(ProseLintBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,))
