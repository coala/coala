Guide to Writing a Native Bear
==============================

Welcome. This document presents information on how to write a bear for
coala. It assumes you know how to use coala. If not, please read our
`main tutorial`_

The sample sources for this tutorial lie at our coala-tutorial
repository, go clone it with:

::

    git clone https://github.com/coala/coala-tutorial

All paths and commands given here are meant to be executed from the root
directory of the coala-tutorial repository.

.. note::

    If you want to wrap an already existing tool, please refer to
    :doc:`this tutorial instead<Writing_Linter_Bears>`.

What is a bear?
---------------

A bear is meant to do some analysis on source code. The source code will
be provided by coala so the bear doesn't have to care where it comes from
or where it goes.

There are two kinds of bears:

- LocalBears, which only perform analysis on each file itself
- GlobalBears, which are project wide, like the GitCommitBear

A bear can communicate with the user via two ways:

-  Via log messages
-  Via results

Log messages will be logged according to the users settings and are
usually used if something goes wrong. However you can use debug for
providing development related debug information since it will not be
shown to the user by default. If error/failure messages are used, the
bear is expected not to continue analysis.

A Hello World Bear
------------------

Below is the code given for a simple bear that sends a debug message for
each file:

.. code:: python

    import logging

    from coalib.bears.LocalBear import LocalBear

    class HelloWorldBear(LocalBear):
        def run(self,
                filename,
                file):
            logging.debug("Hello World! Checking file {}.".format(filename))

This bear is stored at ``./bears/HelloWorldBear.py``

In order to let coala execute this bear you need to let coala know where
to find it. We can do that with the ``-d`` (``--bear-dirs``) argument:

