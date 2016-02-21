from bears.r.RLintBear import RLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear

good_file = """
fun <- function(one){
  one_plus_one <- one + 1
  four <- matrix(1:10, nrow =2)
  print(one_plus_one, four)
}""".split("\n")


bad_file = """
fun = function(one)
{
    one.plus.one <- one + 1
    four <-  matrix(1:10,nrow =2)
    print(one_plus_one , four)
}
""".split("\n")


RLintBearTest = verify_local_bear(RLintBear,
                                  invalid_files=(bad_file,),
                                  valid_files=(good_file,),
                                  tempfile_kwargs={"suffix": ".R"})
