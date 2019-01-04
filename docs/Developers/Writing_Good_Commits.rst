How To Write a Good Commit Message
==================================

Quick reference
---------------

Example of a good commit:

We are looking at pull request `#5759 <https://github.com/coala/coala/pull/5759>`_

::

    Haskell.py: Add Haskell.py file

    Add a new python file in
    coalib/bearlib/languages/definitions/Haskell.py

    Closes https://github.com/coala/coala/issues/5330

- `Haskell.py: Add Haskell.py file`: Describe the change in
   maximum of 50 characters.

- `Add a new python file in.. ..Haskell.py`: Describe the reasoning
   of your changes in maximum of 72 characters per line.

- `Closes https://github.com/coala/coala/issues/5330`: Mention the URL
   of the issue it closes or fixes.

We are now looking at pull request `#5789 <https://github.com/coala/coala/pull/5789>`_

::

    ConfParserTest.py: Fix typos in comments

    This fixes multiple occurences of typos in the comments
    omment --> comment
    inexistent --> non-existent

    Closes https://github.com/coala/coala/issues/5785

- `ConfParserTest.py: Fix typos in comments`: Describe the change in
   maximum of 50 characters.

   For clarity, it is good to notice that the shortlog of this example
   says "Fix". However, this isn't an actual bug fix, it did not resolve
   a bug nor is it labeled as a bug on GitHub, like the pull request in
   "Example 3 (fixed typo)" which you can see further down. That being
   said, it was acceptable to use the term "Fix" in this instance.

- `This fixes.. ..non-existent`: Describe the reasoning of your changes
   in maximum of 72 characters per line.

- `Closes https://github.com/coala/coala/issues/5785`: Mention the URL
   of the issue it closes or fixes.


At coala, we are looking heavily at the maintainability of the code.

.. note::

    Code is more often read than written!

We need good code and for achieving it, we ensure that every
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

    Haskell.py: Add Haskell.py file

    Add a new python file in coalib/bearlib/languages/definitions/Haskell.py

    Closes https://github.com/coala/coala/issues/5330

Shortlog
~~~~~~~~

Example:

::

    Haskell.py: Add Haskell.py file

.. _50:

-  | Maximum of 50 characters.
   | Keeping subject lines at this length ensures that they are
     readable, and explains the change in a concise way.
-  Should describe the *change* - the action being done in the commit.
-  Should not include WIP prefix.
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

    Add a new python file in coalib/bearlib/languages/definitions/Haskell.py

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

    Closes https://github.com/coala/coala/issues/5330

-  Should use the ``Fixes`` keyword if your commit fixes a bug, or ``Closes``
   if it adds a feature/enhancement.
-  In some situations, e.g. bugs overcome in documents, the difference
   between ``Fixes`` and ``Closes`` may be very small and subjective.
   If a specific issue may lead to an unintended behaviour from the user
   or from the program it should be considered a bug, and should be
   addresed with ``Fixes``. If an issue is labelled with ``type/bug``
   you should always use ``Fixes``. For all other issues use ``Closes``.
-  In case your commit does not close an issue but it is related to
   the issue and partly solves the problem, use ``Related to`` instead
   of ``Fixes`` or ``Closes``.
-  Should use full URL to the issue.
-  There should be a single space between the ``Fixes``, ``Closes`` or
   ``Related to`` and the URL.

.. note::

    -  The issue reference will automatically add the link of the commit in
       the issue.
    -  It will also automatically close the issue when the commit is
       accepted into coala.

.. seealso::

    https://wiki.gnome.org/Git/CommitMessages

More Examples
~~~~~~~~~~~~~

Example 1 (fixed bug and added enhacement):
Pull request `#4217 <https://github.com/coala/coala/pull/4217>`_

::

    Diff.py: Remove has_changes and fix __bool__

    Removes the self.has_changes property, since its functionality can be
    accessed from the bool conversion.
    Fixes inconstency of __bool__ that results from looking at
    self._changes:
    removing one line, then adding the same content again resulted in
    bool(diff) == True, instead of False.

    __bool__ now uses the mechanism that was employed by has_changes, to
    fix this bug.

    Closes https://github.com/coala/coala/issues/4178

Example 2 (implemented feature):
Pull request `#435 <https://github.com/coala/projects/pull/435>`_

::

    Update the CI1, CI2 , & CI3 tasks to refer to 2017

    This commit changes all occurrences of 2016 to 2017 and the project
    links with the new ones in use_coala.md, use_coala_2.md and
    use_coala_3.md.

    Closes https://github.com/coala/projects/issues/433

Example 3 (fixed typo):
Pull request `#5544 <https://github.com/coala/coala/pull/5544>`_

::

    Language: Change `TrumpScript` aliases

    This changes aliases of TrumpScript in the
    doctests so that TypeScript and TrumpScript
    have different aliases and so do not collide.

    Fixes https://github.com/coala/coala/issues/5541

Example 4 (related to):
Pull request `#5624 <https://github.com/coala/coala/pull/5624>`_

::

    .moban.yaml: Add cached_property

    This was omitted from 54622c2.

    Related to https://github.com/coala/coala/pull/5618

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
