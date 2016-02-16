from bears.latex.LatexLintBear import LatexLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear


good_file = """
{.}
{ sometext }\\
""".split("\n")


bad_file = """
{ .}
{ Sometext \\
""".split("\n")


LatexLintBear1Test = verify_local_bear(LatexLintBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file,))
