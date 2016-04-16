Bears That Can Suggest And Make Corrections
-------------------------------------------

**Note**: Go through the `Linter Bears
<http://coala.readthedocs.org/en/latest/Users/Tutorials/Linter_Bears.html>`_
before reading this.

Some executables (like ``indent`` or ``autopep8``) can generate a corrected
file from the original. We can use such executables so that *coala*, using
these bears, can suggest and also make automatic corrections. Here's an
example bear. (GNUIndentBear)

::

    import platform

    from coalib.bearlib.abstractions.Lint import Lint
    from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
    from coalib.bears.LocalBear import LocalBear


    class GNUIndentBear(Lint, LocalBear):
        executable = "indent" if platform.system() != "Darwin" else "gindent"
        diff_message = "Indentation can be improved."
        use_stdin = True
        gives_corrected = True

        def run(self,
                filename,
                file,
                max_line_length: int=80,
                use_spaces: bool=True,
                tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
                indent_cli_options: str=''):
            """
            This bear checks and corrects spacing and indentation via the well
            known Indent utility. It is designed to work with the C programming
            language but may work reasonably with syntactically similar
            languages.

            :param max_line_length:    Maximum number of characters for a line.
            :param use_spaces:         True if spaces are to be used, else
                                       tabs.
            :param tab_width:          Number of spaces per indent level.
            :param indent_cli_options: Any command line options the indent
                                       binary understands. They will be simply
                                       passed through.
            """
            self.arguments = "--no-tabs" if use_spaces else "--use-tabs"
            self.arguments += (" --line-length {0} --indent-level {1} "
                               "--tab-size {1} {2}".format(max_line_length,
                                                           tab_width,
                                                           indent_cli_options))
            return self.lint(filename, file)


In the example above, the important line is:

::

    gives_corrected = True

This tells the ``Lint`` class that this bear can suggest corrections. When we
do this, internally a ``diff`` of the original file and the generated
'corrected file' along with some other not-important-for-this-tutorial magic
is used to get the final output (which may be suggestions or
auto-corrections).

Let's try this bear out. Create a new file called ``sample.cpp``. Contents of
``sample.cpp`` are:

::

    #include <iostream>
    int main(){
    if(1 == 1)
    if(2 == 2)
    if(3 != 4)
    cout << "Pun Indented." << endl;

    return 0;
    }

And, run the following command:

::

    coala --bear-dirs=. --bears=GNUIndentBear --files=sample.cpp -s

Make sure that both ``GNUIndentBear.py`` and ``sample.cpp`` are in your current
folder. Also make sure that ``indent`` is installed (**not** the pip package,
but the gnu one which can be installed using your system package manager).

Now, we have a bear that is much more helpful than just a simple Linter Bear!
