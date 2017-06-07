How To Write a Good Commit Message
==================================

Quick reference
---------------

Example of a good commit:

::

    setup.py: Change bears' entrypoint

    This entrypoint ensures that coala discovers
    the bears correctly.
    It helps not writing more functions inside
    ``coalib`` for this.

    Closes https://github.com/coala/coala/issues/5861

- `setup.py: Change bears' entrypoint`: Describe the change in
   maximum of 50 characters.

- `This entrypoint.. ..for this`: Describe the reasoning of your changes
   in maximum of 72 characters per line.

- `Closes https://github.com/coala/coala/issues/5861`: Mention the URL
   of the issue it closes or fixes.

At coala we are looking heavily at the maintainability of the code.

.. note::

    Code is more often read than written!

We need good code. In order to do that we are verifying that every
change to our code (i.e. the commits) is making it better.

What Makes a Good Commit
------------------------

A good commit is atomic. It should describe one change and not more.

Why? Because we may create more bugs if we had more changes per commit.

How to Write Good Commit Messages
---------------------------------

A commit message consists of 3 parts:

- shortlog
- commit body
- issue reference

Example:

::

    setup.py: Change bears' entrypoint

    This entrypoint ensures that coala discovers the bears correctly.
    It helps not writing more functions inside ``coalib`` for this.

    Closes https://github.com/coala/coala/issues/5861

Shortlog
~~~~~~~~

Example:

::

    setup.py: Change bears' entrypoint

.. _50:

-  | Maximum of 50 characters.
   | Keeping subject lines at this length ensures that they are
     readable, and explains the change in a concise way.
-  Should describe the *change* - the action being done in the commit.
-  Should have a tag and a short description separated by a colon (``:``)

   -  **Tag**

      -  The file or class or package being modified.
      -  Not mandatory.

   -  **Short Description**

      - Starts with a capital letter.
      - Written in imperative present tense (i.e. ``Add something``, not
        ``Adding something`` or ``Added something``).
      - No trailing period.

Commit Body
~~~~~~~~~~~

Example:

::

    This entrypoint ensures that coala discovers the bears correctly.
    It helps not writing more functions inside ``coalib`` for this.

.. _72:

-  | Maximum of 72 chars excluding newline for *each* line.
   | The recommendation is to add a line break at 72 characters,
     so that Git has plenty of room to indent text while still
     keeping everything under 80 characters overall.
-  Not mandatory - but helps explain what you're doing.
-  Should describe the reasoning for your changes. This is especially
   important for complex changes that are not self explanatory. This is also
   the right place to write about related bugs.
-  First person should not be used here.

The bot will complain if the 50_/72_ rule is not followed.

Issue reference
~~~~~~~~~~~~~~~

Example:

::

    Fixes https://github.com/coala/coala/issues/5861

-  Should use the ``Fixes`` keyword if your commit fixes a bug, or ``Closes``
   if it adds a feature/enhancement.
-  In some situations, e.g. bugs overcome in documents, the difference
   between ``Fixes`` and ``Closes`` may be very small and subjective.
   If a specific issue may lead to an unintended behaviour from the user
   or from the program it should be considered a bug, and should be
   addresed with ``Fixes``.
-  Should use full URL to the issue.
-  There should be a single space between the ``Fixes`` or ``Closes`` and the
   URL.

.. note::

    -  The issue reference will automatically add the link of the commit in
       the issue.
    -  It will also automatically close the issue when the commit is
       accepted into coala.

.. seealso::

    https://wiki.gnome.org/Git/CommitMessages

More Examples
~~~~~~~~~~~~~

Example 1 (fixed bug):

::

    setup: Install .coafile via package_data

    When installing the .coafile to distutils.sysconfig.get_python_lib, we
    ignore that this is not the installation directory in every case. Thus
    it is easier, more reliable and platform independent to let distutils
    install it by itself.

    Fixes https://github.com/coala/coala/issues/269

Example 2 (implemented feature):

::

    Linter: Output command on debug

    This massively helps debugging linters.

    Closes https://github.com/coala/coala/issues/2060

Editing Commit Messages
-----------------------

If you have previously made a commit and update it on a later date,
it is advisable to also update the commit message accordingly.

In order to do this one can use the amend function as is described `here.
<http://api.coala.io/en/latest/Developers/Git_Basics.html#follow-up>`_

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
