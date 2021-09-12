coala 0.12 - XBear
==================

This release was brought to you by 116 contributors contributing 353
commits.

This release was long overdue, and contains several improvements
in many components of coala, as well as the latest GSoC projects
and features.

The Next-Gen core is still on its way, but it's nearly done, and you can
soon enjoy coala's new core features :)

**Breaking Changes**

- Write output to empty file instead of appending.
  When ``--output`` option is specified, write output of coala to a
  fresh file. This avoids file corruption for certain output formats
  (like ``--json``).
- ``coalib.misc.Shell.get_shell_type`` was removed without deprecation.
- ``Interactions.fail_acquire_settings``: Removed parameter ``section``
  without deprecation.
  `Issue #4740 <https://github.com/coala/coala/issues/4740>`_

**General**

- Improved results output.
- NeoVim is now an editor recognized by coala.
  `Issue #4084 <https://github.com/coala/coala/issues/4084>`_
- New aspects added:
  - ``coalaCorrect`` (`Issue #236@gitlab/coala/GSoC-2017 <https://gitlab.com/coala/GSoC-2017/issues/236>`_)
  - ``Smell`` (`Issue #4305 <https://github.com/coala/coala/issues/4305>`_)
  - ``Security``
  - ``Formatting``
  - ``Indentation``
- New generic filtering system with the ``--filter-by`` flag.
  Filters for language, can-fix- and can-detect-capabilities
  are available in this version. New filters going to come.
  `Issue #2509 <https://github.com/coala/coala/issues/2509>`_
- Basic language features added for
  - TypeScript
  - Shell
- HTML language support for ignore comments was added.
  `Issue #4260 <https://github.com/coala/coala/issues/4260>`_
- Certain bears can now be queried for info with ``--show-bears``
  together with ``--bears``.
  `Issue #4651 <https://github.com/coala/coala/issues/4651>`_
- Windows-style backslashes can now be provided in Windows-shells
  without escaping them for arguments that accept a path. This
  improves workflow with the native auto-completion inside
  Windows-shells.
  `Issue #4356 <https://github.com/coala/coala/issues/4356>`_
- Change naming of ``default_coafile``: ``system_coafile``
  shall be used instead. ``default_coafile`` is hereby deprecated.
  `Issue #3389 <https://github.com/coala/coala/issues/3389>`_
- ``--debug`` flag added; coala immediately steps into a
  debugging-session on errors.

**Bear Developers**

- Bear can now process non-text files.
  `Issue #3529 <https://github.com/coala/coala/issues/3529>`_
- ``CAN_DETECT`` field inside bears got ``Statistics`` as new
  category.
  `Issue #4233 <https://github.com/coala/coala/issues/4233>`_
- ``HiddenResult.__init()__`` now has all the parameters of
  ``Result.__init()__``.
  `Issue #4454 <https://github.com/coala/coala/issues/4454>`_
- Added specialized shortcuts for ``typed_list``,
  for ``str``, ``int``, ``float`` and ``bool`` types.
  `Issue #3224 <https://github.com/coala/coala/issues/3224>`_
- ``LocalBearTestHelper``
  - Add ``check_invalidity``
    `Issue #2197 <https://github.com/coala/coala/issues/2197>`_
  - ``settings`` argument added to ``check_validity`` and
    ``check_invalidity``. This allows to quickly supply section
    settings without overhead.
    `Issue #4247 <https://github.com/coala/coala/issues/4247>`_
  - Added ``check_line_result_count()``,
    to quickly assert how many results occurred on a line.
    `Issue #4227 <https://github.com/coala/coala/issues/4227>`_
  - ``get_results()`` supports now bears with dependencies
    properly.
    `Issue #2860 <https://github.com/coala/coala/issues/2860>`_

**API Changes**

- The two duplicated ``CircularDependencyError`` classes were merged,
  please use ``coalib.core.CircularDependencyError``.
  `Issue #4191 <https://github.com/coala/coala/issues/4191>`_
- Added ``LinterClass``, a virtual base class for linters.
- ``ChainPatchAction`` added
- ``Language``: ``UnknownLanguageError`` created for failing
  language lookups.
  `Issue #4642 <https://github.com/coala/coala/issues/4642>`_
- ``SectionFilling.acquire_settings``: Deprecated ``section``
  parameter.
- ``ConsoleInteraction.show_bear``.py: Deprecated parameters
  ``show_params`` and ``show_description``.
  `Issue #4868 <https://github.com/coala/coala/issues/4868>`_
- ``Diff``
  - ``__bool__``: Behaviour was changed to be more consistent.
    `Issue #4178 <https://github.com/coala/coala/issues/4178>`_
  - Consistently appends linebreaks if they aren't passed with
    file-data.
    `Issue #3834 <https://github.com/coala/coala/issues/3834>`_
- Documentation API:
  - Added support for ``:raises ...:`` metadata.
    `Issue #4279 <https://github.com/coala/coala/issues/4279>`_
  - Improved docstring recognition.
    `Issue #4291 <https://github.com/coala/coala/issues/4291>`_
  - ``DocumentationComment`` accepts now a position instead
    of a range.
    `Issue #2646 <https://github.com/coala/coala/issues/2646>`_
  - Added ``DocBaseClass``.
    `Issue #2659 <https://github.com/coala/coala/issues/2659>`_
  - Added ``MalformedComment``
    `Issue #4548 <https://github.com/coala/coala/issues/4548>`_
  - Added ``padding`` and ``type`` attributes to API.
- Aspects
  - Created exception for aspects lookup.
    `Issue #4381 <https://github.com/coala/coala/issues/4381>`_,
    `Issue #4402 <https://github.com/coala/coala/issues/4402>`_
  - ``coalib.bearlib.aspects.meta.aspectTypeError`` is now
    ``coalib.bearlib.aspects.exceptions.AspectTypeError``.
  - ``AspectList``: Overload ``__init__`` to accept strings.
    `Issue #4382 <https://github.com/coala/coala/issues/4382>`_
  - ``aspectbase`` & ``AspectList`` & ``aspectModule``:
    Add ed``get()`` method, that serves as quick way to get a
    specific, deep subaspect of an aspect.
    `Issue #4410 <https://github.com/coala/coala/issues/4410>`_,
    `Issue #4384 <https://github.com/coala/coala/issues/4384>`_,
    `Issue #4411 <https://github.com/coala/coala/issues/4411>`_
  - ``AspectList``: Added ``exclude`` attribute.
    `Issue #4438 <https://github.com/coala/coala/issues/4438>`_
  - Created ``get_leaf_aspects`` method.
  - Added ``map_setting_to_aspect`` decorator.
    `Issue #4661 <https://github.com/coala/coala/issues/4661>`_

