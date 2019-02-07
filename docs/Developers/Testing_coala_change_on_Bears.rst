Testing changes to coala on coala-bears
=======================================

When large changes are made to the coala core, they should be tested
on the coala-bears to confirm that they work as expected and don't
break anything on the bears' side.

You can do this by changing the coala dependency for the bears to
be the one consisting of the changes. In order to do this, you need to create
a new branch on your coala-bears fork, update the coala requirement to point to
your changes and run CI on it.

Set up a new testing branch
---------------------------

Assuming you have already made changes to coala through a new branch, you can
use that branch to install coala by editing requirements.txt in coala-bears.
Let's set-up a new branch on coala-bears for these changes:

If you have not already, clone the coala-bears repository by running:

::

    $ git clone -o upstream https://github.com/coala/coala-bears

.. note::
    ``-o upstream`` sets the remote name of the original coala-bears repository
    as upstream.

Now, navigate to the directory where coala-bears is located.

::

    $ cd coala-bears

This tutorial assumes you are working on your own fork. If you haven't done so,
go to the `coala-bears <https://github.com/coala/coala-bears>`_ repository
and click on the ``Fork`` button from the website interface. To add it locally,
simply run:

::

    $ git remote add myfork fork_link

where ``myfork`` is the name of your fork, and ``fork_link`` is a link to your
fork repository.

Before making any changes, switch to a new branch.

::

    $ git checkout -b new_test_branch

Here, ``new_test_branch`` is the name of the new branch you just created. You
can use any name you want for this purpose.

.. note::
    Never make any changes on your master branch.
    Please go through our `Newcomers Guide <https://coala.io/newcomer>`_ if
    you are new to coala.

Now that you're on a new branch, you are free to make changes.

Change coala dependency in requirements.txt
-------------------------------------------

First, you need to change the coala dependency.

Now, assuming that you have made changes to your coala fork on branch
``<branch-name>``, you can edit the coala dependency by editing
requirements.txt in coala-bears. To do this, you need to edit the line in
requirements.txt corresponding to:
::

    git+https://github.com/coala/coala#egg=coala

and change it to :

::

    git+https://github.com/<your-username>/coala@<branch-name>#egg=coala

This will install coala from the branch of your coala fork where you have made
changes to the repository.

Commit and push changes
-----------------------

Now, since you have made the required changes to the bears repository, you are
free to commit the changes and push the branch on your fork.

If you are not familiar with git, then first go through our
`Git Tutorial <https://coala.io/gitbasics>`_ to understand the necessary
steps of committing and pushing changes.

.. note::
    Before pushing the branch, make sure to enable CI to your fork. You can
    have a look at our
    `CI Tutorial <https://api.coala.io/en/latest/Developers/Adding_CI.html>`_
    for more info.

Once you've pushed the branch, CI will run the tests and install coala from
the source you've provided. This way you could test core coala changes on
coala-bears to verify the correctness of the changes made.
