.. _newcomer-guide:

Welcome to the Newcomers Guide!
===============================

This is a step by step guide that teaches you the workflow used at coala and
how to use the tools involved with it.
**Please do read the guide before asking us, as most questions we get are
covered in here.**

Before you can start working there are a few things you need to know about
coala:

  - Everyone in the coala community is expected to follow our
    `Code of Conduct <http://coala.io/coc>`_.
  - Do not work on any issue without assignment. Someone else might be working
    on it already.
  - When something is unclear try to find a solution yourself. This is a
    valuable skill!
  - Only after you tried to solve a problem yourself ask the
    `chat <coala.io/chat>`_

You will start as a newcomer, which is kind of a trial. If you complete the
following tasks, you will become a developer at coala:

  - Run coala on a project of yours and fill our
    `usability survey <http://coala.io/usability>`_.
  - Merge a ``difficulty/newcomer`` Pull Request and fill in our
    `survey form <http://coala.io/newform>`_.
  - Review at least a ``difficulty/newcomer`` Pull Request.
  - Merge a ``difficulty/low`` Pull Request.
  - Review at least a ``difficulty/low`` or higher Pull Request.

.. note::

    Just accepting a PR does not count as a review. Even if that PR is
    in a mergable state. We want you to learn and develop an eye for finding
    improvements. When in doubt, don't give an ack and keep reviewing.

Once you have achieved all these, just ask for being promoted on the chat and
provide links to your reviews and merged Pull Requests.
Then, you will be able to name yourself a coala developer!

To see more information about the rights and duties of the different coala
ranks, see the
`membership cEP <https://github.com/coala/cEPs/blob/master/cEP-0001.md>`_.

.. note::

    **You do not need to read the coala codebase to get started** - this guide
    is intended to help you getting started without reading tons of meaningless
    code. Nobody is good at that.

    **Please don't just fix a newcomer issue and leave!**
    Supervising newcomers is a lot of work for us.
    We're all volunteers and we can't keep this up if you don't give back some
    of the work we put into helping you.

Of course, the order is not important, but we recommend starting with a
``newcomer`` issue, followed by a ``low`` issue, and reviewing other PRs while
you wait for reviews.

 Most importantly, this guide is not intended to "check if you are fit" to
 contribute but rather a crash course to *make you fit* to contribute.
 We are a bit picky when it comes to code quality but it's actually not hard at
 all to get to this level if you bear with us through this guide.


Step 0. Run coala
-----------------

As a preparation of joining the community you should find out what this project
is about - if you didn't do this already.
We highly recommend you `install coala <https://coala.io/install>`_ and use it
on at least one of your projects.
Also, we recommend that you read the
`development setup notes <http://coala.io/devsetup>`_ to learn how to set up an
environment to work on coala.

Most importantly, keep notes of what could be better to make the usage easier
and file issues for it!

- What documentation was missing?
- What was hard to understand?
- ...

.. note::

    *Struggling with this?* We have a very verbose guide on this topic in
    `our Google Code In resources <https://github.com/coala/coala/wiki/Google-Code-In-Task-Use-coala>`_
    which can help you find a suitable repository and run coala on a bigger
    project.

Once you complete this, please take the time and
`fill this form <https://coala.io/usability>`_ so we can improve this!

Step 1. Meet the Community!
---------------------------

To get started, the first step is to meet the community.
We use gitter to communicate, and there the helpful community will guide you.
Join us at `coala gitter <https://coala.io/chat>`_.
The newcomers should ping us "Hello World" to let us know they are here
because we care!

**Congratulations!** You are now part of our community.

Step 2. Grab an Invitation to the Organization
----------------------------------------------

Let us know on gitter that you are interested in contributing and ask for an
invitation to our org.
This is your first step towards contributing.
A maintainer will command ``cobot`` (our gitter bot) to invite you and be part
of the Newcomer team.
The invitation will be sent by mail and you will have to accept
it to join.
If you don't find the invitation, accept it `here <https://github.com/coala>`__.

Now that you are part of our organization, you can start working on issues.
If you are familiar with git, you can skip the next section and pick an issue.

Optional. Get Help With Git
---------------------------

We use GitHub to manage our repository.
If you're not familiar with git, we strongly recommend following a tutorial,
such as `this one <https://try.github.io/levels/1/challenges/1>`_.

We also have a page dedicated to git commands that will help you learn the
basics: `here <http://coala.io/git>`__.

Step 3. Picking Up an Issue
---------------------------

Now it is time to pick an issue.
It is the best way to familiarise yourself with the codebase.
Here is the link that will lead you to
`newcomer issues <https://coala.io/new>`_.
Note however, that you need to be logged in before you can follow the Newcomers
issues link.

The easy issues that will help you get started are labeled as
``difficulty/newcomer`` and are only there to give you a glimpse of how it is
to work with us and learning the workflow.

Now pick an issue which isn't assigned.
As stated before, you should never work on an issue without being assigned to
it.
Fortunately, cobot is here to help you!
So, if you are interested in picking up an issue just write the following
command in the gitter chat::

   cobot assign <issue_link>


Take care to write the full link to the issue.


Step 4. Creating a Fork and Testing Your Changes
------------------------------------------------

This tutorial implies you working on your fork.
To fork the repository, go to the official repository of coala/coala-bears
(or whatever coala repository you want to contribute to) and click on the
``Fork`` button from the website interface.
To add it locally, simply run::

    $ git remote add <fork_name> <fork_link>

where ``<fork_name>`` is a name for your fork, and ``<fork_link>`` is a link to
your fork repository.

