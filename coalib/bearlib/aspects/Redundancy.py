from coalib.bearlib.aspects import Aspect, AspectDocumentation


class Redundancy(Aspect):
    docs = AspectDocumentation(
        definition="This aspect describes redundancy in your source code.",
        cause="Redundancies are often caused by forgetting to remove "
              "something during refactorings.",
        example="if False:\n    do_something()",
        example_language="python",
        importance_reason="Redundant code makes your code harder to read and "
                          "understand.",
        fix_suggestions="Redundant code can usually be removed without "
                        "consequences."
    )

    class Clone(Aspect):
        docs = AspectDocumentation(
            definition="""
            Code clones are different pieces of source code in your
            codebase that are very similar.
            """,
            cause="""
            Clones usually result out of copy and pasting.
            """,
            example="""
            if input=="main":
                print("This is main.")
            elif input=="other":
                print("This is other.")
            """,
            example_language='python',
            importance_reason="""
            Code clones are a problem because they bloat up your code base and
            bugs usually occur in all the duplicated fragments.
            """,
            fix_suggestions="""
            Usually code clones can be simplified to only one occurrence. In a
            lot of cases, both just use different values or variables and can
            be reduced to one function called with different parameters or
            loops.
            """
        )

        MIN_CLONE_TOKEN = (
            "The number of tokens that have to be equal for it to be detected "
            "as a code clone.",
            int, 20)

    class UnusedImport(Aspect):
        """
        Unused imports are any kind of import/include that is not needed.

        Redundant imports can cause a performance degrade and make code harder
        to understand when reading through it. Also it causes unneeded
        dependencies within your modules.

        Usually, unused imports can simply be removed.
        """

    class UnreachableCode(Aspect):
        """
        Unreachable code, sometimes called dead code, is source code that can
        never be executed during the program execution.

        Those pieces of code can easily be removed without consequences, making
        your source code simpler and better maintainable.
        """

        class UnusedFunction(Aspect):
            """
            An unused function is a function that is never called during code
            execution.

            Unused functions can happen when some legacy function usages were
            replaced by other functionality and the old function is left
            behind.

            It is recommended to remove those functions. If you would like to
            access it's source code later for other purposes, you can rely on
            a version control system like Git, Mercurial or Subversion.
            """

        class UnreachableStatement(Aspect):
            """
            Anything that is effectively in an if False, TODO
            """

    class UnusedVariable(Aspect):
        """
        Unused variables are declared but never used.

        This can degrade performance marginally but more importantly makes the
        source code harder to read and understand.

        Unused variables can appear due
        """

        class UnusedParameter(Aspect):
            """
            Unused function param, TODO.
            """

        class UnusedLocalVariable(Aspect):
            """
            Unused local variable, TODO.
            """

        class UnusedGlobalVariable(Aspect):
            """
            Unused global variable, TODO.
            """
