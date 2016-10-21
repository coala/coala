from coalib.bearlib.aspects import (
    Aspect, AspectDocumentation, AspectSetting, Root)


Root.new_subaspect(
    'Redundancy',
    AspectDocumentation(
        definition="""
        This aspect describes redundancy in your source code.
        """,
        importance_reason="""
        Redundant code makes your code harder to read and understand.
        """,
        fix_suggestions="""
        Redundant code can usually be removed without consequences.
        """
    )
)

Root.Redundancy.new_subaspect(
    'Clone',
    AspectDocumentation(
        definition="""
        Code clones are multiple pieces of source code in your
        codebase that are very similar.
        """,
        example="""
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
        """,
        example_language='C++',
        importance_reason="""
        Code clones make editing more difficult due to unnecessary increases
        in complexity and length.
        """,
        fix_suggestions="""
        Usually code clones can be simplified to only one occurrence. In a
        lot of cases, both just use different values or variables and can
        be reduced to one function called with different parameters or
        loops.
        """
    ),
    settings=(AspectSetting(
        'min_clone_token',
        "The number of tokens that have to be equal for it to"
        " be detected as a code clone.",
        int,
        (20,),
        20
    ),)
)

Root.Redundancy.new_subaspect(
    'UnusedImport',
    AspectDocumentation(
        definition="""
        Unused imports are any kind of import/include that is not needed.
        """,
        example="""
        import sys
        import os

        print('coala is always written with lowercase c')
        """,
        example_language="python",
        importance_reason="""
        Redundant imports can cause a performance degrade and make code
        harder to understand when reading through it. Also it causes
        unneeded dependencies within your modules. In most programming
        languages, unused imports may have side effects and that may
        be a common false positive. However those should be avoided.
        """,
        fix_suggestions="""
        Usually, unused imports can simply be removed.
        """
    )
)


Root.Redundancy.new_subaspect(
    'UnreachableCode',
    AspectDocumentation(
        definition="""
        Unreachable code, sometimes called dead code, is source code that
        can never be executed during the program execution.
        """,
        example="""
        def func():
            return True

        if func():
            a = {}
        else:
            a = (i for i in range (5))
            print (id(a))
        """,
        example_language='python',
        importance_reason="""
        Unreachable code, makes the source code longer and more difficult
        to maintain.
        """,
        fix_suggestions="""
        Those pieces of code can easily be removed without consequences.
        """
    )
)

Root.Redundancy.UnreachableCode.new_subaspect(
    'UnusedFunction',
    AspectDocumentation(
        definition="""
        An unused function is a function that is never called during
        code execution.
        """,
        example="""
        def func():
            pass

        print('coala is always written with lowercase c')
        """,
        example_language='python',
        importance_reason="""
        Unused functions make the source code more longer and more
        difficult to maintain.
        """,
        fix_suggestions="""
        It is recommended to remove those functions. If you would like
        to access it's source code later for other purposes, you can
        rely on a version control system like Git, Mercurial or
        Subversion.
        """
    )
)

Root.Redundancy.UnreachableCode.new_subaspect(
    'UnreachableStatement',
    AspectDocumentation(
        definition="""
        An unreachable statement is a statement that is never executed
        during code execution.
        """,
        example="""
        def func():
            return True

        if func():
            a = {}
        else:
            a = (i for i in range (5))
            print (id(a))
        """,
        example_language="python",
        fix_suggestions="""
        These statement can be remove without harming the code.
        """
    )
)

Root.Redundancy.new_subaspect(
    'UnusedVariable',
    AspectDocumentation(
        definition="""
        Unused variables are declared but never used.
        """,
        example="""
        a = {}
        print ('coala')
        """,
        example_language='python',
        importance_reason="""
        Unused variables can degrade performance marginally but more importantly
        makes the source code harder to read and understand.
        """,
        fix_suggestions="""
        Those variables can easily be removed without consequences.
        """
    )
)

Root.Redundancy.UnusedVariable.new_subaspect(
    'UnusedParameter',
    AspectDocumentation(
        definition="""
        Unused parameters are functions arguments which are never used.
        """,
        example="""
        def func(a):
            pass
        """,
        example_language='python',
        importance_reason="""
        Unused paramaters are useless to functions, they them difficult to
        use and maintain.
        """,
        fix_suggestions="""
        Those parameters can easily be removed without consequences.
        """
    )
)


Root.Redundancy.UnusedVariable.new_subaspect(
    'UnusedLocalVariable',
    AspectDocumentation(
        definition="""
        These are variable which are defined locally but never used.
        """,
        example="""
        def func():
            for i in range (5):
                a = 0
                print ( ' coala ' )
        """,
        example_language='python',
        importance_reason="""
        They make the code difficult to maintain.
        """,
        fix_suggestions="""
        These can easily be removed without consequences.
        """
    )
)
Root.Redundancy.UnusedVariable.new_subaspect(
    'UnusedGlobalVariable',
    AspectDocumentation(
        definition="""
        These are variable which have a global scope but are never used.
        """,
        example="""
        a = 0
        for i in range (5):
            print ( ' coala ' )
        """,
        example_language='python',
        importance_reason="""
        They make the code difficult to maintain.
        """,
        fix_suggestions="""
        These can easily be removed without consequences.
        """
    )
)