**Bugfixes**

- Section inheritance fixed for upper-cased section names.
  `Issue #4182 <https://github.com/coala/coala/issues/4182>`_
- coala now properly detects BOMs.
  `Issue #1205@coala-bears <https://github.com/coala/coala-bears/issues/1205>`_
- Coloring bug with ``--no-color`` flag was resolved
  `Issue #4185 <https://github.com/coala/coala/issues/4185>`_
- Fix `--apply-patches` not working
  `Issue #4957 <https://github.com/coala/coala/issues/4957>`_
- ``Diff.unified_diff`` renders now properly even when no
  linebreaks were passed to the ``Diff`` instance.
- Linter: Stop TypeError being raised during debug logging.
  `Issue #4433 <https://github.com/coala/coala/issues/4433>`_
- Documentation API
  - Unwanted diff-cutoff fixed.
    `Issue #4187 <https://github.com/coala/coala/issues/4187>`_
  - Cornercase behaviour fixed in ``DocumentationComment.assemble()``.
    `Issue #2645 <https://github.com/coala/coala/issues/2645>`_
  - ``DocumentationComment``: Fixed exception when ending colon missing
    of metadata.
    `Issue #2143 <https://github.com/coala/coala/issues/2143>`_
  - DocstyleDefinition: Multiple loading of coalang files led to unwanted
    section overrides.
    `Issue #4470 <https://github.com/coala/coala/issues/4470>`_
  - Various fixes covered by
    `Issue #4029 <https://github.com/coala/coala/issues/4029>`_
- ``aspectbase``: Recursively instantiate aspect children.
    `Issue #4388 <https://github.com/coala/coala/issues/4388>`_
- Made ``Language`` class pickle-able.
- Collectors: Stabilised bear order irrespective of the order
  of entries returned by the file-system.
  `Issue #4541 <https://github.com/coala/coala/issues/4541>`_


coala 0.11 - BrewBear
=====================

This release was brought to you by 65 contributors contributing 141
commits.

The name of this release is BrewBear to highlight the improvements made to
our dependency management system, including the addition of ``brew`` support
for mac users. Mac has been an officially supported platform for a long time
and we would like to draw attention to this often overlooked fact.
Support has also been added for ``conda`` and ``cargo`` allowing bears which
use linters available from those package managers to manage their dependencies.

Initial next generation core code has been merged and will be integrated over
the coming releases. Until then, please use the current API.

We have added a release candidate system to our release process to allow users
to easily test changes in the latest pre-release version of coala.
Instructions for obtaining the rc package will be posted for each minor/major
release to the coala gitter channel, blog, and twitter. We encourage all users
interested in checking out new features or helping to test these pre-releases
on their projects. If you do find a regression in a release candidate, please
report it to the issue tracker with the word ``Regression`` somewhere in the
title.

**Breaking Changes**

- coala now exits with a non zero exit code when error level results are logged.
  If you relied on coala logging in scripts or other automated systems please
  modify them to work with the new behavior. You can find all exit codes
  `here <http://docs.coala.io/en/latest/Users/Exit_Codes.html>`__.
  `PR #3905 <https://github.com/coala/coala/pull/3905>`_

**General**

- Section Inheritance had been added to the coafile parsing. With this
  change we are deprecating implicit ``default`` section inheritance.
  Instead, you can now have definite section inheritance by using the
  ``.`` in the section title. Append operators are now supported allowing
  addition of values to inherited section. See the
  ``Explicit Setting Inheritance`` section of the
  `docs <https://docs.coala.io/en/latest/Users/coafile.html#explicit-setting-inheritance>`__
  for a syntax example and detailed instructions
- The section name ``cli`` is reserved for cli arguments and should not be
  used in the coala configuration file (``coafile``). If you are currently
  using it in a configuration file, coala will warn you.
- coala now outputs absolute file paths when a bear fails. This should
  make debugging bear failures easier when using custom bears.

**Usability**

- A new placeholder, ``source_lines``,  has been added to the coala
  ``--format`` option. Use it to output the affected lines in the source file
  when a result occurs.
- Bears are displayed alphabetically when listed using ``--show-bears``.
- coala outputs a warning if a setting is overridden in the same section
  since this is probably not what the user intended.
- ``--format`` is handled correctly when ``--ci`` is specified, outputting
  formatted output without asking questions.
  `Issue #3999 <https://github.com/coala/coala/issues/3999>`_
- coala will report the version of the dependency required when the version
  check fails.
  `Issue #3982 <https://github.com/coala/coala/issues/3982>`_

**Bear Developers**

- ``@linter`` decorator works with global bears. See our bear writing
  `docs <http://api.coala.io/en/latest/Developers/Writing_Linter_Bears.html#global-bears>`__
  for more information on how to write a global bear with the ``@linter``
  decorator.
- ``Bear.DownloadCachedFile`` raises exceptions when the download fails.
  Please see the requests library
  `docs <http://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions>`__
  for a complete list of possible exceptions that will need to be handled.
- The ``deprecate_settings`` decorator now supports multiple deprecations
  of the same setting.
  `Issue # 3537 <https://github.com/coala/coala/issues/3537>`_
- A new ``SEE_MORE`` attribute has been added to the ``Bear`` class. Use it
  to attribute (usually by linking the main page)  the original tool in
  linter bears.
- Unified Diff support has been added to the ``Diff`` result, linter
  and display mechanisms.

**Bugfixes**

- Caching has been fixed to work correctly. Results are only cached when a
  bear successfully runs. A bear which fails in the middle of a run will
  not have a result cached anymore. This should make flushing the cache
  manually mostly unnecessary for end users.
  `PR #3722 <https://github.com/coala/coala/pull/3722>`_
- Non-optional settings check settings from dependent bears now. Previously,
  it would error because the dependency would not have its settings satisfied.
  `Issue #3149 <https://github.com/coala/coala/pull/3149>`_
- The ``Result`` object now handles ``None`` values of TextPosition properly.
  Previously, it would return arbitrary results which would impact bear
  authors.
  `Issue #3094 <https://github.com/coala/coala/issues/3094>`_
- A few problems when using coala in systems with incomplete locales data
  have been fixed. This was common in Docker containers.
  `Issue #3906 <https://github.com/coala/coala/issues/3906>`_

