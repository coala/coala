REVIEWING
=========

This document is a guide to coalas review process. It will be extended over
time.

Review Process
--------------

The review process for coala is as follows:

1. Anyone can submit commits for review. This usually happens on WIP branches,
   submitting goes via GitHub Pull Requests.
2. A reviewer reviews every commit by its own and validates that every commit
   is a good change and does not destroy anything.
3. If a commit does not fulfill the expectations of the reviewer, go to step
   one.
4. If the commits are not linearly mergeable into master, rebase and go to step
   one.
5. All commits are acked and fit linearly onto master. The reviewer or
   submitter may now _fast forward_ the master. Since linear fitting is a
   prerequisite merging is not going to happen nor allowed.

Continous Integration
---------------------

It is not allowed to merge a pull request into master if one of the following
applies:

 * The travis build or any test in it fails or is skipped.
 * The branch coverage goes down. (codecov.io)
 * The statement coverage is not 100%. (coveralls)

The coverage values may go down by a commit, however this is to be avoided.
Tests must work for every commit.
