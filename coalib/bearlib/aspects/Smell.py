from coalib.bearlib.aspects import Taste, Root


@Root.subaspect
class Smell:
    """
    This aspect detects `code smells` or `bad smells` in your code.

    `Smells` are certain structures in the code that indicate violation of
    fundamental design principles. They are usually not bugs; they are not
    technically incorrect and do not currently prevent the program from
    functioning.
    """
    class docs:
        example = """
        * Feature envy
        * Data clump
        * Too large class
        * Too long parameter list
        etc...
        """
        example_language = 'English'
        importance_reason = """
        Even though they are not necessarily bugs, code smells increase the risk
        of bugs or failure in the future and may slow down development.
        """
        fix_suggestions = 'some fix suggestions'


@Smell.subaspect
class ClassSmell:
    """
    This aspect detects `code smells` or `bad smells` related to classes'
    definitions in your codebase.

    Class-level code smells are simply code smells indicating poorly defined
    classes (including too large classes or God object, data clump feature
    envy etc...) in your source code.
    """
    class docs:
        example = """
        * Too large classes
        * Data clump
        * Feature envy
        etc ...
        """
        example_language = 'English'
        importance_reason = """
        These classes (the classes containing code smells) should be
        refactored for better readability and maintainability of your source
        code.
        """
        fix_suggestions = """
        When a class is wearing too many (functional) hats, think about
        splitting it up:
            * Extract class
            * Extract subclass
            * Extract interface
        """


@Smell.subaspect
class MethodSmell:
    """
    This aspect detects `code smells` or `bad smells` related to methods'
    and functions definitions in your codebase.

    Method-level code smells are simply code smells indicating poorly defined
    method and or functions (too long method or functions, or functions with
    too many parameters) in your source code.
    """
    class docs:
        example = """
        # This function has way too many parameters

        def func(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, z):
            pass
        """
        example_language = 'python'
        importance_reason = """
        Make your functions and methods unambiguous(by reducing the number of
        parameters, easy to read(by reducing the length of your methods and
        functions) and debug.
        """
        fix_suggestions = """
        A fix for this would simply consist of redefining the functions
        (and or method), making them shorter and reducing the number of
        parameters (maybe by creating more functions or using libraries).
        """

    max_method_length = Taste[int](
        'Represents the max number of lines for a method or a function\'s'
        'definition.',
        (40,), default=40)
    max_paramters = Taste[int](
        'Represents the max number of parameters for a function\'s.',
        (5, 10), default=10)


@ClassSmell.subaspect
class DataClump:
    """
    This aspect detects `data clumps` in you codebase.

    `Data clump` is a name given to any group of variables which are passed
    around together (in a clump) throughout various parts of the program.
    """
    class docs:
        example = """
        public static void main(String args[]) {

            String firstName = args[0];
            String lastName = args[1];
            Integer age = new Integer(args[2]);
            String gender = args[3];
            String occupation = args[4];
            String city = args[5];

            welcomeNew(firstName,lastName,age,gender,occupation,city);
        }

        public static void welcomeNew(String firstName, String lastName,
                              Integer age, String gender,
                              String occupation, String city){

            System.out.printf("Welcome %s %s, a %d-year-old %s "\
                      "from %s who works as a%s\n",firstName, lastName,
                       age, gender, city, occupation);
        }
        """
        example_language = 'java'
        importance_reason = """
        Data clumps make codes difficult to read, debug, scale, and also
        hardly reusable.
        """
        fix_suggestions = """
        Formally group the different variables together into a single object.
        """


