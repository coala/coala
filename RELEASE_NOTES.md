# coala 0.2.0 (WORK IN PROGRESS)

This release features the following new features:

 * Automatically add needed flags to open a new process for some editors.
 * Save backup before applying actions to files.
 * Return nonzero when erroring or yielding results.
 * Write newlines before beginning new sections in coafiles when appropriate.
 * The default_coafile can now be used for arbitrary system-wide settings.
 * coala can now be configured user-wide with a ~/.coarc configuration file.

Additionally many bugfixes and code improvements have been done.

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
