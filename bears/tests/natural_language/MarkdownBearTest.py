from bears.natural_language.MarkdownBear import MarkdownBear
from bears.tests.LocalBearTestHelper import verify_local_bear

test_file1 = """1. abc
1. def
""".splitlines()


test_file2 = """1. abc
2. def
""".splitlines()


MarkdownBear1Test = verify_local_bear(MarkdownBear,
                                      valid_files=(test_file2,),
                                      invalid_files=(test_file1,))

MarkdownBear2Test = verify_local_bear(MarkdownBear,
                                      valid_files=(test_file1,),
                                      invalid_files=(test_file2,),
                                      settings={
                                          "markdown_list_increment": False})
