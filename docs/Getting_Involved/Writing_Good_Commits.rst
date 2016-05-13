Introduction
============

At *coala* we are looking heavily at the maintainability of the code.

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
---------------------------------

A commit message consists of 3 parts - The shortlog (short description),
the long description and the issue reference. There should have an empty
line between each section.

::

    This is the shortlog - one line only

    This is the long description which can extend to multiple lines
    of text.

    And can have multiple paragraphs which explain things in more
    detail too.

    Next is the issue reference

Shortlog
~~~~~~~~

Example:

::

    setup: Install .coafile via package_data

-  Maximum of 50 characters.
-  Should describe the *change* - the action being done in the commit.
-  Should have a tag and and a short description separated by a colon (``:``)

   -  **Tag**

      -  The file or class or package being modified.
      -  Not mandatory.

   -  **Short Description**

      - Starts with a capital letter.
      - Written in imperative present tense (i.e. ``Add something``, not
        ``Adding something`` or ``Added something``).
      - No trailing period.

Long Description
~~~~~~~~~~~~~~~~

Example:

::

    When installing the .coafile to distutils.sysconfig.get_python_lib, we
    ignore that this is not the installation directory in every case. Thus
    it is easier, more reliable and platform independent to let distutils
    install it by itself.

-  Maximum of 72 chars excluding newline for *each* line.
-  Not mandatory - but helps explain what you're doing.
-  Should describe the reasoning for your changes. This is especially
   important for complex changes that are not self explanatory. This is also
   the right place to write about related bugs.

Issue reference
~~~~~~~~~~~~~~~

Example:

::

    Fixes https://github.com/coala-analyzer/coala/issues/269

-  Should use the ``Fixes`` keyword.
-  Should use full URL to the issue.
-  There should be a single space between the ``Fixes`` and the URL.

.. note::

    -  The issue reference will automatically add the link of the commit in
       the issue.
    -  It will also automatically close the issue when the commit is
       accepted into *coala*.

.. seealso::

    https://wiki.gnome.org/Git/CommitMessages

Example
~~~~~~~
Example 1:
::

    setup: Install .coafile via package_data

    When installing the .coafile to distutils.sysconfig.get_python_lib, we
    ignore that this is not the installation directory in every case. Thus
    it is easier, more reliable and platform independent to let distutils
    install it by itself.

    Fixes https://github.com/coala-analyzer/coala/issues/269

Example 2:
::

    Readme: Fix typo begining -> beginning

    Fix a minor typo in the file for better readability.

    Fixes https://github.com/coala-analyzer/coala/issues/xxx

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
