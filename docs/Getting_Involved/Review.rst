Reviewing
=========

This document is a guide to *coala*'s review process. It will be extended
over time.

Review Process
--------------

The review process for *coala* is as follows:

1. Anyone can submit commits for review. This usually happens on WIP
   branches, submitting goes via GitHub Pull Requests.
2. A reviewer reviews every commit by its own and validates that every
   commit is a good change and does not destroy anything.
3. If a commit does not fulfill the expectations of the reviewer, go to
   step one.
4. If the commits are not linearly mergeable into master, rebase and go
   to step one.
5. All commits are acknowledged and fit linearly onto master. All
   continuous integration services (as described below) pass. Anyone
   with collaborator permission may leave the ``@rultor merge`` command
   to get the PR merged automatically.

Continous Integration
---------------------

It is only allowed to merge a pull request into master if all of the
following apply:

-  The build/tests pass on all services. (circleci, appveyor)
-  Scrutinizer shows passed. (That is: no new issues, no new classes
   with rating D or worse, project quality metric may only get better.)
-  All statements and branches are covered by your tests. (codecov.io)

The coverage values may go down by a commit, however this is to be
avoided. Tests must work for every commit.

Continuous integration is always done for the last commit on a pull
request.

Reviewing Commits
-----------------

-  Generated code is not intended to be reviewed. Instead rather try to
   verify that the generation was done right. The commit message should
   expose that.
-  Every commit is reviewed independently from the other commits.
-  Tests should pass for each commit. If you suspect that tests might
   not pass and a commit is not checked by continuous integration, try
   running the tests locally.
-  Check the surroundings. In many cases people forget to remove the
   import when removing the use of something or similar things. It is
   usually good to take a look at the whole file to see if it's still
   consistent.
-  Check the commit message.
-  Take a look at continuous integration results in the end even if they
   pass:
-  Coverage shall not fall.
-  Scrutinizer oftentimes yields helpful results.

As you perform your review of each commit, please make comments on the
relevant lines of code in the GitHub pull request.  After performing your
review, please comment on the pull request directly as follows:

-  If any commit passed review, make a comment that begins with "ack",
   "reack", or "ready" (all case-insensitive) and contains at least the
   first 6 characters of each passing commit hash delimited by spaces,
   commas, or forward slashes (the commit URLs from GitHub satisfy the
   commit hash requirements).

-  If any commit failed to pass review, make a comment that begins with
   "unack" or "needs work" (all case-insensitive) and contains at least
   the first 6 characters of each passing commit hash delimited by
   spaces, commas, or forward slashes (the commit URLs from GitHub
   satisfy the commit hash requirements).

Example:

.. code-block:: none

   unack 14e3ae1 823e363 342700d

If you have a large number of commits to ack, you can easily generate a
list with ``git log --oneline master..`` and write a message like this
example:

.. code-block:: none

   reack
   a8cde5b  Docs: Clarify that users may have pyvenv
   5a05253  Docs: Change Developer Tutorials -> Resources
   c3acb62  Docs: Create a set of notes for development setup

   Rebased on top of changes that are not affected by documentation
   changes.
