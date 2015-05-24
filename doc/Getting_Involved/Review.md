# Reviewing

This document is a guide to coalas review process. It will be extended over
time.

# Review Process

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

> **Note**
>
> You might want to add the option `merge.ff = only` to your
> gitconfig.

# Continous Integration

It is not allowed to merge a pull request into master if one of the following
applies:

 * Any test in it fails or is skipped on any of our build servers (travis,
   circleci, scrutinizer, appveyor).
 * The branch coverage goes down. (codecov.io)
 * The statement coverage is not 100%. (coveralls)

The coverage values may go down by a commit, however this is to be avoided.
Tests must work for every commit.

Continuous integration is always done for the last commit on a pull request.

# Reviewing Commits

 * Generated code is not intended to be reviewed. Instead rather try to verify
   that the generation was done right. The commit message should expose that.
 * Every commit is reviewed independently from the other commits.
 * Tests should pass for each commit. If you suspect that tests might not pass
   and a commit is not checked by continuous integration, try running the tests
   locally.
 * Check the surroundings. In many cases people forget to remove the import when
   removing the use of something or similar things. It is usually good to take
   a look at the whole file to see if it's still consistent.
 * Check the commit message.
 * Take a look at continuous integration results in the end even if they pass:
   * Coverage shall not fall.
   * Scrutinizer oftentimes yields helpful results.
