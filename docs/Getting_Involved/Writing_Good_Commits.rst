Introduction
============

At coala we are looking heavily at the maintainability of the code.

    Code is more often read than written!

It is obvious that we need good code. In order to do that we are
verifying that every change to our code (i.e. the commits) is making it
better.

What Makes a Good Commit
------------------------

A good commit is atomic. It describes but only one logical change and
not more. Why do we do that? Because we find more bugs if we do! Also it
features a good commit message.

How to Write Good Commit Messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are a few things to consider when writing a commit message,
namely:

-  The first line may hold up to 50 chars excluding newline and is
   called shortlog.
-  The shortlog should have a tag and must have a short description:
   ``tag: Short description``.
-  The tag is usually the affected class or package and not mandatory.
   It gives context to the commit.
-  The short description starts with a big letter and is written in
   imperative present tense (i.e. ``Add something``, not
   ``Adding something`` or ``Added something``). It has no trailing
   period.
-  The second line must be empty.
-  All following lines may hold up to 72 chars excluding newline.
-  These lines are the long description. The long description is not
   mandatory but may help expressing what you're doing.
-  The shortlog shall describe the *change* as exactly as possible. If
   it is a bugfix, don't describe the bug but the *change*.
-  In the long description you can add reasoning for your changes. This
   is especially important for complex changes that are not self
   explanatory. This is also the right place to explain related bugs.
-  If the commit fixes a bug, add the following line at the end:
   ``Fixes https://github.com/coala-analyzer/coala/issues/###``, this
   way the commit will appear at the bug and several revisions can be
   tracked this way.
-  Be sure to use the full URL, if we move from github, the links should
   still work.
-  This will automatically close the according bug when pushed to master
   if you have the permissions on GitHub.

Also see: https://wiki.gnome.org/Git/CommitMessages

Example
~~~~~~~

::

    setup: Install .coafile via package_data

    When installing the .coafile to distutils.sysconfig.get_python_lib, we
    ignore that this is not the installation directory in every case. Thus
    it is easier, more reliable and platform independent to let distutils
    install it by itself.

    Fixes https://github.com/coala-analyzer/coala/issues/269

Why Do We Need Good Commits?
----------------------------

-  An atomic commit is way easier to review. The reviewer thus will be
   able to review faster and find more bugs due to the lower complexity
   of the change.
-  Atomic commits are like good objects in object oriented programming -
   you can split up a bigger thing into many small objects. Reducing
   complexity is the key to developing good software and finding its bug
   before they occur.
-  Good commit messages make it easy to check at a glance what happened
   in a time range.
-  It is way easier to revert single changes without side effects.
   Reverting multiple commits at a time is easy, reverting a part of a
   commit is not.
-  ``git blame`` will be much more effective. It is the best
   documentation you can get. The older your code is, the more
   documentation it has. The better the commit messages are, the better
   is your hidden documentation. Your commit messages document the
   reason for every single change you did to any line.
-  ``git bisect`` will be much more effective. If you bisect through
   atomic commits to find the commit which caused a bug, you should be
   able to identify the real cause of the bug fastly. Good commit
   messages and atomicity of commits are key to that ability.
