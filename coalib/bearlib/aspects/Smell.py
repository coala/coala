from coalib.bearlib.aspects import Taste, Root


@Root.subaspect
class Smell:
    """
    Symptom in a piece of code that possibly indicates a deeper problem.

    `Smells` are certain structures in a code that indicate violation of
    fundamental design principles. They are usually not bugs; they are not
    technically incorrect and do not currently prevent the program from
    functioning.
    """
    class docs:
        example = """
        =begin
        Example of Ruby code with data clumps and methods with too many
        parameters.
        =end
        class Dummy
            def x(y1, y2, y3, y4, y5, y6, y7, y8, a); end
            def y(y1, y2, y3, y4, y5, y6, y7, y8); end
            def z(y1, y2, y3, y4, y5, y6, y7, y8); end
        end
        """
        example_language = 'Ruby'
        importance_reason = """
        Even though they are not necessarily bugs, code smells increase the
        risk of bugs or failure in the future and may slow down development.
        """
        fix_suggestions = """
        There are several `refactoring techniques` that can be used to deal
        with `code smells` including:

        * Composing methods
        * Moving features between objects
        * Organizing data
        * Simplifying conditional expressions
        * Simplifying method calls
        * Dealing with generalisation

        See <https://sourcemaking.com/refactoring/refactorings> for more
        information.
        """


@Smell.subaspect
class ClassSmell:
    """
    Code smells related to classes' definition.

    Class-level code smells indicate poorly defined classes (including too
    large classes or God object, data clump feature envy etc...) in your
    source code.
    """
    class docs:
        example = """
        class Warehouse
            def sale_price(item)
                item.price - item.rebate
            end
        end

        # sale_price refers to item more than self.
        """
        example_language = 'Ruby'
        importance_reason = """
        These classes should be refactored for better readability and
        maintainability of your source code.
        """
        fix_suggestions = """
        When a class is wearing too many (functional) hats (too large
        classes), you should probably think about splitting it up:

        * Extract class
        * Extract subclass
        * Extract interface
        """


@Smell.subaspect
class MethodSmell:
    """
    Code smells related to a method or function definition.

    Method-level code smells indicate poorly defined method and or
    functions (too long method or functions, or functions with too many
    parameters) in your source code.
    """
    class docs:
        example = """
        def do_nothing(var1, var2, var3, var4, var5, var6, var7):
            pass
        """
        example_language = 'Python'
        importance_reason = """
        Make your functions and methods unambiguous, easy to read and debug
        by reducing the number of parameters and length of your methods and
        functions.
        """
        fix_suggestions = """
        A fix for this would simply consist of redefining the functions
        (and or method), making them shorter and reducing the number of
        parameters (maybe by creating more functions or using libraries).
        """


@MethodSmell.subaspect
class MethodLength:
    """
    Number of lines of code in a function or method definition.

    Depending on the value of `method_length_count_comment`,
    comments are considered. The `rule of 30
    <https://dzone.com/articles/rule-30-%E2%80%93-when-method-class-or>`_
    suggests that the maximum number of lines for a method is 30. ``PMD``
    defines a default value of 100 lines per method, `checkstlye`` 150 and
    60 (when comments are not considered), ``rubocop`` 10.
    """
    class docs:
        example = """
        def _is_positive(num):
            if num > 0:
                return True
            else:
                return False

        # This function can be defined as follow:

        def is_positive(num):
            return num > 0
        """
        example_language = 'Python'
        importance_reason = """
        It is really important is to stay DRY ("Don't Repeat Yourself") and
        respect separation of concerns. Long methods are sometimes faster and
        easier to write, and don't lead to maintenance problems. But most of
        the time they are an easy way to detect that something *may* be wrong
        in the code, and that special care is required while maintaining it.
        """
        fix_suggestions = """
        Refactoring methods into smaller more generic methods, making code more
        compact by using inline and language specific syntax tricks,
        implementing methods or functions to avoid redundant operation(s),
        making use of methods provided in libraries rather than reimplementing
        them.
        """
    max_method_length = Taste[int](
        'Represents the max number of lines for a method or a function\'s'
        'definition.',
        (10, 30, 50, 60, 100), default=30)
    method_length_count_comment = Taste[bool](
        'Allows when set to `True` to considered comments while calculating'
        'methods\' length.',
        (30, 60, 100, 150), default=60)


