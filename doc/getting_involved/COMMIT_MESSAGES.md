COMMIT MESSAGES
===============

There are a few things to consider when writing a commit message, namely:

 * The first line may hold up to 50 chars excluding newline and is called
   shortlog.
 * The shortlog should have a tag and must have a short description:
   `tag: Short description`.
   * The tag is usually the affected class or package and not mandantory.
   * The short description starts with a big letter and is written in present
     tense.
 * The second line must be empty.
 * All following lines may hold up to 72 chars excluding newline.
   * These lines are the long description. The long description is not
     mandantory but may help expressing what you're doing.
 * The commit message shall describe the _change_ as exactly as possible. If it
   is a bugfix, don't describe the bug but the _change_, especially in the
   shortlog.
 * If the commit fixes a bug, add the following line at the end:
   `Fixes: https://github.com/coala-analyzer/coala/issues/###`, this way the
   commit will appear at the bug and several revisions can be tracked this way.

Structural example:
```
tag: Short description

A more elaborate description. Optionally:

See: https://github.com/coala-analyzer/coala/issues/###
Fixes: https://github.com/coala-analyzer/coala/issues/###
```
