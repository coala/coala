Git Tutorial
============

This tutorial will help you understand how git works and how to use git to
submit your commit on Github.

.. note::
    This tutorial is about using Git in bash/cmd, which we highly recommend,
    as it's cleaner.
    Github is a totally different thing, it is the web interface or app.

How to install Git
------------------

First step is installing Git. Supposing you are on a Debian-based distribution,
this will do:

::

    $ sudo apt-get install git-all

For installing Git on a Mac OS system, you can use the `homebrew <https://brew.sh/>`_ package
manager as follows:

::

    $ brew install git

Getting Started with coala
--------------------------

First of all, you have to fork the repository you are going to contribute to.
This will basically give you a clone of the repository to your own repository.
You can do this by opening `this to fork the coala repository <https://github.com/coala/coala>`_
or `this to fork the coala-bears repository <https://github.com/coala/coala-bears>`_
and then clicking 'Fork' in the upper right corner.

Grabbing coala on your local machine
------------------------------------

Now you should clone the repository to your local machine so that you can have
access to all the code locally and start fixing issues!
To do this, you can use these to clone the coala/coala-bears repositories:

::

    $ git clone -o upstream https://github.com/coala/coala

or

::

    $ git clone -o upstream https://github.com/coala/coala-bears

.. note::

    ``-o upstream`` sets the remote name of the original coala/coala-bears
    repositories as ``upstream``.

    **upstream** is just a name we used for simplicity. You can name it
    however you want.

    Don't worry if you're not familiar with what remotes are. The following
    section will explain more about remotes.

Now you have all your code on your local machine!

Getting to work
---------------

First let's talk about remotes. To communicate with the outside world, git uses
what are called remotes. These are repositories other than the one on your
local disk which you can push your changes into (so that other people can see
them) or pull from (so that you can get others changes).
Now you should add a remote of your fork to your local machine so that you can
``pull`` and ``push`` your commits. This can be simply done by using the
command:

::

    $ git remote add myfork <your_fork_link>

.. note::
  **myfork** is just a name we used for simplicity. You can
  name it however you want.

Creating a new branch
---------------------

To start working on an issue, you first need to create a new branch where you
will work.

::

    $ git checkout -b branchname

.. note::

    ``checkout`` will switch to the newly created branch.

    ``-b`` will create a new branch if the branch doesn't already exist.

Checking your work
------------------

