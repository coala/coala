class HelloWorld
    def initialize(name)
        @name = name.capitalize
    end
    def sayHi
        x = 1 # unused variables invoke a warning
        puts "Hello #{@name}!"
    end