@ClassSmell.subaspect
class ClassLength:
    """
    This aspect checks on classes' definitions length in your codebase.
    """
    class docs:
        example = """
        // This is large class given that the `max_class_length` is 20

        public class Employee
        {
            private float salary;
            private float bonusPercentage;
            private EmployeeType employeeType;
            public Employee(float salary, float bonusPercentage,
                            EmployeeType employeeType)
            {
                this.salary = salary;
                this.bonusPercentage = bonusPercentage;
                this.employeeType = employeeType;
            }
            public float CalculateSalary()
            {
                switch (employeeType)
                {
                    case EmployeeType.Worker:
                        return salary;
                    case EmployeeType.Supervisor:
                        return salary + (bonusPercentage * 0.5F);
                    case EmployeeType.Manager:
                        return salary + (bonusPercentage * 0.7F);
                }
                return 0.0F;
            }
        }
        """
        example_language = 'Java'
        importance_reason = """
        Too large classes also known as God objects, result in ambiguous and
        difficult to debug source code; whereas too small classes (or lazy
        classes or freeloader) are sometimes useless.
        """
        fix_suggestions = """
        Usually splitting up those classes into many other classes solves the
        problem.
        """
    max_class_length = Taste[int](
        'Represents the max number of lines for a class\'s definition.',
        (999,), default=999)

    # This shall probably be removed.
    min_class_length = Taste[int](
        'Represents the min number of lines for a class\'s definition.',
        (1,), default=1)


@ClassSmell.subaspect
class FeatureEnvy:
    """
    This aspect detects occurrences of feature envy in your codebase.

    `Feature envy` describes classes that excessively use methods of other
    classes.
    """
    class docs:
        example = """
        public class Phone {
            private final String unformattedNumber;
            public Phone(String unformattedNumber) {
                this.unformattedNumber = unformattedNumber;
            }
            public String getAreaCode() {
                return unformattedNumber.substring(0,3);
            }
            public String getPrefix() {
                return unformattedNumber.substring(3,6);
            }
            public String getNumber() {
                return unformattedNumber.substring(6,10);
            }
        }
        public class Customer…
            private Phone mobilePhone;
            public String getMobilePhoneNumber() {
                return "(" +
                    mobilePhone.getAreaCode() + ") " +
                    mobilePhone.getPrefix() + "-" +
                    mobilePhone.getNumber();
            }
        }
        """
        example_language = 'java'
        importance_reason = """
        This smell may occur after fields are moved to a data class; which
        makes the code less readable, and difficult to debug.
        """
        fix_suggestions = """
        Move the operations on data to the newly defined class(given that
        the fields of one class were moved to this class) as well.
        """


@Smell.subaspect
class Naming:
    """
    This aspect checks on identifiers in your codebase (their length
    and the appropriate naming convention to use for them, be it variables,
    classes or functions)
    """
    class docs:
        example = """
        camelCase naming convention, snake_case naming convention,
        hyphenated-case naming convention etc...
        """
        example_language = 'English'
        importance_reason = """
        Consistent use of naming convention, make the code easy to read
        and debug.
        """
        fix_suggestions = """
        Use the appropriate naming convention for each data type.
        """

    variable_naming_convention = Taste[str](
        'Naming convention to use for variables\'s identifiers',
        ('lowerCamelCase', 'snake_case', 'hyphenated-case', 'UpperCamelCase'),
        default='snake_case')
    function_naming_convention = Taste[str](
        'Naming convention to use for functions\'s or methods\'s identifiers',
        ('lowerCamelCase', 'snake_case', 'hyphenated-case', 'UpperCamelcase'),
        default='snake_case')
    class_naming_convention = Taste[str](
        'Naming convention to use for classes\'s identifiers',
        ('lowerCamelCase', 'snake_case', 'hyphenated-case', 'UpperCamelCase'),
        default='UpperCamelCase')
    max_identifier_length = Taste[int](
        'The maximum number of character for an identifier.',
        (31,), default=31)


@Smell.subaspect
class Complexity:
    """
    This aspect checks on the cyclomatic complexity of your code
    """
    class docs:
        example = """
        for (i=0; i<n; ++i){
            for (i=0; i<n; ++i){
                for (i=0; i<n; ++i){
                    for (i=0; i<n; ++i){
                        for (i=0; i<n; ++i){
                            for (i=0; i<n; ++i){
                                for (i=0; i<n; ++i){
                                    for (i=0; i<n; ++i){
                                        ...
                                        //do something
        ...
        }
        """
        example_language = 'C++'
        importance_reason = """
        Very complex code are difficult to read, debug and maintain.
        It is always a good idea to keep things as simple as possible.
        """
        fix_suggestions = """
        This can be solved by breaking down complex functions into smaller
        onces.
        """
    cyclomatic_complexity = Taste[int](
        'This the maximum number of embedded branches or embedded loops'
        ' allowed.',
        (6,), default=6)