@MethodSmell.subaspect
class ParameterListLength:
    """
    Number of parameter a function or method has.

    In the book "Code Complete", ISBN 0735619670 it is suggested that the
    maximum number of parameter per function or method is 7; ``rubocop``
    suggests 5.
    """
    class docs:
        example = """
        def func(a, b, c, d, e, f, g, h, i, j, k):
            pass
        """
        example_language = 'Python'
        importance_reason = """
        Methods that take too many parameters are difficult to read, maintain
        and work with, and callers of those method often have an awkward time
        assembling all of the data and the resulting code is usually not pretty.
        """
        fix_suggestions = """
        This can be fixed by:

        Instead of passing a group of data received from an object as
        parameters, pass the object itself to the method.
        Sometimes you can merge several parameters into a single object etc.
        """
    max_parameters = Taste[int](
        'Represents the max number of parameters for a function or a method.',
        (5, 7), default=7)


@ClassSmell.subaspect
class DataClump:
    """
    Identical groups of variables found in many different part of a program.
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

            System.out.printf(
                "Welcome %s %s, a %d-year-old %s from %s who works as a %s",
                firstName, lastName, age, gender, city, occupation
            );
        }
        """
        example_language = 'Java'
        importance_reason = """
        Data clumps make code difficult to read, understand, and reuse.
        It also spoils their architecture.
        """
        fix_suggestions = """
        Formally group the different variables together into a single object.
        """


@ClassSmell.subaspect
class ClassSize:
    """
    Class size refers to the size of a class.

    A class's size is based on:

        * the number of fields it contains,
        * the number of methods,
        * and the number of lines of code.
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
        Refactoring large classes spares developers from the need to remember
        a large number of attributes and methods. Splitting these classes
        avoids duplication, and makes the code shorter and easier to maintain.
        Sometimes a Lazy Class (a class that does too little) is created in
        order to delineate intentions for future development, In this case,
        try to maintain a balance between clarity and simplicity in your code;
        and they should be deleted if they serve no purpose.
        """
        fix_suggestions = """
        Usually splitting up large classes into other classes or giving in
        line Class treatment to component that are near useless can solve this
        problem.
        """


@ClassSize.subaspect
class ClassLength:
    """
    Number of lines of code in class' definition.
    """
    class docs:
        example = """
        # Here is an example of a large class (in terms of number of lines) if
        # we assume that the maximum number of lines per class defintion is 10

        class Student:
            def __init__(self, first_name, last_name, dob,
                         matricule, school, faculty, department,
                         level, courses):
                self.first_name = first_name
                self.last_name = last_name
                self.dob = dob
                self.matricule = matricule
                self.school = school
                self.faculty = faculty
                self.department = department
                self.level = level
                self.courses = courses
        """
        example_language = 'Python 3'
        importance_reason = """
        Too large classes are difficult to read and maintain, and can easily
        introduce bugs or duplication in our code base.
        """
        fix_suggestions = """
        Usually splitting up those classes into other classes solves the
        problem.
        """
    max_class_length = Taste[int](
        'Represents the max number of lines for a class\'s definition.',
        (999, 900), default=900)


@ClassSize.subaspect
class ClassConstants:
    """
    Number of constants in a class.
    """
    class docs:
        example = """
        // Here is an example of class with too many constants if we assume
        // that the maximum number of constants per class is 4

        class Aclass {
            final public int a = 1;
            final public int b = 2;
            final public String c = "coala";
            final public String d = "aspectsYEAH";
            final public Boolean e = true;

            public Aclass(){}
        }
        """
        example_language = 'Java'
        importance_reason = """
        Avoids having too many constants to spare developers from the neeed
        to remember too many of them.
        """
        fix_suggestions = """
        `ClassConstants` issues can be fixed by using data classes.
        """
    max_constants = Taste[int](
        'Represents the max number of constants for a class',
        (3,), default=3)


@ClassSize.subaspect
class ClassInstanceVariables:
    """
    Number of instance variables in a class.
    """
    class docs:
        example = """
        # Here is an example of a class with a large number of instance
        # variables if we assume that the maximun nubmer of instance variables
        # per class is 5.

        class Student:
            def __init__(self, first_name, last_name, dob,
                         matricule, school, faculty, department,
                         level, courses):
                self.first_name = first_name
                self.last_name = last_name
                self.dob = dob
                self.matricule = matricule
                self.school = school
                self.faculty = faculty
                self.department = department
                self.level = level
                self.courses = courses
        """
        example_language = 'Python 3'
        importance_reason = """
        Refactoring these classes spares developers from the need to remember
        a large number of attributes.
        """
        fix_suggestions = """
        Usually splitting up those classes into other classes solves the
        problem.
        """
    max_instance_variables = Taste[int](
        'Represents the max number of instance variables for a class',
        (3,), default=3)


