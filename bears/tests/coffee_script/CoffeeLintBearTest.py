from bears.coffee_script.CoffeeLintBear import CoffeeLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear

good_file = """
# Lint your CoffeeScript!

class Gangster

  wasItAGoodDay : () ->
    yes
""".split("\n")


warning_file = """
# Nested string interpolation
str = "Book by #{"#{firstName} #{lastName}".toUpperCase()}"
""".split("\n")


error_file = """
# Wrong capitalization
class theGangster

  wasItAGoodDay : () ->
    yes
""".split("\n")


invalid_file = """
# Coffeelint is buggy here and will generate an error with invalid CSV on this
var test
""".split("\n")


CoffeeLintBear1Test = verify_local_bear(CoffeeLintBear,
                                        valid_files=(good_file,),
                                        invalid_files=(warning_file,
                                                       error_file,
                                                       invalid_file))
