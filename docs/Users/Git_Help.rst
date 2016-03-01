Git tutorial
============

This tutorial will help you understand how git works and how to use git to
submit your commit on Github.

.. note::
    This tutorial is about using Git in bash/cmd, which we highly recommend,
    as it's cleaner.
    Github is a totally different thing, it is the web interface or app.

How to install Git
------------------

First step is installing Git. Supposing you are on a Debian based distribution,
this will do:

::

    $ sudo apt-get install git-all

Getting started with coala
--------------------------

First of all, you have to fork the repository you are going to contribute to.
This will basically give you a clone of the repository to your own repository.
You can do this by opening `this to fork the coala website <https://github.com/coala-analyzer/coala>`_
or `this to fork the coala-bears website <https://github.com/coala-analyzer/coala-bears>`_
and then clicking 'Fork' in the upper right corner.

Grabbing coala on your local machine
------------------------------------

Now you should clone the repository to your local machine so that you can have
access to all the code and start fixing issues!
To do this, you can use these to clone the coala / coala-bears repositories:

::

    $ git clone https://github.com/coala-analyzer/coala

or

::

    $ git clone https://github.com/coala-analyzer/coala-bears

You should ideally clone the fork so that gets set to 'origin' automatically.
Now you have all your code on your local machine!

Getting to work
---------------

First let's talk about remotes. To communicate with the outside world, git uses
what are called remotes. These are repositories other than the one on your local
disk which you can push your changes into (so that other people can see them) or
pull from (so that you can get others changes).
Now you should add a remote to your local machine so that you can ``pull`` and
``push`` your commits. This can be simply done by using the command:

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
    For more information about tests, check `this link <http://coala.readthedocs.org/en/latest/Getting_Involved/Writing_Tests.html>`_.

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
We are very strict about writing commit messages as they help us keep coala
**clean** and **stable**. Commit messages usually consists of three main
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

  This part will usually have "Fixes <issue_link>", so the issue gets referenced
  on github.

.. seealso::

  For more information about writing commit messages, check this
  `link <http://coala.readthedocs.org/en/latest/Getting_Involved/Writing_Good_Commits.html>`_.

Now that your message is written, you will have to save the file. Press escape
to exit insert mode, and save the file (in Vim that is being done by pressing
shift + Z twice).

Pushing the commit
------------------

Now you will need to push the commit to the fork. All you have to do is:

::

    $ git push myfork

It will most likely ask for your login credentials from github. Type them in,
and your commit will be pushed online.

Creating a Pull Request
-----------------------

Now you would like to get your commit into the actual master branch. Making
your changes available to all future users of the project. For this, you will
have to create a Pull Request. To do this, you will have to go on github, on
your fork page. You should change to branch to the one you have worked on and
submitted the commit on. It should say that it is "1 commit ahead of the master
branch". In case it says something else, such as it is MORE commits ahead or
a few commits behind the master branch, you will have to fix this before you are
creating the Pull Request.

In case your branch is a few commits behind the master branch, it means that
in the meantime, somebody else got an accepted commit, and you need to rebase
it on your local repository. You can do this by typing:

::

    $ git pull origin master

This will try to merge your current branch with the origin master one.
Now it should say your branch is up-to-date. You can keep working now, push it
again online and go ahead and create a Pull Request.

You can create a Pull Request by clicking ``New Pull Request`` button in the
pull request tab.

**Congratulations!** You have just created your first Pull Request!
You are awesome!

Follow-up
---------

Now after you have created the Pull Request, there are two possibilities:

- your PR will get accepted, and your commit will get merged into the master
  branch - sadly, this rarely happens on the first Pull Request

- your PR will be rejected. There are 2 cases when a PR is rejected:

      - Test fails
      - Reviewer wants something changed (This also causes gitmate to fail)

It's highly unlikely that your PR will be accepted on the first attempt - but
don't worry that's just how it works. It helps us keeping coala
**clean** and **stable**.

.. seealso::

     `Review Process <http://coala.readthedocs.org/en/latest/Getting_Involved/Review.html>`_.

Now if you need to modify your code, you can simply edit it again, add it and
commit it using

::

    $ git commit -a --amend

This will edit your last commit message. If your commit message was considered
fine by our reviewers, you can simply send it again like this. If not, edit it
and send it.
Now you have successfully edited your last commit!

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

    $ git rebase

Rebasing is the process of moving a branch to a new base commit. From a content
perspective, rebasing really is just moving a branch from one commit to another.
But internally, Git accomplishes this by creating new commits and applying them
to the specified base—it’s literally rewriting your project history. It’s very
important to understand that, even though the branch looks the same, it’s
composed of entirely new commits.


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
