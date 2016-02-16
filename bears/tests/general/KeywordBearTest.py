from bears.general.KeywordBear import KeywordBear
from bears.tests.LocalBearTestHelper import verify_local_bear

test_file = """
test line fix me
to do
error fixme
""".split("\n")


SpaceConsistencyBearTest = verify_local_bear(KeywordBear,
                                             valid_files=(test_file),
                                             invalid_files=("test line FIXME",
                                                            "test line todo",
                                                            "test line warNING",
                                                            "test line ERROR"),
                                             settings={
                                                "cs_keywords": "FIXME, ERROR",
                                                "ci_keywords": "todo, warning"})