After the issue is fixed and you have tested it (tests are very important!
never submit a change that isn't tested), you should check your progress. Type:

::

    $ git status

It will give you an idea about what files are currently modified.

.. note::

    Tip: If there's something you don't find, you can always use:

    ``$ git grep "syntax"``

    This will search through the whole repository and show you the files
    that contain the syntax.

.. seealso::
    For more information about tests, check
    :doc:`this link. <Writing_Tests>`

Adding the files and commiting
------------------------------

Now you can add your files/folders to the current commit:

::

    $ git add <file/folder_name>

Do this until you have added all the files needed for your commit.
Then type:

::

    $ git commit

This will lead you to a text editor. Now you need to write your commit message.
We are very strict about writing commit messages as they help us maintain
coala **clean** and **stable**. Commit messages usually consists of three main
parts. They should have a newline between them.

- **The header**

  The header should have the name of the file that you have made the change on,
  followed by ":", a space, and then a short title that explains the change
  made.

  Example: `.gitignore: Add a new Constants variable`

- **The body**

  The body should have a short paragraph that briefly describes the change
  that was made, and the reason why this change was needed in imperative.
  Its maximum length is 50 characters.

- **The issue that is being fixed**

  This part will usually have "Fixes <issue_link>", so the issue gets
  referenced on GitHub.

.. seealso::

  For more information about writing commit messages, check this
  `link <http://coala.io/commit>`_.

Now that your message is written, you will have to save the file. Press escape
to exit insert mode, and save the file (in Vim that is being done by pressing
shift + Z twice).

Run coala
------------------

Now you can check if your commit messages and code formattings
conform with the community guidelines.
If something goes wrong, coala will let you know. The continuous integration
(CI) will fail if coala reports errors which means that we cannot proceed
with merging your fix/pull request.

::

  $ coala

Pushing the commit
------------------

Now you will need to push the commit to the fork. All you have to do is:

::

    $ git push myfork

It will most likely ask for your login credentials from GitHub. Type them in,
and your commit will be pushed online.

Creating a Pull Request
-----------------------

Now you would like to get your commit into the actual master branch. Making
your changes available to all future users of the project. For this, you will
have to create a Pull Request. To do this, you will have to go on GitHub, on
your fork page. You should change the branch to the one you have worked on and
submitted the commit on. Now you can create a Pull Request by clicking the
``New Pull Request`` button in the pull request tab.

**Congratulations!** You have just created your first Pull Request!
You are awesome!

.. note::
    If you see any error like ``1 commit ahead of the master branch`` you need
    to sync your local fork with the remote repository before sending
    a pull request.

    More information regarding syncing can be found `here <http://coala.io/git#rebasing>`_.

Follow-up
---------

Now after you have created the Pull Request, there are two possibilities:

- your PR will get accepted, and your commit will get merged into the master
  branch - sadly, this rarely happens on the first Pull Request

- your PR will be rejected. There are 2 cases when a PR is rejected:

      - Test fails
      - Reviewer wants something changed (This also causes gitmate to fail)

It's highly unlikely that your PR will be accepted on the first attempt - but
don't worry that's just how it works. It helps us maintain coala
**clean** and **stable**.

.. seealso::

     :doc:`Review Process. <Review>`

Now if you need to modify your code, you can simply edit it again, add it and
commit it using

::

    $ git commit -a --amend

This will edit your last commit message. If your commit message was considered
fine by our reviewers, you can simply send it again like this. If not, edit it
and send it.
Now you have successfully edited your last commit!

If you need to rebase, or want to edit an older commit from your branch, we
have an amazing `tutorial that you can watch <https://asciinema.org/a/78683>`__
to understand how it works.

Rebasing
--------

As people work on coala new commits will be added. This will result in your
local fork going out of sync with the remote repository.
To sync your changes with the remote repository run the following commands in
the desired branch:

.. note::

    This assumes that the remote ``upstream`` is the original
    coala repository at https://github.com/coala/coala (or other,
    like coala/coala-bears, etc.), **not your fork**.

    If you have followed the steps outlined in this guide and cloned
    the original coala repository, ``upstream`` should refer to it.
    You can proceed to the following section without worry.

    If you're unsure about this, run ``git remote -v`` to check which
    remote points to the original repository and use that instead
    of ``upstream`` in the following section.

::

    $ git fetch upstream
    $ git rebase upstream/master

This will fetch the commits from the remote repository and will merge it into
the branch where you are currently working, and move all of the local commits
that are ahead of the rebased branch to the top of the history on that branch.

.. note::

    After following these instructions when you try to push to remote you may
    get fast-forwarding error. If that is the case, then you will have to
    force push since you are attempting to rewrite the git commit history.
    To do that append the ``--force`` argument in the push command:

    ``$ git push myfork --force``

    **Warning:** Never force-push on the master branch, or any branch not
    owned by you.

To verify whether you have rebased correctly, go to the web page of the
branch in your fork. If it says your branch is ``n commits behind
coala:master`` (or whichever repo you are contributing to), then you
haven't correctly rebased yet. Otherwise, you're good to go!

Squashing your commits
----------------------

It's possible that you have more than one commit and you want them to be
squashed into a single commit. You can take your series of commits and squash
them down into a single commit with the interactive rebasing tool. To squash
your commits run the following command:

::

    $ git rebase -i master

.. note::

    master is the SHA1 hash of the commit before which you want to squash all
    the commits and make sure that rebase is done onto master branch.

An editor will be fired up with all the commits in your current branch
(ignoring merge commits), which come after the given commit. Keep the first one
as "pick" and on the second and subsequent commits with "squash". After saving,
another editor will be fired up with all the messages of commits which you want
to squash. Clean up all the messages and add a new message to be
displayed for the single commit.

Common Git Issues
-----------------

