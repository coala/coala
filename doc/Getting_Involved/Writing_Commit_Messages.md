Commit Messages
===============

There are a few things to consider when writing a commit message, namely:

 * The first line may hold up to 50 chars excluding newline and is called
   shortlog.
 * The shortlog should have a tag and must have a short description:
   `tag: Short description`.
   * The tag is usually the affected class or package and not mandantory.
   * The short description starts with a big letter and is written in
     imperative present tense (i.e. `Add something`, not `Adding something` or
     `Added something`).
 * The second line must be empty.
 * All following lines may hold up to 72 chars excluding newline.
   * These lines are the long description. The long description is not
     mandantory but may help expressing what you're doing.
 * The commit message shall describe the _change_ as exactly as possible. If it
   is a bugfix, don't describe the bug but the _change_, especially in the
   shortlog.
 * If the commit fixes a bug, add the following line at the end:
   `Fixes https://github.com/coala-analyzer/coala/issues/###`, this way the
   commit will appear at the bug and several revisions can be tracked this way.
   * Be sure to use the full URL, if we move from github, the links should
     still work.
   * This will automatically close the according bug when pushed to master.

Also see: https://wiki.gnome.org/Git/CommitMessages

Example:
```
setup: Install .coafile via package_data

When installing the .coafile to distutils.sysconfig.get_python_lib, we
ignore that this is not the installation directory in every case. Thus
it is easier, more reliable and platform independent to let distutils
install it by itself.

Fixes https://github.com/coala-analyzer/coala/issues/269
```