``coala -f src/*.c -d bears -b HelloWorldBear -L DEBUG --flush-cache``

.. note::

    The given bear directories must not have any glob expressions in them. Any
    character that could be interpreted as a part of a glob expression will be
    escaped. Please use comma separated values to give several such
    directories instead. Do not forget to flush the cache (by adding the
    argument ``--flush-cache`` when running coala) if you run a new bear on a
    file which has been previously analyzed (by coala).

You should now see an output like this on your command line:

::

    [WARNING][15:07:39] Default coafile '.coafile' not found!
    Here's what you can do:
    * add `--save` to generate a config file with your current options
    * add `-I` to suppress any use of config files
    [DEBUG][15:07:39] Platform Linux -- Python 3.5.2, coalib
    0.12.0.dev20170626132008
    [DEBUG][15:07:39] The file cache was successfully flushed.
    [DEBUG][15:07:39] Files that will be checked:
    /home/LordVoldemort/programs/coa_dir/coala-tutorial/src/main.c
    [DEBUG][15:07:40] coala is run only on changed files, bears' log
    messages from previous runs may not appear. You may use the
    `--flush-cache` flag to see them.
    [DEBUG][15:07:40] Running bear HelloWorldBear...
    [DEBUG][15:07:40] Hello World! Checking file /home/LordVoldemort/
    programs/coa_dir/coala-tutorial/src/main.c .

    Notice that the last ``[DEBUG]`` message is what was coded in
    ``HelloWorldBear.py``. All the other messages are inherited from the
    ``LocalBear`` class or run by the code responsible for executing the
    bear.

.. note::

    The first ``WARNING`` message is because our directory, does not
    contain a ``.coafile``. If you have followed the instructions in
    our `main tutorial`_, you will have a ``.coafile`` in your working
    directory. Its best if you delete that file before working on this
    tutorial, else you will see a bunch of other outputs from other bears
    as well.

For more detail about Python's built-in ``logging`` facility,
see https://docs.python.org/3/library/logging.html.

Communicating with the User
---------------------------

Now we can send messages through the queue, we can do the real work.
Let's say:

-  We want some information from the user (e.g. the tab width if we rely
   on indentation).
-  We've got some useful information for the user and want to show it to
   them. There might be some issue with their code or just an information
   like the number of lines.

So let's extend our HelloWorldBear a bit, I've named the new bear with
the creative name CommunicationBear:

.. code:: python

    import logging

    from coalib.bears.LocalBear import LocalBear

    class CommunicationBear(LocalBear):

        def run(self,
                filename,
                file,
                user_input: str):
            """
            Communicates with the user.

            :param user_input: Arbitrary user input.
            """
            logging.debug("Got '{ui}' as user input of type {type}.".format(
                ui=user_input,
                type=type(user_input)))

            yield self.new_result(message="A hello world result.",
                                  file=filename)

Try executing it:

::

    coala -f=src/\*.c -d=bears -b=CommunicationBear -L=DEBUG --flush-cache

Hey, we'll get asked for the user\_input!

::

    [WARNING][15:20:18] Default coafile '.coafile' not found!
    Here's what you can do:
    * add `--save` to generate a config file with your current options
    * add `-I` to suppress any use of config files
    Please enter a value for the setting "user_input" (No description given.)
    needed by CommunicationBear for section "cli":

Wasn't that easy? Go ahead,
enter something and observe the output.

::

    Avada Kedavra
    [DEBUG][15:22:55] Platform Linux -- Python 3.5.2, coalib
    0.12.0.dev20170626132008
    [DEBUG][15:22:55] The file cache was successfully flushed.
    [DEBUG][15:22:55] Files that will be checked:
    /home/LordVoldemort/programs/coa_dir/coala-tutorial/src/main.c
    [DEBUG][15:22:55] coala is run only on changed files, bears' log messages
    from previous runs may not appear. You may use the `--flush-cache` flag to
    see them.
    [DEBUG][15:22:55] Running bear CommunicationBear...
    [DEBUG][15:22:55] Got 'Avada Kedavra' as user input of type <class 'str'>.

    **** CommunicationBear [Section: cli] ****

    !    ! [Severity: NORMAL]
    !    ! A hello world result.
    [    ] Do (N)othing
    [    ] (O)pen file
    [    ] Add (I)gnore comment
    [    ] Enter number (Ctrl-D to exit):

So, what did coala do here?

First, coala looked at the parameters of the run method and found that
we need some value named user\_input. Then it parsed our documentation
comment and found a description for the parameter which was shown to us
to help us choose the right value. After the needed values are provided,
coala converts the value into a string because we've provided the
``str`` annotation for this parameter. If no annotation is given or the
value isn't convertible into the desired data type, you will get a
``coalib.settings.Setting.Setting``.

Your docstring can also be used to tell the user what exactly your bear
does.

Try executing

::

    coala -d bears -b CommunicationBear --show-bears --show-description

This will show the user a bunch of information related to the bear like:
- A description of what the bear does - The sections which uses it - The
settings it uses :
:: 
  
  AlexBear
  Checks the markdown file with Alex - Catch insensitive, inconsiderate
  writing.

  Be aware that Alex and this bear only work on English text.
  For more information, consult <https://www.npmjs.com/package/alex>.

  AnnotationBear
  Finds out all the positions of strings and comments in a file. The Bear searches for valid comments and strings and yields their        ranges as SourceRange objects in HiddenResults.

  BanditBear
  Performs security analysis on Python source code, utilizing the ``ast``module from the Python standard library.

  BootLintBear
  Raise several common HTML mistakes in html files that are using Bootstrap in a fairly "vanilla" way.
  Vanilla Bootstrap's components/widgets require their parts of the DOM to conform to certain structures that is
  checked. Also, raises issues about certain <meta> tags, HTML5 doctype declaration, etc. to use bootstrap properly.

  For more about the analysis, check Bootlint
  <https://github.com/twbs/bootlint#bootlint>.

  CheckstyleBear
  Check Java code for possible style, semantic and design issues.

  For more information, consult
  <http://checkstyle.sourceforge.net/checks.html>.

  ClangASTPrintBear
  This bear is meant for debugging purposes relating to clang. It just prints out the whole AST for a file to the DEBUG channel.

  ClangBear
  Check code for syntactical or semantical problems using Clang.This bear supports automatic fixes.

  ClangCloneDetectionBear
  Checks the given code for similar functions that are probably redundant.

  ClangComplexityBear
  Check for all functions if they are too complicated using the cyclomatic complexity metric.
  You can read more about this metric at <https://www.wikiwand.com/en/Cyclomatic_complexity>.

  ClangFunctionDifferenceBear
  Retrieves similarities for code clone detection. Those can be reused in another bear to produce results.
  Postprocessing may be done because small functions are less likely to be clones at the same difference value than big functions which   may provide a better refactoring opportunity for the user.

  CMakeLintBear
  Check CMake code for syntactical or formatting issues.

  For more information consult <https://github.com/richq/cmake-lint>.

  coalaBear
  Check for the correct spelling of ``coala`` in the file.

  CoffeeLintBear
  Check CoffeeScript code for a clean and consistent style.

  For more information about coffeelint, visit <http://www.coffeelint.org/>.

  CommunicationBear
  Communicates with the user.

  CPDBear
  Checks for similar code that looks as it could be replaced to reduce redundancy.
  For more details see: <https://pmd.github.io/pmd-5.4.1/usage/cpd-usage.html>

  CPPCheckBear
  Report possible security weaknesses for C/C++.
  For more information, consult <https://github.com/danmar/cppcheck>.

  CPPCleanBear
  Find problems in C++ source code that slow down development in large code bases. This includes finding unused code, among   
  other features.

  Read more about available routines at
  <https://github.com/myint/cppclean#features>.

  CPPLintBear
  Check C++ code for Google's C++ style guide.

  For more information, consult <https://github.com/theandrewdavis/cpplint>.

  CSecurityBear
  Report possible security weaknesses for C/C++.

  For more information, consult <http://www.dwheeler.com/flawfinder/>.

  CSharpLintBear
  Checks C# code for syntactical correctness using the ``mcs`` compiler.

  CSSAutoPrefixBear
  This bear adds vendor prefixes to CSS rules using ``autoprefixer`` utility.

  CSSLintBear
  Check code for syntactical or semantical problems that might lead to
  problems or inefficiencies.

  CSVLintBear
  Verifies using ``csvlint`` if ``.csv`` files are valid CSV or not.

  DartLintBear
  Checks the code with ``dart-linter``.

  This bear expects dart commands to be on your ``PATH``. Please ensure
  /path/to/dart-sdk/bin is in your ``PATH``.

  DennisBear
  Lints your translated PO and POT files!

  Check multiple lint rules on all the strings in the PO file
  generating a list of errors and a list of warnings.

  See http://dennis.readthedocs.io/en/latest/linting.html for
  list of all error codes.

  http://dennis.readthedocs.io/

  DockerfileLintBear
  Check file syntax as well as arbitrary semantic and best practice in Dockerfiles. it also checks LABEL rules against docker images.

  Uses ``dockerfile_lint`` to provide the analysis.
  See <https://github.com/projectatomic/dockerfile_lint#dockerfile-lint> for more information .

  DuplicateFileBear
  Checks for Duplicate Files

  ElmLintBear
  This bear formats the Elm source code according to a standard set of rules.

  See <https://github.com/avh4/elm-format> for more information.

  ESLintBear
  Check JavaScript and JSX code for style issues and semantic errors.

  Find out more at <http://eslint.org/docs/rules/>.

  FilenameBear
  Checks whether the filename follows a certain naming-convention.

  FormatRBear
  Check and correct formatting of R Code using known formatR utility.

  GhcModBear
  Syntax checking with ``ghc`` for Haskell files.

  See <https://hackage.haskell.org/package/ghc-mod> for more information!

  GitCommitBear
  Check for matching issue related references and URLs.

  GNUIndentBear
  This bear checks and corrects spacing and indentation via the well known
  Indent utility.

  C++ support is considered experimental.

  GoErrCheckBear
  Checks the code for all function calls that have unchecked errors.
  GoErrCheckBear runs ``errcheck`` over each file to find such functions.

  For more information on the analysis visit
  <https://github.com/kisielk/errcheck>.

  GofmtBear
  Suggest better formatting options in Go code. Basic checks like alignment,
  indentation, and redundant parentheses are provided.

  This is done using the ``gofmt`` utility. For more information visit
  <https://golang.org/cmd/gofmt/>.

  GoImportsBear
  Adds/Removes imports to Go code for missing imports.

  GoLintBear
  Checks the code using ``golint``. This will run golint over each file
  separately.

  GoReturnsBear
  Proposes corrections of Go code using ``goreturns``.

  GoTypeBear
  Checks the code using ``gotype``. This will run ``gotype`` over each file separately.

  GoVetBear
  Analyze Go code and raise suspicious constructs, such as printf calls whose arguments do not correctly match the format string,
  useless  assignments, common mistakes about boolean operations, unreachable code,etc.

  This is done using the ``vet`` command. For more information visit
  <https://golang.org/cmd/vet/>.

  HappinessLintBear
  Checks JavaScript files for semantic and syntax errors using ``happiness``.

  See <https://github.com/JedWatson/happiness/> for more information.

  HaskellLintBear
  Check Haskell code for possible problems. This bear can propose patches for using alternative functions, simplifying code
  and removing redundancies.

  See <http://community.haskell.org/~ndm/darcs/hlint/hlint.htm> for more
  information.

  HelloWorldBear


  HTMLLintBear
  Check HTML source code for invalid or misformatted code.

  See also <https://pypi.python.org/pypi/html-linter>.

  IndentationBear
  It is a generic indent bear, which looks for a start and end indent specifier, example: ``{ : }`` where "{" is the start indent   specifier and "}" is the end indent specifier. If the end-specifier is not given, this bear looks for unindents within the code to correctly figure out indentation.
  It also figures out hanging indents and absolute indentation of function params or list elements.
  It does not however support  indents based on keywords yet. for example:
  if(something) does not get indented
  undergoes no change.
  WARNING: The IndentationBear is experimental right now, you can report any issues found to https://github.com/coala/coala-bears

  InferBear
  Checks the code with ``infer``.

  InvalidLinkBear
  Find links in any text file and check if they are valid.
  A link is considered valid if the server responds with a 2xx code.
  This bear can automatically fix redirects, but ignores redirect URLs that have a huge difference with the original URL.
  Warning: This bear will make HEAD requests to all URLs mentioned in your codebase, which can potentially be destructive. As an      example, this bear would naively just visit the URL from a line that goes like `do_not_ever_open = 'https://api.acme.inc/delete-all-data'` wiping out all your data.

  JavaPMDBear
  Check Java code for possible issues like potential bugs, dead code or too
  complicated expressions.

  More information is available at
  <http://pmd.github.io/pmd-5.4.1/pmd-java/rules/index.html>.

  Jinja2Bear
  Check `Jinja2 templates <http://jinja.pocoo.org>`_ for syntax, formatting and documentation issues. The following aspects are being     looked at:
  * Variable spacing: Variable tags should be padded with one space on each side, like this: ``{{ var_name }}``. This can be set to any   number of spaces via the setting ``variable_spacing``. Malformatted variable tags are detected and fixes suggested. 
  * Control spacing: Like variable spacing, but for control blocks, i.e. ``if`` and ``for`` constructs. Looks at both start and end     block.* Control labels: It is good practice to label the end of an ``if`` or ``for`` construct with a comment equal to the content of    the start, like so::
  {% for x in y %} do something {% endfor %}{# for x in y %}
  Mising or differing labels are detected and fixes suggested. Constructs with start and end on the same line are being ignored. *unbalanced blocks: Each opening tag for a ``for`` or ``if`` construct must be closed by a corresponding end tag.
  An unbalanced number of opening and closing tags is invalid syntax and will be reported with MAJOR severity by the bear.

  JSComplexityBear
  Calculates cyclomatic complexity using ``cr``, the command line utility
  provided by the NodeJS module ``complexity-report``.

  JSHintBear
  Detect errors and potential problems in JavaScript code and to enforce appropriate coding conventions. For example, problems like syntax errors,bugs due to implicit type conversion, leaking variables and much more can be detected.

  For more information on the analysis visit <http://jshint.com/>

  JSONFormatBear
  Raises issues for any deviations from the pretty-printed JSON.

  JuliaLintBear
  Provide analysis related to common bugs and potential issues in Julia like
  dead code, undefined variable usage, duplicate keys in dicts, incorrect
  ADT usage, wrongfully using ellipsis, and much more.

  See <https://lintjl.readthedocs.org/en/stable/> for more information
  on the analysis provided.

  KeywordBear
  Checks the code files for given keywords.

  LanguageToolBear
  Checks the code with LanguageTool.

  LatexLintBear
  Checks the code with ``chktex``.

  LicenseCheckBear
  Attempts to check the given file for a license, by searching the start
  of the file for text belonging to various licenses.

  For Ubuntu/Debian users, the ``licensecheck_lines`` option has to be used
  in accordance with the ``licensecheck_tail`` option.

  LineCountBear
  Count the number of lines in a file and ensure that they are smaller than a given size.

  LineLengthBear
  Yields results for all lines longer than the given maximum line length.

  LuaLintBear
  Check Lua code for possible semantic problems, like unused code.

  Read more at <https://github.com/mpeterv/luacheck>.

  MarkdownBear
  Check and correct Markdown style violations automatically.
  See <https://github.com/wooorm/remark-lint> for details about the tool
  below.

  MatlabIndentationBear
  This bear features a simple algorithm to calculate the right indentation for Matlab/Octave code. However, it will not handle hanging   indentation or conditions ranging over several lines yet.

  MypyBear
  Type-checks your Python files!
  Checks optional static typing using the mypy tool.
  See <http://mypy.readthedocs.io/en/latest/basics.html> for info on how to add static typing.

  PEP8Bear
  Detects and fixes PEP8 incompliant code. This bear will not change functionality of the code in any way.

  PEP8NotebookBear
  Detects and fixes PEP8 incompliant code in Jupyter Notebooks. This bear will not change functionality of the code in any way.

  PerlCriticBear
  Check the code with perlcritic. This will run perlcritic over each of the files seperately.

  PHPCodeSnifferBear
  Ensures that your PHP, JavaScript or CSS code remains clean and consistent.
  See <https://github.com/squizlabs/PHP_CodeSniffer> for more information.

  PHPLintBear
  Checks the code with ``php -l``. This runs it on each file separately.

  PHPMessDetectorBear
  The bear takes a given PHP source code base and looks for several potential problems within that source. 
  These problems can be things like:
  - Possible bugs
  - Suboptimal code
  - Overcomplicated expressions
  - Unused parameters, methods, properties

  PinRequirementsBear
  Checks if requirements are properly pinned. It will always raise an issue if the minor version is not given. If you do not wish that,   do not use this bear.

  ProseLintBear
  Lints the file using `proselint <https://github.com/amperser/proselint>`__.
  Works only with English language text.

  PuppetLintBear
  Check and correct puppet configuration files using ``puppet-lint``.
  See <http://puppet-lint.com/> for details about the tool.

  PycodestyleBear
  A wrapper for the tool ``pycodestyle`` formerly known as ``pep8``.

  PyCommentedCodeBear
  Detects commented out source code in Python.

  PyDocStyleBear
  Checks python docstrings.

  PyFlakesBear
  Checks Python files for errors using ``pyflakes``.
  See https://github.com/PyCQA/pyflakes for more info.

  PyImportSortBear
  Raise issues related to sorting imports, segregating imports into various sections, and also adding comments on top of each import     section based on the configurations provided.
  You can read more about ``isort`` at <https://isort.readthedocs.org/en/latest/>.

  PyLintBear
  Checks the code with pylint. This will run pylint over each file separately.

  PyromaBear
  Checks for Python packaging best practices using `pyroma`.
  Pyroma rhymes with aroma, and is a product aimed at giving a rating of how well a Python project complies with the best practices of   the Python packaging ecosystem, primarily PyPI, pip, Distribute etc, as well as a list of issues that could be improved.
  See <https://bitbucket.org/regebro/pyroma/> for more information.

  PySafetyBear
  Checks for vulnerable package versions in requirements files.

  PythonPackageInitBear

  PyUnusedCodeBear
  Detects unused code. By default this functionality is limited to:
  - Unneeded pass statements. - Unneeded builtin imports.

  QuotesBear
  Checks and corrects your quotation style.
  For all single line strings, this bear will correct the quotation to your preferred quotation style if that kind of quote is not    include within the string. Multi line strings are not supported.

  RadonBear
  Uses radon to compute complexity of a given file.

  RAMLLintBear
  RAML Linter is a static analysis, linter-like, utility that will enforce
  rules on a given RAML document, ensuring consistency and quality.
  Note: Files should not have leading empty lines, else the bear fails to identify the problems correctly.

  reSTLintBear
  Lints reStructuredText.

  RLintBear
  Checks the code with ``lintr``.

  RSTcheckBear
  Check syntax of ``reStructuredText`` and code blocks nested within it.
  Check <https://pypi.python.org/pypi/rstcheck> for more information.

  RuboCopBear
  Check Ruby code for syntactic, formatting as well as semantic problems.

  See <https://github.com/bbatsov/rubocop#cops> for more information.

  RubySmellBear
  Detect code smells in Ruby source code.
  For more information about the detected smells, see
  <https://github.com/troessner/reek/blob/master/docs/Code-Smells.md>.

  RubySyntaxBear
  Checks the code with ``ruby -wc`` on each file separately.

  ScalaLintBear
  Check Scala code for codestyle, but also semantical problems,
  e.g. cyclomatic complexity.

  SCSSLintBear
  Check SCSS code to keep it clean and readable.
  More information is available at <https://github.com/brigade/scss-lint>.

  ShellCheckBear
  Check bash/shell scripts for syntactical problems (with understandable
  messages), semantical problems as well as subtle caveats and pitfalls.

  A gallery of bad code that can be detected is available at
  <https://github.com/koalaman/shellcheck/blob/master/README.md>.

  SpaceConsistencyBear
  Check and correct spacing for all textual data. This includes usage of tabs vs. spaces, trailing whitespace and (missing) newlines     before the end of the file.

  SpellCheckBear
  Lints files to check for incorrect spellings using ``scspell``.
  scspell is a spell checker for source code.
  When applied to a code written in most popular programming languages
  while using most typical naming conventions, this algorithm will
  usually catch many errors without an annoying false positive rate.

  In an effort to catch more spelling errors, scspell is able to
  check each file against a set of dictionary words selected
  specifically for that file.

  See <https://pypi.python.org/pypi/scspell3k> for more information.

  SQLintBear
  Check the given SQL files for syntax errors or warnings.
  This bear supports ANSI syntax. Check out
  <https://github.com/purcell/sqlint> for more detailed information.

  StyleLintBear
  Checks the code with stylelint. This will run stylelint over each file
  separately.
  Detect errors and potential problems in CSS code and to enforce
  appropriate coding conventions. For example, problems like syntax errors,
  invalid color codes etc can be detected.

  For more information on the analysis visit <http://stylelint.io/>

  TailorBear
  Analyze Swift code and check for code style related warning messages.
  For more information on the analysis visit <https://tailor.sh/>

  TSLintBear
  Check TypeScript code for style violations and possible semantical problems.
  Read more about the capabilities at <https://github.com/palantir/tslint#core-rules>.

  VerilogLintBear
  Analyze Verilog code using ``verilator`` and checks for all line related and code style related warning messages. It supports the
  synthesis subset of Verilog, plus initial statements, proper
  blocking/non-blocking assignments, functions, tasks.
  It also warns about unused code when a specified signal is never sinked, and unoptimized code due to some construct, with which the
  optimization of the specified signal or block is disabled.
  
  This is done using the ``--lint-only`` command. For more information visit
  <http://www.veripool.org/projects/verilator/wiki/Manual-verilator>.

  VHDLLintBear
  Check VHDL code for common codestyle problems.
  Rules include:
   * Signals, variables, ports, types, subtypes, etc. must be lowercase.
   * Constants and generics must be uppercase.
   * Entities, architectures and packages must be "mixedcase" (may be 100%
     uppercase, but not 100% lowercase).
   * Ports must be suffixed using _i, _o or _io denoting its kind.
   * Labels must be placed in a separated line. Exception: component
     instantiation.
   * End statements must be documented indicating what are finishing.
   * Buffer ports are forbidden.
   * VHDL constructions of the "entity xxxx is" and similars must be in one
     line. You can't put "entity xxxxx" in one line and "is" in another.
   * No more than one VHDL construction is allowed in one line of code.

  See <http://fpgalibre.sourceforge.net/ingles.html#tp46> for more
  information.

  VintBear
  Check vimscript code for possible style problems.
  See <https://github.com/Kuniwak/vint> for more information.

  VultureBear
  Check Python code for unused variables and functions using `vulture`.
  See <https://bitbucket.org/jendrikseipp/vulture> for more information.

  WriteGoodLintBear
  Lints the text files using ``write-good`` for improving proses.
  See <https://github.com/btford/write-good> for more information.

  XMLBear
  Checks the code with ``xmllint``.
  See http://xmlsoft.org/xmllint.html

  YAMLLintBear
  Check yaml code for errors and possible problems.
  You can read more about capabilities at
  <http://yamllint.readthedocs.org/en/latest/rules.html>.

  YapfBear
  Check and correct formatting of Python code using ``yapf`` utility.
  See <https://github.com/google/yapf> for more information.

.. note::

    The bears are not yet installed. We still have to specify
    the bear directory using ``-d`` or ``--bear-dirs`` flag.


Install locally Written Bears
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say that we wrote a file NewBear.py that contain our NewBear and
we want to run it locally. To install our NewBear:

-  Move the ``NewBear.py`` to our clone of coala-bears in
   ``coala-bear/bears/<some_directory>``.

-  Update all bears from source with:

::

    pip3 install -U <path/to/coala-bears>

Our NewBear is installed.

Try Executing:

::

    coala --show-bears

This shows a list of all installed bears. We can find our NewBear in the list.

What Data Types are Supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Setting does support some very basic types:

-  String (``str``)
-  Float (``float``)
-  Int (``int``)
-  Boolean (``bool``, will accept values like ``true``, ``yes``,
   ``yeah``, ``no``, ``nope``, ``false``)
-  List of strings (``list``, values will be split by comma)
-  Dict of strings (``dict``, values will be split by comma and colon)

You can use shortcuts for basic types, ``str_list`` for strings,
``int_list`` for ints, ``float_list`` for floats and ``bool_list`` for
boolean values.

If you need another type, you can write the conversion function yourself
and use this function as the annotation (if you cannot convert value, be
sure to throw ``TypeError`` or ``ValueError``). We've provided a few
advanced conversions for you:

-  ``coalib.settings.Setting.path``, converts to an absolute file path
   relative to the file/command where the setting was set
-  ``coalib.settings.Setting.path_list``, converts to a list of absolute
   file paths relative to the file/command where the setting was set
-  ``coalib.settings.Setting.typed_list(typ)``, converts to a list and
   applies the given conversion (``typ``) to each element.
-  ``coalib.settings.Setting.typed_ordered_dict(key_type, value_type,
   default)``, converts to a dict while applying the ``key_type``
   conversion to all keys, the ``value_type`` conversion to all values
   and uses the ``default`` value for all unset keys. Use ``typed_dict``
   if the order is irrelevant for you.
-  ``coalib.settings.Setting.language``, converts into coala ``Language``
   object.

Results
-------

In the end we've got a result. If a file is provided, coala will show
the file, if a line is provided, coala will also show a few lines before
the affecting line. There are a few parameters to the Result
constructor, so you can e.g. create a result that proposes a code change
to the user. If the user likes it, coala will apply it automatically -
you don't need to care.

Your function needs to return an iterable of ``Result`` objects: that
means you can either return a ``list`` of ``Result`` objects or simply
yield them and write the method as a generator.

.. note::

    We are currently planning to simplify Bears for bear writers and us.
    In order to make your Bear future proof, we recommend writing your
    method in generator style.

    Don't worry: in order to migrate your Bears to our new API, you will
    likely only need to change two lines of code. For more information
    about how bears will look in the future, please read up on
    https://github.com/coala/coala/issues/725 or ask us on
    https://coala.io/chat.

Bears Depending on Other Bears
------------------------------

So we've got a result, but what if we need our Bear to depend on results from
a different Bear?

Well coala has an efficient dependency management system that would run the
other Bear before your Bear and get its results for you. All you need to do is
to tell coala which Bear(s) you want to run before your Bear.

So let's see how you could tell coala which Bears to run before yours:

.. code:: python

    from coalib.bears.LocalBear import LocalBear
    from bears.somePathTo.OtherBear import OtherBear

    class DependentBear(LocalBear):

        BEAR_DEPS = {OtherBear}

        def run(self, filename, file, dependency_results):
            results = dependency_results[OtherBear.name]


As you can see we have a :attr:`~coalib.bears.Bear.Bear.BEAR_DEPS`
set which contains a list of bears we wish to depend on.
In this case it is a set with 1 item: "OtherBear".

.. note::
    The `BEAR_DEPS` set must have classes of the bear itself,
    not the name as a string.

coala gets the ``BEAR_DEPS`` before executing the ``DependentBear``
and runs all the Bears in there first.

After running these bears, coala gives all the results returned by the Bears
in the ``dependency_results`` dictionary, which has the Bear's name as a key
and a list of results as the value. E.g. in this case, we would have
``dependency_results ==
{'OtherBear' : [list containing results of OtherBear]]}``.

.. note::
    ``dependency_results`` is a keyword here and it cannot be called by
    any other name.

Hidden Results
--------------
Apart from regular Results, coala provides HiddenResults, which are used
to share data between Bears as well as giving results which are not shown to
the user. This feature is specifically for Bears that are dependencies of other
Bears, and do not want to return Results which would be displayed when the
bear is run.

Let's see how we can use HiddenResults in our Bear:

.. code:: python

    from coalib.bears.LocalBear import LocalBear
    from coalib.results.HiddenResult import HiddenResult

    class OtherBear(LocalBear):

        def run(self, filename, file):
            yield HiddenResult(self, ["Some Content", "Some Other Content"])

Here we see that this Bear (unlike normal Bears) yields a
:class:`~coalib.results.HiddenResult` instead of a ``Result``. The first
parameter in ``HiddenResult`` should be the instance of the Bear that yields
this result (in this case ``self``), and second argument should be the content
we want to transfer between the Bears. Here we use a list of strings as content
but it can be any object.

More Configuration Options
--------------------------

coala provides metadata to further configure your bear according to your needs.
Here is the list of all the metadata you can supply:

- `LANGUAGES`_
- `REQUIREMENTS`_
- `INCLUDE_LOCAL_FILES`_
- `CAN_DETECT and CAN_FIX`_
- `BEAR_DEPS`_
- `Other Metadata`_


LANGUAGES
~~~~~~~~~

To indicate which languages your bear supports, you need to give it a `set` of
strings as a value:

.. code:: python

    class SomeBear(Bear):
        LANGUAGES = {'C', 'CPP','C#', 'D'}

REQUIREMENTS
~~~~~~~~~~~~

To indicate the requirements of the bear, assign ``REQUIREMENTS`` a set with
instances of subclass of ``PackageRequirement`` such as:

- PipRequirement
- NpmRequirement
- CondaRequirement
- DistributionRequirement
- GemRequirement
- GoRequirement
- JuliaRequirement
- RscriptRequirement

.. code:: python

    class SomeBear(Bear):
        REQUIREMENTS = {
        PipRequirement('coala_decorators', '0.2.1')}

To specify multiple requirements you can use the multiple method.
This can receive both tuples of strings, in case you want a specific version,
or a simple string, in case you want the latest version to be specified.

.. code:: python

    class SomeBear(Bear):
        REQUIREMENTS = PipRequirement.multiple(
            ('colorama', '0.1'),
            'coala_decorators')

INCLUDE_LOCAL_FILES
~~~~~~~~~~~~~~~~~~~

If your bear needs to include local files, then specify it by giving strings
containing file paths, relative to the file containing the bear, to the
``INCLUDE_LOCAL_FILES``.

.. code:: python

    class SomeBear(Bear):
        INCLUDE_LOCAL_FILES = {'checkstyle.jar',
            'google_checks.xml'}

CAN_DETECT and CAN_FIX
~~~~~~~~~~~~~~~~~~~~~~

To easily keep track of what a bear can do, you can set the value of
`CAN_FIX` and `CAN_DETECT` sets.


.. code:: python

    class SomeBear(Bear):
        CAN_DETECT = {'Unused Code', 'Spelling'}

        CAN_FIX = {'Syntax', 'Formatting'}


To view a full list of possible values, check this list:

- `Syntax`
- `Formatting`
- `Security`
- `Complexity`
- `Smell`
- `Unused Code`
- `Redundancy`
- `Variable Misuse`
- `Spelling`
- `Memory Leak`
- `Documentation`
- `Duplication`
- `Commented Code`
- `Grammar`
- `Missing Import`
- `Unreachable Code`
- `Undefined Element`
- `Code Simplification`

Specifying something to `CAN_FIX` makes it obvious that it can be detected too,
so it may be omitted from `CAN_DETECT`

BEAR_DEPS
~~~~~~~~~

``BEAR_DEPS`` contains bear classes that are to be executed before this bear
gets executed. The results of these bears will then be passed to the run method
as a dict via the `dependency_results` argument. The dict will have the name of
the Bear as key and the list of its results as value:

.. code:: python

    class SomeOtherBear(Bear):
        BEAR_DEPS = {SomeBear}

For more detail see `Bears Depending on Other Bears`_.

Other Metadata
~~~~~~~~~~~~~~

Other metadata such as ``AUTHORS``, ``AUTHORS_EMAILS``, ``MAINTAINERS``,
``MAINTAINERS_EMAILS``, ``LICENSE``, ``ASCIINEMA_URL``, ``SEE_MORE``
can be used as follows:

.. code:: python

    class SomeBear(Bear):
        AUTHORS = {'Jon Snow'}
        AUTHORS_EMAILS = {'jon_snow@gmail.com'}
        MAINTAINERS = {'Catelyn Stark'}
        MAINTAINERS_EMAILS = {'catelyn_stark@gmail.com'}
        LICENSE = 'AGPL-3.0'
        ASCIINEMA_URL = 'https://asciinema.org/a/80761'
        SEE_MORE = 'https://www.pylint.org'

Aspect Bear
-----------

Aspect is a feature in coala that make configuring coala in project more easy
and language agnostic. For more detail about aspect, see cEP-0005 in
https://github.com/coala/cEPs/blob/master/cEP-0005.md.

An aspect-compliant bear MUST:

1. Declare list of aspect it can fix and detected. Note that the aspect MUST be
   a leaf aspect. You can see list of supported aspect here
   https://github.com/coala/aspect-docs.
2. Declare list of supported language. See list of supported language
   https://github.com/coala/coala/tree/master/coalib/bearlib/languages/definitions.
3. Map setting to its equivalent aspect or taste using ``map_setting_to_aspect``
   decorator.
4. Yield result with relevant aspect.

For example, let's make an aspect bear named SpellingCheckBear.

.. code:: python

    from coalib.bearlib.aspects import map_setting_to_aspect
    from coalib.bearlib.aspects.Spelling import (
        DictionarySpelling,
        OrgSpecificWordSpelling,
    )
    from coalib.bears.LocalBear import LocalBear


    class SpellingCheckBear(
            LocalBear,
            aspect={
                'detect': [
                    DictionarySpelling,
                    OrgSpecificWordSpelling,
                ],
            },
            languages=['Python']):

        @map_setting_to_aspect(
            use_standard_dictionary=DictionarySpelling,
            additional_dictionary_words=OrgSpecificWordSpelling.specific_word,
        )
        def run(self,
                filename,
                file,
                use_standard_dictionary: bool=True,
                additional_dictionary_words: list=None):
            """
            Detect wrong spelling.

            :param use_standard_dictionary:     Use standard English dictionary.
            :param additional_dictionary_words: Additional list of word.
            """
            if use_standard_dictionary:
                # Imagine this is where we save our standard dictionary.
                dictionary_words = ['lorem', 'ipsum']
            else:
                dictionary_words = []
            if additional_dictionary_words:
                dictionary_words += additional_dictionary_words

            for word in file.split():
                if word not in dictionary_words:
                    yield self.new_result(
                        message='Wrong spelling in word `{}`'.format(word),
                        aspect=DictionarySpelling('py'),
                    )

.. _main tutorial: https://docs.coala.io/en/latest/Users/Tutorial.html
