# coala 0.2.0 (WORK IN PROGRESS)

This release features the following feature changes:

 * Automatically add needed flags to open a new process for some editors.
 * Save backup before applying actions to files.
 * Return nonzero when erroring or yielding results.
 * Write newlines before beginning new sections in coafiles when appropriate.
 * The default_coafile can now be used for arbitrary system-wide settings.
 * coala can now be configured user-wide with a ~/.coarc configuration file.
 * Manual written documentation is now hosted at http://coala.rtfd.org/.
 * Changed logging API in Bears (now: debug/warn/err).
 * clang python bindings were added to the bearlib.
 * ClangCodeCloneDetection bear was added.
 * Exitcodes were organized and documented.
   (http://coala.readthedocs.org/en/latest/Exit_Codes/)
 * Handling of EOF/Keyboard Interrupt was improved.
 * Console output is now colored.
 * Bears can now easily convert settings to typed lists or dicts.
 * Bears have no setUp/tearDown mechanism anymore.
 * Colons cannot be used for key value seperation in configuration files
   anymore as that clashes with the new dictionary syntax. Use `=` instead.
 * The `--job-count` argument was removed for technical reasons. It will be
   re-added in the near future.
 * A `--show-bears` parameter was added to get metainformation of bears.
 * The coala versioning scheme was changed to comply PEP440.
 * `coala --version` now gives the version number. A `dev` version has the
   build number appended, 0 means locally from source.
 * A `coala-dbus` binary will now be installed that spawns up a dbus API for
   controlling coala. (Linux only.)
 * The StringProcessing libary is there to help bear writers deal with regexes
   and similar things.
 * A new glob syntax was introduced and documented.
   (http://coala.readthedocs.org/en/latest/Glob_Patterns/)

Infrastructural changes:

 * Tests are executed with multiple processes.
 * Branch coverage raised to glorious 100%.
 * We switched from Travis CI to CircleCI.
 * AppVeyor (Windows CI) was added.
 * Development releases are automatically done from master and available via
   `pip install coala --pre`.
 * Rultor is now used exclusively to push on master. Manual pushes to master
   are not longer allowed to avoid human errors.

Internal code changes:

 * Uncountable bugfixes.
 * Uncountable refactorings touching the core of coala. Code has never been
   more beautiful.

We are very happy that 7 people contributed to this release, namely Abdeali
Kothari, Mischa Krüger, Udayan Tandon, Fabian Neuschmidt, Ahmed Kamal and
Shivani Poddar (sorted by number of commits). Many thanks go to all of those!

coala's code base has grown sanely to now over 12000 NCLOC with almost half of
them being tests.

We are happy to announce that Mischa Krüger is joining the maintainers team of
coala.

Furthermore we are happy to announce basic windows support. This would not
have been possible without Mischa. coala is fully tested against python 3.3
and 3.4 on windows while not all builtin bears are.

# coala 0.1.1 alpha

This patch release fixes a major usability issue where data entered into the
editor may be lost.

For more info, see release 0.1.0.

# coala 0.1.0 alpha

### Attention: This release is old and experimenental.

coala 0.1 provides basic functionality. It is not feature complete but already
useful according to some people.

For information about the purpose of coala please look at the README provided
with each source distribution.

Note that this is a prerelease, thus this release will be supported with only
important bugfixes for limited time (at least until 0.2.0 is released). Linux
is the only supported platform.

Documentation for getting started with coala is provided here:
https://github.com/coala-analyzer/coala/blob/v0.1.0-alpha/TUTORIAL.md

If you want to write static code analysis routines, please check out this guide:
https://github.com/coala-analyzer/coala/blob/v0.1.0-alpha/doc/getting_involved/WRITING_BEARS.md

We love bugs - if you find some, be sure to share them with us:
https://github.com/coala-analyzer/coala/issues
