from coalib.bearlib.languages import Language
from coalib.bearlib.aspects import Root, Taste


@Root.subaspect
class Redundancy:
    """
    This aspect describes redundancy in your source code.
    """
    class docs:
        importance_reason = """
        Redundant code makes your code harder to read and understand.
        """
        fix_suggestions = """
        Redundant code can usually be removed without consequences.
        """


@Redundancy.subaspect
class Clone:
    """
    Code clones are multiple pieces of source code in your
    codebase that are very similar.
    """
    class docs:
        example = """
        extern int array_a[];
        extern int array_b[];

        int sum_a = 0;

        for (int i = 0; i < 4; i++)
            sum_a += array_a[i];

        int average_a = sum_a / 4;

        int sum_b = 0;

        for (int i = 0; i < 4; i++)
            sum_b += array_b[i];

        int average_b = sum_b / 4;
        """
        example_language = 'C++'
        importance_reason = """
        Code clones make editing more difficult due to unnecessary increases
        in complexity and length.
        """
        fix_suggestions = """
        Usually code clones can be simplified to only one occurrence. In a
        lot of cases, both just use different values or variables and can
        be reduced to one function called with different parameters or
        loops.
        """

    min_clone_tokens = Taste[int](
        'The number of tokens that have to be equal for it to'
        ' be detected as a code clone.',
        (20, ), default=20)

    ignore_using = Taste[bool](
        'Ignore ``using`` directives in C#.',
        (True, False), default=False,
        languages=(Language.CSharp, ))


@Redundancy.subaspect
class UnusedImport:
    """
    Unused imports are any kind of import/include that is not needed.
    """
    class docs:
        example = """
        import sys
        import os

        print('coala is always written with lowercase c')
        """
        example_language = 'python'
        importance_reason = """
        Redundant imports can cause a performance degrade and make code
        harder to understand when reading through it. Also it causes
        unneeded dependencies within your modules. In most programming
        languages, unused imports may have side effects and that may
        be a common false positive. However those should be avoided.
        """
        fix_suggestions = """
        Usually, unused imports can simply be removed.
        """


@Redundancy.subaspect
class UnreachableCode:
    """
    Unreachable code, sometimes called dead code, is source code that
    can never be executed during the program execution.
    """
    class deco:
        example = """
        def func():
            return True

        if func():
            a = {}
        else:
            a = (i for i in range (5))
            print (id(a))
        """
        example_language = 'python'
        importance_reason = """
        Unreachable code, makes the source code longer and more difficult
        to maintain.
        """
        fix_suggestions = """
        Those pieces of code can easily be removed without consequences.
        """


@UnreachableCode.subaspect
class UnusedFunction:
    """
    An unused function is a function that is never called during
    code execution.
    """
    class docs:
        example = """
        def func():
            pass

        print('coala is always written with lowercase c')
        """
        example_language = 'python'
        importance_reason = """
        Unused functions make the source code more longer and more
        difficult to maintain.
        """
        fix_suggestions = """
        It is recommended to remove those functions. If you would like
        to access it's source code later for other purposes, you can
        rely on a version control system like Git, Mercurial or
        Subversion.
        """


@UnreachableCode.subaspect
class UnreachableStatement:
    """
    An unreachable statement is a statement that is never executed
    during code execution.
    """
    class docs:
        example = """
        def func():
            return True

        if func():
            a = {}
        else:
            a = (i for i in range (5))
            print (id(a))
        """
        example_language = 'python'
        fix_suggestions = """
        These statement can be remove without harming the code.
        """


@Redundancy.subaspect
class UnusedVariable:
    """
    Unused variables are declared but never used.
    """
    class docs:
        example = """
        a = {}
        print ('coala')
        """
        example_language = 'python'
        importance_reason = """
        Unused variables can degrade performance marginally but more importantly
        makes the source code harder to read and understand.
        """
        fix_suggestions = """
        Those variables can easily be removed without consequences.
        """


@UnusedVariable.subaspect
class UnusedParameter:
    """
    Unused parameters are functions arguments which are never used.
    """
    class docs:
        example = """
        def func(a):
            pass
        """
        example_language = 'python'
        importance_reason = """
        Unused paramaters are useless to functions, they them difficult to
        use and maintain.
        """
        fix_suggestions = """
        Those parameters can easily be removed without consequences.
        """


@UnusedVariable.subaspect
class UnusedLocalVariable:
    """
    These are variable which are defined locally but never used.
    """
    class docs:
        example = """
        def func():
            for i in range (5):
                a = 0
                print ( ' coala ' )
        """
        example_language = 'python'
        importance_reason = """
        They make the code difficult to maintain.
        """
        fix_suggestions = """
        These can easily be removed without consequences.
        """


@UnusedVariable.subaspect
class UnusedGlobalVariable:
    """
    These are variable which have a global scope but are never used.
    """
    class docs:
        example = """
        a = 0
        for i in range (5):
            print ( ' coala ' )
        """
        example_language = 'python'
        importance_reason = """
        They make the code difficult to maintain.
        """
        fix_suggestions = """
        These can easily be removed without consequences.
        """