Sometimes, you use git add-A and add files you didn't want to your push (often
after rebasing) and push it to the remote. Here ,is a short outline of, how can
you remove (or revert changes in) particular files from your commit even after
pushing to remote.

In your local repo, to revert the file to the state before the previous commit
run the following:
::

    $ git checkout HEAD^ /path/to/file

Now , after reverting the file(s) update your last commit, by running :
::

    $ git commit -a --amend

To apply these changes to the remote you need to force update the branch :
::

    $ git push -f myfork

.. note::

    The procedure outlined above helps roll back changes by one commit only.
    'myfork' mentioned above is your forked repository, where you push your
    commits.

The ``git checkout <revision sha> path/to/file`` command offers you more
flexibility in reverting the changes in a file, done even from earlier than the
last commit. By replacing the ``HEAD^`` by the revision number of the particular
HEAD commit, you can refer to the required revision of the file.

Might sound a little intimidating, but don't worry, an example has been
provided for you.
First you can check the commit's revision number, where the file was revised by
running the following command:
::

    $ git log /path/to/file

The revision number might look like ``3cdc61015724f9965575ba954c8cd4232c8b42e4``
Now, to revert the file to that revision, run the command:
::

    $ git checkout 3cdc61015724f9965575ba954c8cd4232c8b42e4 /path/to/file.txt

Now, after the file gets reverted back to the required revision, commit the
changes and (force)push to the remote.

If at any stage you are confused, or have an issue, do not close your Pull
Request. Instead, contact us on gitter so that we can help you resolve your
problem.

Useful Git commands
-------------------

This section will briefly explain some other Git commands you will most likely
use and will really make your work easier.

::

    $ git config

The ``git config`` command lets you configure your Git installation (or an
individual repository) from the command line. This command can define
everything from user info to preferences to the behavior of a repository.

::

    $ git log

The ``git log`` command displays committed snapshots. It lets you list the
project history, filter it, and search for specific changes. While git status
lets you inspect the working directory and the staging area, git log only
operates on the committed history.

::

    $ git push --force myfork

While we normally use ``git push myfork`` to push your commit to your fork,
after further editing and work on your commit, you will need to use the
``--force`` parameter to your push to automatically update your Pull Request.

::

    $ git reset --hard

Reset the staging area and the working directory to match the most recent
commit. In addition to unstaging changes, the ``--hard`` flag tells Git to
overwrite all changes in the working directory, too. Put another way: this
obliterates all uncommitted changes, so make sure you really want to throw
away your local developments before using it.

::

    $ git clean

The ``git clean`` command removes untracked files from your working directory.
This is really more of a convenience command, since it’s trivial to see which
files are untracked with git status and remove them manually. Like an ordinary
rm command, ``git clean`` is not undoable, so make sure you really want to
delete the untracked files before you run it.

::

    $ git checkout <branch>

The ``git checkout`` command is used to switch to another branch in the
repository. Here <branch> is the name of the branch you want to switch to.

::

    $ git rebase

Rebasing is the process of moving a branch to a new base commit. From a content
perspective, rebasing really is just moving a branch from one commit to
another. But internally, Git accomplishes this by creating new commits and
applying them to the specified base—it’s literally rewriting your project
history. It’s very important to understand that, even though the branch looks
the same, it’s composed of entirely new commits.


::

    $ git rebase -i

Running ``git rebase`` with the -i flag begins an interactive rebasing session.
Instead of blindly moving all of the commits to the new base, interactive
rebasing gives you the opportunity to alter individual commits in the process.
This lets you clean up history by removing, splitting, and altering an existing
series of commits. It’s like ``git commit --amend`` on steroids.
Usage is ``$ git rebase -i <base>``. Rebase the current branch onto <base>, but
use an interactive rebasing session. This opens an editor where you can enter
commands (described below) for each commit to be rebased. These commands
determine how individual commits will be transferred to the new base. You can
also reorder the commit listing to change the order of the commits themselves.

If you would like more information/commands, please use your favourite search
engine to look for it. Git is widely used throughout the world and there are
many good tutorials and git related Q&A threads out there.