coala 0.10 - PolarBear
======================

::


                       `++-    -o+`
                -oo:  :yhho    ohhy:  :oo.
                :hhhoohhh+      +hhhoohhy:
            ``.--shhhhhy:        /yhhhhho--..`
           +hhhhhhhhhhh+          ohhhhhhhhhhh/
           `/+/////+hhhh/        +hhhy+///////`
                    -yhhhs     hshhhy-
       .os/           hhhhy-  -yhhhh           +ss.
       .yhho           shhho``ohhhs          `ohhy`
        -yhhs`          +hhhsshhh+          `shhy-
      .::shhhs++/+yhy////shhhhhhs////yhy++++yhhho::-
     /hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh/
      -::shhhs++++yhy////shhhhhhs          +shhhs::.
        -yhhs`          +hhhsshhh+          `shhy-
       .yhho`          shhho``ohhhs           ohhy.
       .ss+           hhhhy   -yhhhh           /so.
                    -yhhhs      shhhy-
           `///////+yhhh+        /hhhh+/////+/`
           /hhhhhhhhhhho          +hhhhhhhhhhh+
            `..--ohhhhhy/        :yhhhhhs--.``
                :hhhoohhh+      +hhhoohhh:
                -oo:  :yhho    ohhy:  :oo-
                       `+o-    -++`

For this release we had 168 commits contributed by 66 unique contributors
over 2.5 months.

The name of this release is PolarBear to reflect changes we have made to our
release process. We have implemented a release freeze before all releases
to serve as a testing period for all staged changes. This should also help
us keep releases on schedule.

This release is an enhancement release which brings the usual slew of
improvements to documentation and API. We have started preparing the codebase
for the big changes that are outlined in the cEPs like section inheritance
and the next generation core.

**Known Bugs**

- Results are cached even if a bear does not run. This can lead to empty
  results where there should be errors. To temporarily deal with this
  run coala with the ``--flush-cache`` option

**General**

- Test cases have been improved across the board so they catch more errors
  before production.
- Log output via json has been added which is accessible by using the
  ``--log-json`` option.
- coala domain has been changed from ``coala-analyzer.org`` to ``coala.io``.
  Please file a bug if you find any broken links or instances of the old url.

**Usability**

- emacs has been added to list of editors that coala supports.
- coala will now output a warning if you specify an editor that is not known.
- The ``noqa`` keyword used by other linters as an ignore keyword is now
  supported as a coala ignore keyword.
- ``libclang-py3`` update to 3.4 is known to cause problems for some users.
  Please uninstall and reinstall it if coala tells you there is a version
  mismatch in ``libclang-py3``.
- ``C#`` now has proper language support and should work with AnnotationBear
  and all other bears which require language configuration.

**Deprecations**

- ``change_line`` method in ``Diff.py`` has been deprecated and has been
  scheduled for removal.
- ``format_str`` setting has been completely removed after being deprecated
  last release. Use ``format`` instead to specify a formatting string.

**Developers**

- Travis has been enabled for developers to test their changes on their own CI.

- Bears will now check for prerequisites using specified requirements
  before running. Either override ``check_prequisites`` in the bear or write
  a new requirement class if you wish to have a custom check.
- When a language is not known by coala, an ``Unknown`` language will be
  used.
- ``@linter`` decorator now warns when using unsupported or anonymous capture
  groups.
- New ``dependency_management`` package has been created to contain package
  manager and dependency classes used by coala. All of the old ``*Requirement``
  classes have been moved here. Some new dependencies classes are
  ``CabalRequirement`` and ``MavenRequirement``. Developers should add
  requirement classes there now for the requirement types they wish to support.
- ``DistributionRequirement`` can now check if a package is installed in many
  popular linux distros.
- Diffs are able to add a single line using the ``add_line`` method now.
- ``Language`` class ignores leading and trailing spaces in language lookups.
- ``Language`` class should auto-complete when using languages that have
  been defined.

**Docs**

- A Code of Conduct has been added. This will guide conflict resolution if the
  need ever arises.
- API docs are now part of the coala repository.
- Developer contribution documentation has received a major update

**Bugfixes**

- Fixed an issue where using linter bears on windows had thrown an exception.
  `Issue 3323 <https://github.com/coala/coala/issues/3323>`_
- coala ``-c`` (config file) option properly supports specifying directories.
  Previously it has thrown an exception.
  `Issue 3221 <https://github.com/coala/coala/issues/3221>`_
- Documentation status github badge has been fixed.
- Console interaction uses a unicode dot to represent spaces instead of the
  bullet for better cross platform rendering.
  `Issue 2751 <https://github.com/coala/coala/issues/2753>`_
- ``Language`` class raises proper exception to fix ``hasattr`` behavior.
  `Issue 3160 <https://github.com/coala/coala/issues/3160>`_
- Ignore statements in multi-line comments should be supported properly now.
  `Issue 3441 <https://github.com/coala/coala/issues/3441>`_

coala 0.9.1
===========

This bugfix release addressed the following issues:

- The installer has been fixed to only install on supported python versions.
  `Issue #3310 <https://github.com/coala/coala/issues/3310>`_
  `Issue #3383 <https://github.com/coala/coala/issues/3383>`_
- The format_str option to specify a format string has been restored to
  coala run in format mode. This is deprecated and was only restored to
  provide plug-in developers a grace period to switch to the replacement
  setting ``format``.
  `Issue #3303 <https://github.com/coala/coala/issues/3303>`_
- Setuptools was removed from our requirements list because having it only
  only caused dependency problems for other packages installed on the system
  `coala Bears Issue #751 <https://github.com/coala/coala-bears/issues/751>`_
- PyPrint dependency was updated to a version which does not pull in
  setuptools anymore.
- API change: An auto-apply disable option was added to run_coala to fix
  issue detection by unattended services that use coala when the coafile
  contains a default_action
  `Issue #3212 <https://github.com/coala/coala/issues/3212>`_
- A few specific language class behaviors were changed. This should only
  affect developers
  `Pull #3175 <https://github.com/coala/coala/pull/3175>`_
  `Pull #3167 <https://github.com/coala/coala/pull/3167>`_

coala 0.9.0 - GlobalBear
========================

