Welcome to the Newcomers guide!
===============================

This guide will help you to get involved and teach you how to make your first
contribution to *coala*!

Meet the community!
-------------------

To get started, the first step is to meet the community. We use gitter to
communicate, and there the helpful community will guide you. Join us at `coala gitter <https://gitter.im/coala-analyzer/coala/>`_.
The newcomers should ping us "Hello World" to let us know they are here
because we care!

**Congratulations!** You are now part of our community.

Start working
-------------

Let us know that you are interested in contributing on gitter and ask for an
invitation to our org. This is your first step towards contributing.
The invitation will be sent by mail and you will have to accept
it to join. If you don't find the invitation, accept it `here <https://github.com/coala-analyzer>`_.

Now that you are part of our organization, you can start working on issues.
If you are familiar with git, you can skip the next section and pick an issue.


Get help with git
-----------------

We use github to manage our repository. If you're not familiar with git, we
strongly recommend following a tutorial, such as `this one <https://try.github.io/levels/1/challenges/1>`_.

If there's anything unclear, or you are encountering problems, feel free
to contact us on gitter, and we will help you!

Start working
-------------

Now is the time to pick an issue.
Here is the link that will lead you to `Newcomers issues <http://tinyurl.com/coala-new>`_.

.. seealso::

    For more information about what bears are, please check the following link: `Writing bears <http://coala.readthedocs.org/en/latest/Users/Tutorials/Writing_Bears.html>`_

The easy issues that will help you get started are labeled as
"difficulty/newcomer" and are only there to give you a glimpse of how it is
to work with us.

Now pick an issue which isn't assigned, and if you want to fix
it, then leave a comment that you would like to get assigned. This way
we don't have multiple people working on the same issue at the same time.
Now you can start working on it.
For more info on how to work correctly with git, try `this <http://coala.readthedocs.org/en/latest/Users/Tutorials/Git_Help.html>`_.

.. note::

    Before starting to write your first commit, check out this link:
    `Writing good commits <http://coala.readthedocs.org/en/latest/Getting_Involved/Writing_Good_Commits.html>`_

Things to do before pushing
---------------------------

Now you need to make sure your change is actually working. For this, you will
need to test it locally before pushing it to your fork, and checking it with
concrete examples. So basically, run tests and run *coala* by simply typing

::

    $ coala

into your bash. This will analyze your code and help you fix it.

.. seealso::

    `Executing tests <http://coala.readthedocs.org/en/latest/Getting_Involved/Testing.html>`_

Sending your changes
--------------------

Now that you've fixed the issue, you've tested it and you think it is ready
to be used, create a commit and push it to your fork, using:

::

    $ git push origin fix-branch

Creating a ``Pull Request``
---------------------------

Now that your commit has been sent to your fork, it is time
to do a ``Pull Request``. It can be done by accessing your fork on github and
clicking ``New Pull Request``.

**Congratulations!** You have now created your first ``Pull Request``!

What to do after creating a ``Pull Request``
--------------------------------------------

After creating your ``Pull Request``, there's two options:

- your ``Pull Request`` gets accepted, and your commit will get merged into the
  master branch
- your ``Pull Request`` doesn't, and therefore you will need to to modify it as
  per the review comments

It's highly unlikely that your ``Pull Request`` will be accepted on the first
attempt - but don't worry, that's just how it works. It helps us keep *coala*
**clean** and **stable**.

.. seealso::

    `Review Process <http://coala.readthedocs.org/en/latest/Getting_Involved/Review.html>`_.

Now if you need to modify your code, you can simply edit it again, add it and
commit it using

::

    $ git commit -a --amend

This will edit your last commit message. If your commit message was considered
fine by our reviewers, you can simply send it again like this. If not, edit it
and send it. You have successfully edited your last commit!

.. note::

    Don't forget! After editing your commit, you will have to push it again.
    This can be done using:

::

    $ git push --force origin

**Congratulations!** Your PR just got accepted! You're awesome.
Now try `writing a bear <http://coala.readthedocs.org/en/latest/Users/Tutorials/Writing_Bears.html>`_,
they are really rewarding!
