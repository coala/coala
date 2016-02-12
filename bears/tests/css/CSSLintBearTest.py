from bears.css.CSSLintBear import CSSLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear


good_file = """
.class {
  font-weight: 400;
  font-size: 5px;
}
""".split("\n")


bad_file = """
.class {
  font-weight: 400
  font-size: 5px;
}
""".split("\n")


CSSLintBear1Test = verify_local_bear(CSSLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
