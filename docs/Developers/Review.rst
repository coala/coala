Reviewing
=========

This document is a guide to coala's review process.

Manual Review Process
---------------------

The review process for coala is as follows:

1. Anyone can submit commits for review. These are submitted via Pull Requests
   on Github.
2. After a Pull Request has been created, another developer shall be
   assigned to review the Pull Request. In order for this to be done properly,
   the case of assignment should be asked on the main channel.
3. The commits will undergo review of the developer that is assigned,
   while other developers have the possibility of reviewing it as well.
4. The Pull Request will be labeled with a ``process`` label:

    - ``pending review`` the commit has just been pushed and is awaiting review
    - ``wip`` the Pull Request has been marked as a ``Work in Progress`` by the
      reviewers and has comments on it regarding how the commits shall be
      changed
    - ``approved`` the commits have been reviewed by the developers and they
      are ready to be merged into the master branch

5. The developers will acknowledge the commits by writing

    - ``ack commit_SHA``, in case the commit is ready, or

    - ``unack commit_SHA / commit_SHA needs work`` in case it is not ready yet
      and needs some more work.

6. If the commits are not linearly mergeable into master, rebase and go
   to step one.
7. All commits are acknowledged and fit linearly onto master. All
   continuous integration services (as described below) pass. Anyone
   with collaborator permission may leave the ``@rultor merge`` command
   to get the PR merged automatically.

Automated Review Process
------------------------

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

For the Reviewers
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
   pass.
-  Coverage shall not fall.
-  Scrutinizer often yields helpful results.

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