::

                       __
                 o#'9MMHb':'-,o,
              .oH":HH$' "' ' -*R&o,
             dMMM*""'`'      .oM"HM?.
           ,MMM'          "HLbd< ?&H\
          .:MH ."\          ` MM  MM&b
         . "*H    -        &MMMMMMMMMH:
         .    dboo        MMMMMMMMMMMM.
         .   dMMMMMMb      *MMMMMMMMMP.
         .    MMMMMMMP        *MMMMMP .
              `#MMMMM           MM6P ,
          '    `MMMP"           HM*`,
           '    :MM             .- ,
            '.   `#?..  .       ..'
               -.   .         .-
                 ''-.oo,oo.-''

For this release only we had `58 different contributors
<http://pastebin.com/raw/PpdZm7yL>`_ from all around the globe contributing way
over 200 commits over 2.5 months to coala.

**The name of this release is GlobalBear** to honour our `GlobalBear` class and
leave a statement on how global the community grows: gone are the days when we
visit conferences and we have to explain the project to all the people. More
and more people know the project before we meet them and this is great! This is
a huge step in our conquest to take over the world!

The `GlobalBear` class serves our users by providing project wide "global"
analysis. This release it will probably make its last appearance because it
will be deprecated in favour of a `more sophisticated concept
<https://github.com/coala/cEPs/blob/master/cEP-0002.md>`_ in the near future.

We have also worked a lot towards building our dream of **letting users declare
code analysis configuration completely language independently**: to take a
sneak peek at what we want to do, `check this out
<https://github.com/coala/cEPs/blob/master/cEP-0005.md>`_. You will see that
the first aspects are already in our source code and that bears can already
associate results with them so future versions of coala will be able to tell
the user a plethora of facts around the type of issue pointed out.

**For users**, we have added a lot of usability improvements as well as for
example the ability to merge patches within one line: if you previously had
to run coala multiple times because of patch conflicts, this is likely not
the case anymore!

**As a Bear writer** you now have access to our ``Language`` facilities: they
will give you facts about programming languages that you analyse so you can
build truly language independent bears. Also, you now can use
http://api.coala.io/ to get more information about our classes and functions
you work with.

Command Line Interface Changes:

- ``coala-ci`` and ``coala-json`` have been deprecated. You can now use
  ``coala --non-interactive`` and ``coala --json`` respectively.
- Multiple patches within one line, even from different bears, can be
  automatically merged by coala.
- ``coala`` returns the exitcode 2 when not passing any ``--bears`` or
  ``--files`` as well as when no section is enabled and nothing was done.
- coala can now automatically add ``Ignore ...Bear`` comments to your source
  code. Simply use the ``Add ignore comment`` action when offered.
- Users can press enter to dismiss a result by default.
- Result action descriptions have been compressed to make them easier readable.
- The section name is now displayed when asking the user for missing settings.
- ``coala --non-interactive`` shows results *and* patches by default now.
- ``coala-dbus`` has been removed as it wasn't used by anyone.
- A ``--no-color`` argument allows to run coala with uncoloured results.
- Log messages are printed on stderr now.
- ``coala --json`` doesn't output log messages in JSON anymore. This is a
  technical issue. Log messages can easily be fetched from the stderr stream.
