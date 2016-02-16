from bears.c_languages.IndentBear import IndentBear
from bears.tests.LocalBearTestHelper import verify_local_bear

test_file1 = """
int
main ()
{
    return 0;
}""".split("\n")

test_file2 = """
int
main ()
{
  return 0;
}""".split("\n")


test_file3 = """
int
main ()
{
\treturn 0;
}""".split("\n")


test_file4 = """
int main() {
  return 0;
}""".split("\n")


IndentBear1Test = verify_local_bear(IndentBear,
                                    valid_files=(test_file1,),
                                    invalid_files=(test_file3,),
                                    settings={"use_spaces": "true",
                                              "max_line_length": "80"})


IndentBear2Test = verify_local_bear(IndentBear,
                                    valid_files=(test_file3,),
                                    invalid_files=(),
                                    settings={"use_spaces": "nope",
                                              "max_line_length": "80"})


IndentBear3Test = verify_local_bear(IndentBear,
                                    valid_files=(test_file2,),
                                    invalid_files=(),
                                    settings={"use_spaces": "true",
                                              "max_line_length": "80",
                                              "tab_width": "2"})


IndentBear4Test = verify_local_bear(IndentBear,
                                    valid_files=(),
                                    invalid_files=(test_file4,),
                                    settings={"use_spaces": "true",
                                              "max_line_length": "80"})
