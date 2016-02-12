from bears.natural_language.reSTLintBear import reSTLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear


good_file = ["test\n====\n"]
bad_file = ["test\n==\n"]


reSTLintBearTest = verify_local_bear(reSTLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