To start working on an issue, you first need to create a new branch where you
will work.
This is important as working on the master brancht would lead to problems with
our workflow.
To create a new branch, run the following command, where ``<branch_name>`` is
a name for your branch.
Usually this could be something like ``username/feature`` as it helps with
identification::


    $ git checkout -b <branch_name>

Now you need to make sure your change is actually working.
For this, you will need to test it locally before pushing it to your fork,
and checking it with concrete examples.
The first time, you will need to install some requirements.
This can be done by executing the following command while in the root of the
coala project directory::

    $ pip3 install -r test-requirements.txt -r requirements.txt

After that, you can run coala by simply typing::

    $ coala

into your bash. This will analyze your code and help you fix it. If you get
any GitMate errors on your PR that means you probably didn't run coala on it.
To get reviews, fix all the GitMate errors or better, run coala before pushing
to prevent them.

You should also run all tests to make sure, that everything still works as
intended. You can find a guide on how to run our tests
`here <http://api.coala.io/en/latest/Developers/Executing_Tests.html>`__.

If you add new code, that code also has to be tested. You can find a guide on
how to write tests
`here <http://api.coala.io/en/latest/Developers/Writing_Tests.html>`__.

Step 5. Sending Your Changes
----------------------------

.. note::

   Before committing your changes, please check that you are indeed in a
   development branch created in step 4. To check if you are in a branch, type:

   ::

         $ git branch

   Your current branch will have an asterisk (\*) next to it. Ensure that there
   is no asterisk next to the master branch.

Now that you've fixed the issue, you've tested it and you think it is ready
to be merged, create a commit and push it to your fork, using:

::

    $ git push myfork

where ``myfork`` is the name of your fork that you added at the previous step.

.. note::

    You could also add a profile picture on your Github account, so that
    you can be distinguished out from the crowd!

Step 6. Creating a ``Pull Request``
-----------------------------------

Now that your commit has been sent to your fork, it is time
to do a ``Pull Request``. It can be done by accessing your fork on GitHub and
clicking ``New Pull Request``.

**Congratulations!** You have now created your first ``Pull Request``!

.. note::

    Do not delete your comments on Github because it makes it hard for other
    developers to follow on that issue. If necessary, edit your comment in case
    there is a typo or a task list to be updated. If you have to add some new
    information, make a new comment.

If you know you have more work to do on this ``Pull Request`` before it is
ready to be accepted, you can optionally indicate this to other
developers by starting your ``Pull Request`` title with ``wip``
(case-insensitive).

Step 7. Waiting for Review
--------------------------

After creating a Pull Request, your PR is open to the review process (to read
more about it, have patience and it is explained on the next step), and all
you can do is wait. The best thing you can do while at this step is review
other people's PRs. Not only will this help the maintainers with the workload,
but this is one of the three core steps towards becoming a full-norm coalaian.
Never close a Pull Request unless you are told to do so.

For more information about reviewing code, check out this `link <http://coala.io/reviewing>`_.

.. note::

    Reviewing code helps you by watching other people's mistakes and not making
    them yourself in the future!

    **We highly encourage you to do reviews.** Don't be afraid of doing
    something wrong - there will always be someone looking over it before
    merging it to master.

Step 8. Review Process
----------------------

After creating your ``Pull Request``, it is under the review process. This can
be deduced from the ``process/pending review`` label. Now all you have to do
is wait, or let the other developers know on Gitter that you have published
your changes.

.. note::

    Do not tag the reviewers every time you push a change. They review PRs
    consistently whenever they have time!

Now there's two possibilities:

- your ``Pull Request`` gets accepted, and your commits will get merged into
  the master branch
- your ``Pull Request`` doesn't get accepted, and therefore you will
  need to to modify it as per the review comments

.. note::

    Wait until the reviewer has already reviewed your whole Pull Request
    and has labeled it ``process/wip``. Else, if you push again and his
    comments disappear, it can be considered rude.

.. note::

    You might be wondering what those CI things on your ``Pull Request`` are.
    For more detailed info about them, see `this page`_.

It's highly unlikely that your ``Pull Request`` will be accepted on the first
attempt - but don't worry, that's just how it works. It helps us maintain
coala **clean** and **stable**.

.. seealso::

    `Review Process <http://api.coala.io/en/latest/Developers/Review.html>`_.

Now, if you need to modify your code, you can simply edit it again, add it and
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

    $ git push --force myfork

The meaning of ``myfork`` is explained
`here <http://api.coala.io/en/latest/Developers/Newcomers_Guide.html#step-4-creating-a-fork-and-testing-your-changes>`__.
The ``Pull Request`` will automatically update with the newest changes.

**Congratulations!** Your PR just got accepted! You're awesome.
Now you should `tell us about your experience <https://coala.io/newform>`_ and
go for `a low issue <https://coala.io/low>`__ - they are really rewarding!

.. note::

    **Do not only fix a newcomer issue!** It is highly recommended that you
    fix one newcomer issue to get familiar with the workflow at coala and
    then proceed to a ``difficulty/low`` issue.

    However those who are familiar with opensource can start with
    ``difficulty/low`` issues.

    We highly encourage you to start `reviewing <https://coala.io/review>`__
    other's issues after you complete your newcomer issue, as reviewing helps
    you to learn more about coala and python.

.. note::

    If you need help picking up an issue, you can always ask us and we'll help
    you!

    If you ever have problems in finding some links maybe you can find
    the solution in our :doc:`useful links section <Useful_Links>`.

.. _this page: https://docs.coala.io/en/latest/Help/FAQ.html#what-are-those-things-failing-passing-on-my-pull-request
