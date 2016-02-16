from bears.natural_language.AlexBear import AlexBear
from bears.tests.LocalBearTestHelper import verify_local_bear

good_file = ["Their network looks good."]

bad_file = ["His network looks good."]


AlexBearTest = verify_local_bear(AlexBear,
                                 valid_files=(good_file,),
                                 invalid_files=(bad_file,))
