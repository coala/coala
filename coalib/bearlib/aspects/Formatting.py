from coalib.bearlib.aspects import Root, Taste


@Root.subaspect
class Formatting:
    """
    The visual appearance of source code.
    """
    class docs:
        example = """
        # Here is an example of Python code with lots of
        # formatting issues including: trailing spaces, missing spaces
        # around operators, strange and inconsistent indentation etc.

        z = 'hello'+'world'
             def f ( a):
                pass
        """
        example_language = 'Python'
        importance_reason = """
        A coding style (the of rules or guidelines used when writing the
        source code) can drastically affect the readability, and
        maintainability of a program and might as well introduce bugs.
        """
        fix_suggestions = """
        Defining a clearly and thoughtful coding style (based on the available
        ones given the programming language in use) and strictly respect it or
        apply it through out the implementation of a project.
        """


@Formatting.subaspect
class Length:
    """
    Hold sub-aspects for file and line length.
    """
    class docs:
        example = """
        # We assume that the maximum number of characters per line is 10
        # and that the maximum number of lines per files is 3.

        def run(bear, file, filename, aspectlist):
            return bear.run(file, filename, aspectlist)
        """
        example_language = 'Python'
        importance_reason = """
        Too long lines of code and too large files result in code difficult to
        read, understand and maintain.
        """
        fix_suggestions = """
        Length issues can be fixed by writing shorter lines of code (splitting
        long lines into multiple shorter lines); writing shorter files
        (splitting files into modules, writing shorter methods and classes.).
        """


@Length.subaspect
class LineLength:
    """
    Number of characters found in a line of code.
    """
    class docs:
        example = """
        print('The length of this line is 38')
        """
        example_language = 'Python'
        importance_reason = """
        Too long lines make code very difficult to read and maintain.
        """
        fix_suggestions = """
        Splitting long lines of code into multiple shorter lines whenever
        possible. Avoiding the usage of in-line language specific constructs
        whenever they result in too long lines.
        """
    max_line_length = Taste[int](
        'Maximum number of character for a line.',
        (79, 80, 100, 120, 160), default=80)


@Length.subaspect
class FileLength:
    """
    Number of lines found in a file.
    """
    class docs:
        example = """
        # This file would be a large file if we assume that the max number of
        # lines per file is 10

        class Node:
            def __init__(self, value, left_most_child, left_sibling):
                self.value=value
                self.left_most_child=left_most_child
                self.left_sibling=left_sibling

        # This is example is just showing what this aspect is about, because
        # the max number of lines per file is usually 999.
        """
        example_language = 'Python 3'
        importance_reason = """
        Too long programs (or files) are difficult to read, maintain and
        understand.
        """
        fix_suggestions = """
        Splitting files into modules, writing shorter methods and classes.
        """
    max_file_length = Taste[int](
        'Maximum number of line for a file',
        (999,), default=999)


@Formatting.subaspect
class Spacing:
    """
    All whitespace found between non-whitespace characters.
    """
    class docs:
        example = """
        # Here is an example of code with spacing issues including
        # unnecessary blank lines and missing space around operators.



        def func(   ):
           return      37*-+2
        """
        example_language = 'Python'
        importance_reason = """
        Useless spacing affects the readability and maintainability of a code.
        """
        fix_suggestions = """
        Removing the trailing spaces and the meaningless blank lines.
        """


@Spacing.subaspect
class Indentation:
    """
    Spaces/tabs used before blocks of code to convey a program's structure.
    """
    class docs:
        example = """
        # If this code was written on an editor that defined a tab as 2
        # spaces, mixing tabs and spaces would look like this on a different
        # editor defining tabs as four spaces.

        def spaces():
          pass

        def tabs():
            pass
        """
        example_language = 'Python'
        importance_reason = """
        Mixing tabs and spaces can cause issues when collaborating on
        code, as well as during testing and compilation.
        """
        fix_suggestions = """
        Using either tabs or spaces consistently.
        If using spaces, by using a suitable number of spaces, preferably four.
        """
    indent_type = Taste[str](
        'Represents the type of indent used.',
        ('tab', 'space'), default='tab')
    indent_size = Taste[int](
        'Represents the number of spaces per indentation level.',
        (2, 3, 4, 5, 6), default=4)


@Spacing.subaspect
class TrailingSpace:
    """
    Unnecessary whitespace at end of a line.

    Trailing space is all whitespace found after the last non-whitespace
    character on the line until the newline. This includes tabs "\\\\t",
    blank lines, blanks etc.
    """
    class docs:
        example = """
        def func( a ):
              pass

        """.replace('\n', '\t\n')
        example_language = 'Python'
        importance_reason = """
        Trailing spaces make code less readable and maintainable.
        """
        fix_suggestions = """
        Removing the trailing spaces.
        """
    allow_trailing_spaces = Taste[bool](
        'Determines whether or not trailing spaces should be allowed or not.',
        (True, False), default=False)


