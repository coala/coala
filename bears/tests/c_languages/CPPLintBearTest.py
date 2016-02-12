from bears.c_languages.CPPLintBear import CPPLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear


test_file = """
int main() {
    return 0;
}
""".split("\n")

CPPLintBear1Test = verify_local_bear(CPPLintBear,
                                     valid_files=(),
                                     invalid_files=(test_file,),
                                     tempfile_kwargs={"suffix": ".cpp"})

CPPLintBear2Test = verify_local_bear(CPPLintBear,
                                     valid_files=(test_file,),
                                     invalid_files=(),
                                     settings={'cpplint_ignore': 'legal'},
                                     tempfile_kwargs={"suffix": ".cpp"})

CPPLintBear3Test = verify_local_bear(CPPLintBear,
                                     valid_files=(),
                                     invalid_files=(test_file,),
                                     settings={'cpplint_ignore': 'legal',
                                               'max_line_length': '13'},
                                     tempfile_kwargs={"suffix": ".cpp"})