- Some performance improvements could be achieved.
- A lot more strings, like ``roger`` or ``no way`` are allowed for boolean
  values. (https://github.com/coala/coala/commit/728b7b02da8ca8f91b91c67784872244c0820a77)

Bear API Changes:

- ``LanguageDefinition`` has been deprecated. Use
  ``coalib.bearlib.languages.Language`` instead. Consult
  http://api.coala.io/en/latest/coalib.bearlib.languages.html#module-coalib.bearlib.languages.Language
  for usage hints.
- The deprecated ``Lint`` class has now been removed.
- The ``CondaRequirement`` has been removed.
- The ``multiple`` constructor for ``PackageRequirement`` classes has been
  removed.
- A ``deprecate_bear`` decorator is now available so bears can be renamed
  seamlessly.
- The ``Diff`` object has now dedicated functions to ``replace``, ``insert``
  and ``remove`` ``SourceRange`` objects.

Bug Fixes:

- A glob corner case has been fixed.
  (https://github.com/coala/coala/issues/2664)
- An issue where empty patches have been shown to the user has been fixed.
  (https://github.com/coala/coala/issues/2832)
- Wrong handling of periods when changing casing has been fixed.
  (https://github.com/coala/coala/issues/2696)
- A caching bug where results have not been shown to the user has been fixed.
  (https://github.com/coala/coala/issues/2987)

Documentation:

- API documentation is now available at http://api.coala.io/

Internal Changes:

- Deprecated parameters are stored in the function metadata.
- Python builtin logging is now used.
- Numerous changes to get started on https://coala.io/cep5 have been
  implemented. The first aspects are already defined in
  ``coalib.bearlib.aspects`` and bears can already append aspects to results.
- ``coalang`` files now have an alias dictionary.

coala 0.8.1
===========

This bugfix release addressed the following issues:

- The cache will be correctly invalidated when changing section targets now.
  (https://github.com/coala-analyzer/coala/issues/2708)
- Dependencies are resolved before asking the user for needed values. This will
  only affect custom bears that have dependencies that require settings.
  (https://github.com/coala-analyzer/coala/issues/2709)
- PyPrint was updated from 0.2.4 to 0.2.5.
- PipRequirement uses ``sys.executable`` instead of hardcoded python. This will
  only affect coala or bear developers.

coala 0.8.0 - grizzly
=====================

::

                   -
                 `Ns      :s-
            .     mMd`     :Nd.
           :h     /ss/`     +md.
           dN`    :NMMMy`  .ymmy. -+`
           dM+    dMMMMMm`.NMMMMN. +Mo
        `  -sddy: yMMMMMM/+MMMMMMo  dMo
       s/  +MMMMMy.dMMMMM-:MMMMMM+ -yhs`
      .Ms  /MMMMMMo /hdh:  oMMMMh`+MMMMm.
      -MN.  hMMMMMh  `/osssoos+-  dMMMMMs
       oyhho.+mMMm:+dMMMMMMMMMm+  sMMMMMs
       mMMMMMy``` dMMMMMMMMMMMMMh.`sMMMh`
       yMMMMMMy  `MMMMMMMMMMMMMMMMy:..`
       `yMMMMMd  yMMMMMMMMMMMMMMMMMMMMNh+`
         .ohhs-+mMMMMMMMMMMMMMMMMMMMMMMMMd
            .yMMMMMMMMMMMMMMMMMMMMMMMMMMMh
            mMMMMMMMMMMMMMMMMMMMMMMMMMMMh`
            yMMMMMMMMMMMMMMMNhssssyyyso-
             /dMMMMMMMMMNy+.
               ./syhys/-


For this release, we have had 46 developers from around the world contributing
over 150 commits in the last 9 weeks.

Improving the API available for bear writers is one of the areas we've focused
on for this release, with several new and exciting features. General performance
has also been improved heavily with some major changes under the hood. The
documentation has also been worked on, with an emphasis on user-friendliness
and design.

There have also been major internal changes in preparation for the complete
decentralization of bears, which would allow the installation of individual
bears.

Below are some of the important changes introduced for this release:

**New Features**

- coala now supports syntax highlighting in results!

- Questions are now printed in color; this will improve visibility when a lot
  of text is written to the screen.

- ``coala-json`` now supports ``--show-bears`` and ``--filter-by-language``

- Added a ``--show-capabilities`` flag that displays the types of issues coala
  can detect and fix for a particular language.

- Display the line number when a line is missing; this could happen if a bear
  that had run previously overwrites it.

**For Bear Writers**

- Bears now have a new ``REQUIREMENTS`` attribute which will be used to
  automatically resolve bear dependencies. This includes:

  + Native requirements
    (from package managers such as ``apt-get``, ``dnf``, ``pacman``, ...)
  + Conda requirements
  + Python requirements through ``pip3``
  + ``go`` requirements
  + Ruby requirements through ``gem``
  + NodeJS requirements through ``npm``
  + RScript requirements
  + Julia requirements

- Language independent documentation parsing routines: these can be used to
  make bears for linting documentation without having to worry about the
  language.

- ``coalang`` now supports C, C++, CSS, Java, Python3 and Vala.

- A new bear creation tool has been released: with this tool, it's easier than
  ever before to create external linter based bears for coala!

- A new `ASCIINEMA_URL` attribute has been added to bears. This should
  contain an URL to an asciinema video displaying the bear's capabilities in
  action.

- Bear results may now have a ``confidence`` parameter: this is supposed to
  quantify the confidence, on a scale of 1 to 100, the bear has when flagging
  results.

- A ``deprecate_settings`` decorator has been created to deprecate old,
  unsupported bear parameters. Please see
  `here <https://github.com/coala-analyzer/coala/blob/fa8fe22562277762fd73ab3761ad1ec33263839a/coalib/bearlib/__init__.py#L15>`_
  for an example usage.

- ``Code Simplification`` has been added to the set of possible fixes that
  bears can offer.

**Bug Fixes**

- Fixed an issue where errors were generated for lines containing only a
  single tab character. `Issue #2180 <https://github.com/coala-analyzer/coala/issues/2180>`_

- Fixed an issue with question where stray escape characters may be present.
  `Issue #2546 <https://github.com/coala-analyzer/coala/issues/2546>`_

- Group questions about missing values in a coafile by bears.
  `Issue #2530 <https://github.com/coala-analyzer/coala/issues/2530>`_

- An issue where an exception was raised wrongly when the same diff was
  generated multiple times has been fixed.
  `PR #2465 <https://github.com/coala-analyzer/coala/pull/2465>`_

**Performance**

- Caching is now enabled by default. This is a huge performance improvement
  for HDD users - we've seen a 2x improvement when coala is run on coala.
  To disable caching run coala with the ``--disable-caching`` flag.

- An issue where coala takes over 2 seconds to print the help manual through
  ``--help`` has been fixed.
  `Issue #2344 <https://github.com/coala-analyzer/coala/issues/2344>`_

- A small performance improvement from reusing already loaded file contents.

**Documentation**

- A complete overhaul to the README page with a focus on design and
  readability.

- A new `FAQ page <http://docs.coala.io/en/latest/Users/FAQ.html>`_ has
  been created.

- Various other documentation pages have been improved with new resources,
  better explanations, and some corrections.

- The whole documentation has been moved to a
  `separate repository <https://github.com/coala-analyzer/documentation>`__.
  Please file any documentation related issues over there.

**Regressions**

- Dropped Python 3.3 support

**Internal Changes**

- There has been a shift of several modules from coala to
  `coala-utils <https://gitlab.com/coala/coala-utils/>`. This includes the whole
  ``StringProcessing`` library, ``ContextManagers``, and some decorators.

coala 0 7 0 - baloo
===================

::

              ,o8b,         .o88Oo._
             P    d        d8P         .ooOO8bo._
            d'    p        88                  '*Y8bo.
           .Y    ."         YA                      '*Y8b   __
       db, d" _ooQ.dPQ,     YA                        68o68**8Oo.
     .8'  YI.Y"   b   B      "8D                       *"'    "Y8o
    .Y    ;L 8,    Yq.8       Y8     'YB                       .8D
    B .db_.L  q,   q "q       '8               d8'             8D
    8"    qp   8,  8           8       d8888b          d      AY
           8    ",dP           Y,     d888888         d'  _.oP"
           "q    8;             q.    Y8888P'        d8
            '8    b              "q.  `Y88P'       d8"
             'D,  ,8                Y           ,o8P
               'odY'                     oooo888P"

(Release logo by Fabian Neuschmidt)

For this release, 32 people from all over the world have contributed about 200
commits over almost two months.

The focus of this release is certainly on the usability of coala. Usability
testing has made us aware of some important difficulties, users have to face
when trying out coala. We have implemented a lot of countermeasures to lower
this barrier.

The changelog below summarizes the most important user facing changes. Not
listed are especially lots of internal improvements and documentation fixes.

New Features:

- `Shell Autocompletion <http://docs.coala.io/en/latest/Users/Tutorials/Shell_Autocompletion.html>`_
- Patches are shown without prompting the user if small enough, otherwise
  diffstats.
- Bears have metadata and can be browsed. Browse the
  `bear documentation <https://github.com/coala-analyzer/bear-docs>`_
  repository for more information on all the bears.
- Lots of usability improvements! coala will suggest using certain options if
  no meaningful configuration was supplied.
- The help was revamped completely and is way easier to read.
- A ``--verbose`` alias is available for ``-L DEBUG``.
- The ``default_actions`` setting accepts globs for bears now.
- The ``--apply-patches`` argument was added to automatically apply all
  patches.
- coala supports experimental caching. This can lower the run time to a
  fraction of the time needed to perform the full analysis. It will be enabled
  by default in the next release. To use it, invoke coala with
  ``--changed-files``.
- Bear showing is divided into a new set of settings: ``--show-bears`` shows
  all bears, ``--filter-by-language`` allows to filter them, ``--show-details``
  and ``--show-description`` allow changing verbosity of the output.

Feature Removals:

- Tagging was removed.
- ``linter`` does no longer show the executable of the bear by default.

Performance Improvements:

- Globs will be internally cached now so they don't need to be retranslated
  every time. This may show improvements of several seconds when working with
  a large set of files.
- coala supports experimental caching. See ``New Features`` for more
  information.
- coala does not delete ``*.orig`` files on startup anymore. This was a huge
  performance hit especially on HDDs or big file trees. The cleanup can be
  performed manually by running ``coala-delete-orig``. Instead coala will
  keep track of ``*.orig`` files more smartly.

Bugfixes:

- ``**.py`` can again be used instead ``**/*.py``.
- If errors happen before the initialization of logging, tracebacks will be
  shown.

For bear writers:

- Bears can have a number of attributes now, including author information,
  supported languages or categories. A requirements attribute will help
  generating requirements definition files more easily in the future.
- The ``linter`` wrapper provides a ``result_severity`` and a
  ``result_message`` parameter now.
- Bears can now delete and rename files.
- The ``LanguageDefinition`` doesn't need a ``language_family`` anymore to
  load language definitions.
- Results can be created directly from the Bear class more conveniently
  with ``self.new_result(...)``.

coala 0.6.0 - honeybadger
=========================

::

     .o88Oo._                                .".      "     .".
    d8P         .ooOO8bo._                   dPo.    O#O   .oPb
    88                  '*Y8bo.              88o.   .o#o.  .o88
    YA                      '*Y8b   __       Y88o.   .8.  .o88Y
     YA                        68o68**8Oo.    W8888O888888888W
      "8D                       *"'    "Y8o    w8888'88'8888w
       Y8     'YB                       .8D     `o88:88:88o'
       '8               d8'             8D       .O8`88'8O.
        8       d8888b          d      AY        oO8I88I8Oo
        Y,     d888888         d'  _.oP"         oO8|88|Oo
         q.    Y8888P'        d8                 oO8.88.8Oo
          "q.  `Y88P'       d8"                  .oO.88.Oo.
            Y           ,o8P                    .oO888888Oo.
                  oooo888P"                    .oO8      8Oo.
                                               +oO8+    +8Oo+
                                               'bo.      .od'

This release is shaped a lot by working on high quality bear writing tools. Our
codebase has matured further (improved tests, various internal improvements)
and key features for writing and organizing bears were introduced.

Over the last 1.5 months, 22 unique contributors have helped us at the coala
core project.

This time, the release logo is carefully hand crafted by Max Scholz!

New features:

-  Smart globbing: use backslashes without an extra escape now if they don't
   escape delimiters.
-  Results now can have additional information appended.
-  Bears expose information on which languages they support. You can query for
   bears e.g. with ``coala --show-language-bears C++`` for C++.

Bugfixes:

-  Linters suppress the output correctly now when checking for linter
   availability. (https://github.com/coala-analyzer/coala/issues/1888)
-  The result filter algorithms can handle file additions and deletions now.
   (https://github.com/coala-analyzer/coala/issues/1866)
-  Ignore statements without a stop statement are now accepted as well
   (https://github.com/coala-analyzer/coala/issues/2003).

For bear writers:

-  A tutorial for managing bear dependencies is available in our documentation
   now.
-  The Result object has a field ``additional_info`` which can be used to give
   an elaborate description of the problem.
-  A ``typechain()`` function is now available for easy conditional type
   conversion. (https://github.com/coala-analyzer/coala/issues/1859)
-  Bears have a ``name()`` shortcut now which provides the bear class name.
-  A ``get_config_directory()`` function is available that returns the root
   directory of the project guessed by coala or provided (overridden) by the
   user.
-  A new ``linter`` decorator makes it even easier to write new linter
   wrappers. (https://github.com/coala-analyzer/coala/issues/1928)

Notable internal/API changes:

-  ``FunctionMetadata`` has a new ``merge`` function that can be used to merge
   function signatures and documentation comments.

coala 0.5.0 - joey
==================

::

     .o88Oo._
    d8P         .ooOO8bo._
    88                  '*Y8bo.
    YA                      '*Y8b   __
     YA                        68o68**8Oo.
      "8D                       *"'    "Y8o
       Y8     'YB                       .8D
       '8               d8'             8D
        8       d8888b          d      AY
        Y,     d888888         d'  _.oP"
        ,q.    Y8888P'        d8,
        d "q.  `Y88P'       d8" b
        Y,   Y           ,o8P  ,Y
        8q.       oooo888P"   .p8
        8 "qo._           _.op" 8
        8   '"P8866ooo6688P"'   8
        8                       8
        8                       8
        8.                     .8
        "b                     d"
        'b                     d'
         8                     8
         q.                   .p
          q.                 .p
          "qo._           _.op"
            '"P8866ooo6688P"'

With this release we declare coala proudly as beta. Most features are now
available and coala is ready for daily use.

All bears have been moved out of coala into the ``coala-bears`` package. If you
want to develop bears for coala, you can now install it without the bears just
as before. If you want to use the coala official bears, make sure to install the
``coala-bears`` package and if needed follow the instructions to install linters
needed by the bears for your language.

According to ``git shortlog -s -n 5fad168..`` 56 people contributed to this
release. We sadly cannot name all the new coalaians here but every single
one of them helped making coala as awesome and polished as it is today.

New features:

-  ``--no-config`` allows to ignore existing coafiles in the current directory.
   (https://github.com/coala-analyzer/coala/issues/1838)
-  In-file ignore directives now support globs.
   (https://github.com/coala-analyzer/coala/issues/1781)
-  ``coala-json`` supports the ``--relpath`` argument so the JSON output can be
   moved to other systems reasonably.
   (https://github.com/coala-analyzer/coala/issues/1593)
-  ``--bear-dirs`` are now searched recursively. They are also added to the
   Python PATH so imports relative to a given bear directory work.
   (https://github.com/coala-analyzer/coala/issues/1711,
   https://github.com/coala-analyzer/coala/issues/1712)
-  ``coala-format`` exposes the ``{severity_str}`` so you can get a human
   readable severity in your self formatted result representation.
   (https://github.com/coala-analyzer/coala/issues/1313)
-  Spaces and tabs are highlighted in the CLI to make whitespace problems
   obvious. (https://github.com/coala-analyzer/coala/issues/606)
-  Actions that are not applicable multiple times are not shown after applying
   them anymore. (https://github.com/coala-analyzer/coala/issues/1064)
-  Documentation about how to add coala as a pre-commit hook has been added:
   http://docs.coala.io/en/latest/Users/Git_Hooks.html
-  Actions emit a success message now that is shown to the user and improves
   usability and intuitivity of actions.
-  A warning is emitted if a bear or file glob does not match any bears or
   files.
-  ``coala-json`` supports now a ``--text-logs`` argument so you can see your
   logs in realtime, outside the JSON output if requested. You can output the
   JSON output only into a file with the new ``-o`` argument.
   (https://github.com/coala-analyzer/coala/issues/847,
   https://github.com/coala-analyzer/coala/issues/846)
-  ``coala-ci`` yields a beautiful output now, showing the issues
   non-interactively. (https://github.com/coala-analyzer/coala/issues/1256)
-  A ``coala-delete-orig`` script is now available to delete autogenerated
   backup files which were created when a patch was applied. This is called
   automatically on every coala run.
   (https://github.com/coala-analyzer/coala/issues/1253)
-  The ``--limit-files`` CLI argument was introduced which is especially useful
   for writing performant editor plugins.

Exitcode changes:

-  coala returns ``5`` if patches were applied successfully but no other results
   were yielded, i.e. the code is correct after the execution of coala but was
   not before.
-  coala returns ``4`` now if executed with an unsupported python version.

Bugfixes:

-  The ``appdirs`` module is now used for storing tagged data.
   (https://github.com/coala-analyzer/coala/issues/1805)
-  Package version conflicts are now handled with own error code ``13``.
   (https://github.com/coala-analyzer/coala/issues/1748)
-  Previously inputted values for actions are not stored any more if the action
   fails.
   (https://github.com/coala-analyzer/coala/issues/1825)
-  coala doesn't crash any more on Windows when displaying a diff. Happened due
   to the special chars used for whitespace-highlighting Windows terminals do
   not support by default.
   (https://github.com/coala-analyzer/coala/issues/1832)
-  Escaped characters are written back to the ``.coafile`` correctly.
   (https://github.com/coala-analyzer/coala/issues/921)
-  ``coala-json`` doesn't show logs when invoked with ``-v`` or ``-h`` anymore
   (https://github.com/coala-analyzer/coala/issues/1377)
-  Keyboard interrupts are handled more cleanly.
   (https://github.com/coala-analyzer/coala/issues/871)
-  Tagging will only emit a warning if the data directory is not writable
   instead of erroring out.
   (https://github.com/coala-analyzer/coala/issues/1050)
-  Unicode handling has been improved.
   (https://github.com/coala-analyzer/coala/issues/1238)
-  Cases where ``--find-config`` has not found the configuration correctly have
   been resolved. (https://github.com/coala-analyzer/coala/issues/1246)
-  Some cases, where result ignoring within files didn't work have been
   resolved. (https://github.com/coala-analyzer/coala/issues/1232)

For bear writers:

-  A new built-in type is available from ``Setting`` for using inside ``run()``
   signature: ``url``.
-  ``Lint`` based bears have a new argument which can be set to test whether a
   command runs without errors. This can be used to check for example the
   existence of a Java module.
   (https://github.com/coala-analyzer/coala/issues/1803)
-  The ``CorrectionBasedBear`` and ``Lint`` class have been merged into the new
   and more powerful ``Lint`` class to make linter integration even easier. It
   also supports you if you need to generate an actual configuration file for
   your linter.
-  ``LocalBearTestHelper`` as well as the ``verify_local_bear`` have been
   revamped to make it even easier to test your bears and debug your tests.
-  File dictionaries are now given as tuples and are thus not modifiable.
-  A number of new tutorials about bear creation have been written.
-  Bears can now be registered at coala and thus be distributed as own packages.

Notable internal changes:

-  API documentation is now available at
   http://api.coala.io
-  coala switched to PyTest. Our old own framework is no longer maintained.
   (https://github.com/coala-analyzer/coala/issues/875)
-  As always loads of refactorings to make the code more stable, readable and
   beautiful!
-  The main routines for the coala binaries have been refactored for less
   redundancy. If you are using them to interface to coala directly, please
   update your scripts accordingly.
-  Loads of new integration tests have been written. We're keeping our 100% test
   coverage promise even for all executables now.

coala 0.4.0 - eucalyptus
========================

::

        88        .o88Oo._
       8 |8      d8P         .ooOO8bo._
      8  | 8     88                  '*Y8bo.
      8\ | /8    YA                      '*Y8b   __
     8  \|/ 8     YA                        68o68**8Oo.
     8\  Y  8      "8D                       *"'    "Y8o
     8 \ | /8       Y8     'YB                       .8D
    8   \|/ /8     '8               d8'             8D
    8\   Y / 8       8       d8888b          d      AY
    8 \ / /  8       Y,     d888888         d'  _.oP"
    8  \|/  8         q.    Y8888P'        d8
    8   Y   8          "q.  `Y88P'       d8"
     8  |  8             Y           ,o8P
      8 | 8                    oooo888P"

New features:

-  Auto-apply can be enabled/disabled through the ``autoapply`` setting
   in a coafile.
-  Auto-applied actions print the actual file where something happened.
-  A new bear was added, the GitCommitBear! It allows to check your
   current commit message at HEAD from git!
-  Filenames of results are now printed relatively to the execution
   directory. (https://github.com/coala-analyzer/coala/issues/1124)

Bugfixes:

-  coala-json outputted results for file-ranges that were excluded.
   (https://github.com/coala-analyzer/coala/issues/1165)
-  Auto-apply actions that failed are now marked as unprocessed so the
   user can decide manually what he wants to do with them.
   (https://github.com/coala-analyzer/coala/issues/1202)
-  SpaceConsistencyBear: Fixed misleading message when newline at EOF is
   missing. (https://github.com/coala-analyzer/coala/issues/1185)
-  Results from global bears slipped through our processing facility.
   Should not happen any more.

coala 0.3.0 - platypus
======================

We are dropping Python 3.2 support (and so PyPy). Also we are removing
translations, the default language is English.

This release contains these following feature changes:

-  Auto-apply feature added! Results can directly be processed without
   user interaction specifying the desired action!
-  A missing coafile that is explicitly wanted through the ``--config``
   flag throws an error instead of a warning. Only default coafile names
   (ending with ``.coafile``) raise a warning.
-  Various new bears integrating existing linter tools, e.g. for C/C++,
   Python, Ruby, JSON and many more!
-  Allow to ignore files inside the coafile.
-  Results can now be stored and tagged with an identifier for accessing
   them later.
-  OpenEditorAction lets the user edit the real file instead of a
   temporary one.
-  All usable bears can now be shown with ``--show-all-bears``.
-  Only ``#`` is supported for comments in the configuration file
   syntax.
-  Multiple actions can now be executed on the CLI.
-  Patches can now be shown on the CLI.
-  A ``coala-format`` binary was added that allows customized formatting
   for results to ease integration in other systems.
-  Printing utilities have moved into the PyPrint library.

Bear API changes:

-  A bear can implement ``check_prerequisites`` to determine whether it
   can execute in the current runtime.
-  The PatchResult class was merged into the Result class.

Bear changes:

-  SpaceConsistencyBear offers more verbose and precise information
   about the problem.

coala 0.2.0 - wombat
====================

::

     .o88Oo._
    d8P         .ooOO8bo._
    88                  '*Y8bo.
                          '*Y8b   __
     YA                        68o68**8Oo.     _.o888PY88o.o8
      "8D                       *"'    "Y8o.o88P*'         Y.
       Y8     'YB                       .8D                 Y.
       '8               d8'             8D             o     8
        8       d8888b          d      AY   o               d'
        Y,     d888888         d'  _.oP"         d88b       8
         q.    Y8888P'        d8       Y,       d8888       P
          "q.  `Y88P'       d8"         q.      Y888P     .d'
             Y           ,o8P            "q      `"'    ,oP
                  oooo888P"               `Y         .o8P"
                                              8ooo888P"

This release features the following feature changes:

-  ``--find-config`` flag: Searches for .coafile in all parent
   directories.
-  Add code clone detection bears and algorithms using CMCD approach.
-  Console color gets properly disabled now for non-supporting platforms
   (like Windows).
-  coala results can be outputted to JSON format using the
   ``coala-json`` command.
-  Automatically add needed flags to open a new process for some
   editors.
-  Save backup before applying actions to files.
-  Return nonzero when erroring or yielding results.
-  Write newlines before beginning new sections in coafiles when
   appropriate.
-  The default\_coafile can now be used for arbitrary system-wide
   settings.
-  coala can now be configured user-wide with a ~/.coarc configuration
   file.
-  Manually written documentation is now hosted at http://coala.rtfd.org/.
-  Changed logging API in Bears (now: debug/warn/err).
-  clang python bindings were added to the bearlib.
-  Exitcodes were organized and documented.
   (http://docs.coala.io/en/latest/Users/Exit_Codes.html)
-  Handling of EOF/Keyboard Interrupt was improved.
-  Console output is now colored.
-  Bears can now easily convert settings to typed lists or dicts.
-  Bears have no setUp/tearDown mechanism anymore.
-  Colons cannot be used for key value separation in configuration files
   anymore as that clashes with the new dictionary syntax. Use ``=``
   instead.
-  The ``--job-count`` argument was removed for technical reasons. It
   will be re-added in the near future.
-  A ``--show-bears`` parameter was added to get meta information of
   bears.
-  The coala versioning scheme was changed to comply PEP440.
-  ``coala --version`` now gives the version number. A released ``dev``
   version has the build date appended, 0 for local versions installed
   from source.
-  A ``coala-dbus`` binary will now be installed that spawns up a dbus
   API for controlling coala. (Linux only.)
-  The StringProcessing library is there to help bear writers deal with
   regexes and similar things.
-  A new glob syntax was introduced and documented.
   (http://docs.coala.io/en/latest/Users/Glob_Patterns.html)
-  The ``--apply-changes`` argument was removed as its concept does not
   fit anymore.
-  Bears can now return any iterable. This makes it possible to
   ``yield`` results.

New bears:

-  ClangCloneDetectionBear
-  LanguageToolBear
-  PyLintBear

Infrastructural changes:

-  Tests are executed with multiple processes.
-  Branch coverage raised to glorious 100%.
-  We switched from Travis CI to CircleCI as Linux CI.
-  AppVeyor (Windows CI) was added.
-  Travis CI was added for Mac OS X.
-  Development releases are automatically done from master and available
   via ``pip3 install coala --pre``.
-  Rultor is now used exclusively to push on master. Manual pushes to
   master are no longer allowed to avoid human errors. Rultor deploys
   translation strings to Zanata and the PyPI package before pushing the
   fast-forwarded master.

Internal code changes:

-  Uncountable bugfixes.
-  Uncountable refactorings touching the core of coala. Code has never
   been more beautiful.

We are very happy that 7 people contributed to this release, namely
Abdeali Kothari, Mischa Krüger, Udayan Tandon, Fabian Neuschmidt, Ahmed
Kamal and Shivani Poddar (sorted by number of commits). Many thanks go
to all of those!

coala's code base has grown sanely to now over 12000 NCLOC with almost
half of them being tests.

We are happy to announce that Mischa Krüger is joining the maintainers
team of coala.

Furthermore we are happy to announce basic Windows and Mac OS X support.
This would not have been possible without Mischa and Abdeali. coala is
fully tested against Python 3.3 and 3.4 on Windows and 3.2, 3.3, 3.4 and
Pypy3 on Mac while not all builtin bears are tested. coala is also
tested against Pypy3 and Python 3.5 beta (in addition to 3.3 and 3.4) on
Linux.

coala 0.1.1 alpha
=================

This patch release fixes a major usability issue where data entered into
the editor may be lost.

For more info, see release 0.1.0.

coala 0.1.0 alpha
=================

Attention: This release is old and experimental.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

coala 0.1 provides basic functionality. It is not feature complete but
already useful according to some people.

For information about the purpose of coala please look at the README
provided with each source distribution.

Note that this is a prerelease, thus this release will be supported with
only important bugfixes for limited time (at least until 0.2.0 is
released). Linux is the only supported platform.

Documentation for getting started with coala is provided here:
https://github.com/coala-analyzer/coala/blob/v0.1.0-alpha/TUTORIAL.md

If you want to write static code analysis routines, please check out
this guide:
https://github.com/coala-analyzer/coala/blob/v0.1.0-alpha/doc/getting\_involved/WRITING\_NATIVE\_BEARS.md

We love bugs - if you find some, be sure to share them with us:
https://github.com/coala-analyzer/coala/issues