@Spacing.subaspect
class BlankLine:
    """
    A line with zero characters.
    """
    class docs:
        example = """
        name = input('What is your name?')


        print('Hi, {}'.format(name))
        """
        example_language = 'Python 3'
        importance_reason = """
        Various programming styles use blank lines in different places.
        The usage of blank lines affects the readability, maintainability and
        length of a code i.e blank lines can either make code longer, less
        readable and maintainable or do the reverse.
        """
        fix_suggestions = """
        Following specific rules about the usage of blank lines: using them
        only when necessary.
        """


@BlankLine.subaspect
class BlankLineAfterDeclaration:
    """
    Those found after declarations.
    """
    class docs:
        example = """
        #include <stdio.h>

        int main ()
        {
          int a;
          float b;

          scanf("%d%f", &a, &b);
          printf("a = %d and b = %f", a, b);
          return 0;
        }
        """
        example_language = 'C'
        importance_reason = """
        Having a specific and reasonable number of blank lines after every
        block of declarations improves on the readability of the code.
        """
        fix_suggestions = """
        `BlankLintAfterDeclaration` issues can be fixed specifying (and of
        course using) a reasonable number of blank lines to use after block
        declaration.
        """
    blank_lines_after_declarations = Taste[int](
        'Represents the number of blank lines after declarations',
        (0, 1, 2), default=0)


@BlankLine.subaspect
class BlankLineAfterProcedure:
    """
    Those found after procedures or functions.
    """
    class docs:
        example = """
        #include <stdio.h>

        void proc(void){
            printf("this does nothing");
        } int add(float a, float b){
            return a + b;
        }
        """
        example_language = 'C'
        importance_reason = """
        Having a specific and reasonable number of blank lines after every
        procedures improves on the readability of the code.
        """
        fix_suggestions = """
        `BlankLintAfterProcedure` issues can be fixed specifying (and of
        course using) a reasonable number of blank lines to use after
        procedures' definition.
        """
    blank_lines_after_procedures = Taste[int](
        'Represents the number of blank lines to use after a procedure or'
        'a function', (0, 1, 2), default=1)


@BlankLine.subaspect
class BlankLineAfterClass:
    """
    Those found after classes' definitions.
    """
    class docs:
        example = """
        class SomeClass:
            def __init__(self):
                raise RuntimeError('Never instantiate this class')


        def func():
            pass
        """
        example_language = 'Python 3'
        importance_reason = """
        Having a specific number of blank lines after every classes'
        definitions declarations improves on the readability of the code.
        """
        fix_suggestions = """
        """
    blank_lines_after_class = Taste[int](
        'Represents the number of blank lines to use after a class'
        'definition.', (1, 2), default=2)


@BlankLine.subaspect
class NewlineAtEOF:
    """
    Newline character (usually '\\\\n', aka CR) found at the end of file.
    """
    class docs:
        example = """
        def do_nothing():
            pass
        """ + ('\n')
        example_language = 'Python'
        importance_reason = """
        A text file consists of a series of lines, each of which ends with a
        newline character (\\\\n). A file that is not empty and does not end
        with a newline is therefore not a text file.

        It's not just bad style, it can lead to unexpected behavior, utilities
        that are supposed to operate on text files may not cope well with files
        that don't end with a newline.
        """
        fix_suggestions = """
        `NewlineAtEOF` issues can be fixed by simply adding a newline at the
        end of the file.
        """
    newline_at_EOF = Taste[bool](
        'If ``True``, enforce a newline at End Of File.',
        (True, False), default=True)


@Spacing.subaspect
class SpacesAroundOperator:
    """
    Spacing around operators.
    """
    class docs:
        example = """
        def f(a, x):
            return 37+a[42 -  x]
        """
        example_language = 'Python'
        importance_reason = """
        Having a specific and reasonable number of whitespace (blank) around
        operators improves on the readability of the code.
        """
        fix_suggestions = """
        `SpacesAroundOperator` issues can be fixed by simply specifying and
        the number of whitespace to be used after each operator.
        """
    spaces_around_operators = Taste[int](
        'Represents the number of space to be used around operators.',
        (0, 1), default=1)
    spaces_before_colon = Taste[int](
        'Represents the number of blank spaces before colons.',
        (0, 1), default=0)
    spaces_after_colon = Taste[int](
        'Represents the number of blank spaces after colons.',
        (0, 1), default=1)


@Formatting.subaspect
class Quotation:
    """
    Quotation mark used for strings and docstrings.
    """
    class docs:
        example = """
        # Here is an example of code where both '' and "" quotation mark
        # Are used.

        string = 'coala is always written with lowercase c.'
        string = "coala is always written with lowercase c."
        string = "'coala' is always written with lowercase 'c'."
        """
        example_language = 'Python'
        importance_reason = """
        Using the same quotation whenever possible in the code, improve on its
        readability by introducing consistency.
        """
        fix_suggestions = """
        Choosing a preferred quotation and using it everywhere (if possible).
        """
    preferred_quotation = Taste[str](
        'Represents the preferred quotation marks.'
        'It ensures that every string contains the selected style of quotes, '
        'except where there is a delimiter collision.',
        ('\'', '"'), default='\'')
