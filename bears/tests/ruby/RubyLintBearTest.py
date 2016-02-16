from bears.ruby.RubyLintBear import RubyLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear

good_file = """
class HelloWorld
    def initialize(name)
        @name = name.capitalize
    end
    def sayHi
        puts "Hello #{@name}!"
    end
end
""".split("\n")


bad_file = """
class HelloWorld
    def initialize(name)
        @name = name.capitalize
    end
    def sayHi
        x = 1 # unused variables invoke a warning
        puts "Hello #{@name}!"
    end
"""


RubyLintBearTest = verify_local_bear(RubyLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
