from bears.general.LineLengthBear import LineLengthBear
from bears.tests.LocalBearTestHelper import verify_local_bear


test_file = """
test
too
er
e
""".split("\n")


LineLengthBear1Test = verify_local_bear(LineLengthBear,
                                        valid_files=(test_file,),
                                        invalid_files=(["testa"],
                                                       ["test line"]),
                                        settings={"max_line_length": "4"})


LineLengthBear2Test = verify_local_bear(LineLengthBear,
                                        valid_files=(test_file,
                                                     ["http://a.domain.de"]),
                                        invalid_files=(["asdasd"],),
                                        settings={
                                            "max_line_length": "4",
                                            "ignore_length_regex": "http://"})