@ClassSize.subaspect
class ClassMethods:
    """
    Number of class methods a class has.
    """
    class docs:
        example = """
        # Here is an example of a class with too many methods
        # Assuming that the maximum per class is 5.

        class AClass:
            def x(self): pass
            def y(self): pass
            def z(self): pass
            def p(self): pass
            def q(self): pass
            def r(self): pass
        """
        example_language = 'Python 3'
        importance_reason = """
        Refactoring these classes spares developers from the need to remember
        a large number of methods.
        """
        fix_suggestions = """
        Usually splitting up those classes into other classes solves the
        problem.
        """
    max_methods = Taste[int](
        'Represents the max number of methods for a class',
        (3,), default=3)


@ClassSmell.subaspect
class FeatureEnvy:
    """
    Classes that excessively use methods of other classes.
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
        example_language = 'Java'
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
    `Naming` refers to the naming conventions to use for identifiers.
    """
    class docs:
        example = """
        dummyVar = None  # lowerCamelCase naming convention
        DummyVar = None  # UpperCamelCase naming convention
        dummy_var = None  # snake_case naming convention
        """
        example_language = 'Python 3'
        importance_reason = """
        Consistent use of naming convention, make the code easy to read
        and debug.
        """
        fix_suggestions = """
        Use the appropriate naming convention for each data type.
        """

    variable_naming_convention = Taste[str](
        'Naming convention to use for variables\'s identifiers',
        ('lowerCamelCase', 'snake_case', 'kebab-case', 'UpperCamelCase'),
        default='snake_case')
    function_naming_convention = Taste[str](
        'Naming convention to use for functions\'s or methods\'s identifiers',
        ('lowerCamelCase', 'snake_case', 'kebab-case', 'UpperCamelcase'),
        default='snake_case')
    class_naming_convention = Taste[str](
        'Naming convention to use for classes\'s identifiers',
        ('lowerCamelCase', 'snake_case', 'kebab-case', 'UpperCamelCase'),
        default='UpperCamelCase')
    max_identifier_length = Taste[int](
        'The maximum number of character for an identifier.',
        (31,), default=31)


@Smell.subaspect
class Complexity:
    """
    Complexity of a code based on different complexity metrics.
    """
    class docs:
        example = """
        * McCabe's complexity
        * Halstead complexity
        * Elshof complexity
        * Data complexity
        etc...

        Here is an example of complex code:
        https://github.com/sympy/sympy/blob/master/sympy/solvers/solvers.py
        """
        example_language = 'reStructuredText'
        importance_reason = """
        Complex programs are difficult to read and maintain. Reducing a code's
        complexity improves its organization.
        """
        fix_suggestions = """
        Implementing simple methods, avoiding too many branches, avoiding too
        much multilevel inheritance etc... can fix this.
        """


@Complexity.subaspect
class CylomaticComplexity:
    """
    Number of linearly independent paths through a program's source code.

    The `Cyclomatic complexity
    <https://wikipedia.org/wiki/Cyclomatic_complexity>`_  was developed by
    Thomas J. McCabe in 1976 and it is based on a control flow representation
    of the program.
    """
    class docs:
        example = """
        // The cyclomatic complexity of this program is 4.

        int foo (int a, int b) {
            if (a > 17 && b < 42 && a+b < 55) {
                return 1;
            }
            return 2;
        }
        """
        example_language = 'C'
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


@Complexity.subaspect
class MaintainabilityIndex:
    """
    Software metric which measure how maintainable is a program.

    The `maintainablity index
    <www.projectcodemeter.com/cost_estimation/help/GL_maintainability.htm>`_
    is always in the range 0-100 and is ranked
    as follow:

    * A `MI` in the range 0-9 maps to a code extremely difficult to maintain.
    * A `MI` in the range 10-19 maps to a maintainable code.
    * A `MI` in the range 20-100 maps to a code highly maintainable.
    """
    class docs:
        example = """
        '''
        The maintainability index for the following piece of code is 100.
        '''
        def preorder(node):
            if tree:
                print(node.key)
                preorder(node.left)
                preorder(node.right)
        """
        example_language = 'Python'
        importance_reason = """
        Complex codes are difficult to maintain.
        """
        fix_suggestions = """
        This can be solved by writing simpler functions and methods.
        """
    maintainability_index = Taste[int](
        'Maintainability index of your code',
        tuple(range(100)), default=10)
