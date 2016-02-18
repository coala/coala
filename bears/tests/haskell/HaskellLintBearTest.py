from bears.haskell.HaskellLintBear import HaskellLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear

good_file = """
myconcat = (++)
""".split("\n")

bad_file = """
myconcat a b = ((++) a b)
""".split("\n")

HaskellLintBear1Test = verify_local_bear(HaskellLintBear,
                                         valid_files=(good_file,),
                                         invalid_files=(bad_file,),
                                         tempfile_kwargs={"suffix": ".hs"})
