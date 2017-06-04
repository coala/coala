.. _newcomer-guide:

Welcome to the Newcomers Guide!
===============================

**DO NOT WORK ON ANY ISSUE WITHOUT ASSIGNMENT!** If you do, someone else might
work on it as well and we might have no choice but reject one of your Pull
Requests - we hate it if anyone wastes their time. For your own sake, please
follow this guide. We put a lot of work into this for you!

Everyone in the coala community is expected to follow our
`Code of Conduct <http://coala.io/coc>`_.

To become part of the coala developers team, there are a few steps you need
to complete. The newcomer process is as follows:

You will start as a newcomer, which is kind of a trial. If you complete the
following tasks, you will become a developer at coala:

  - run coala on a project of yours
  - merge a ``difficulty/newcomer`` Pull Request
  - review at least a ``difficulty/newcomer`` Pull Request
  - merge a ``difficulty/low`` Pull Request
  - review at least a ``difficulty/low`` or higher Pull Request

When you ran coala on a project, please fill our
`usability survey <http://coala.io/usability>`_. Once you got your first Pull
Request merged successfully, fill in our
`survey form <http://coala.io/newform>`_. With that you can help us making your
experience better!

Once you have achieved all these, just ask for being promoted on the chat and
provide links to your reviews and merged Pull Requests. Then, you will be able
to name yourself a coala developer!

.. note::

    **Do not only fix a newcomer issue!** Supervising newcomers is really a lot
    of work. We're all volunteers and we can't keep this up if you don't help
    us in other areas as well!

Of course, the order is not important, although, we recommend you to start
with a ``newcomer`` issue, end with a ``low`` issue, and review other PRs in
the meantime!

This is a step-based guide that will help you get your first contribution
at coala, making you familiar with the work flow!

For more information about Pull Requests, keep reading!

.. note::

    **You do not need to read the coala codebase to get started** - this guide
    is intended to help you do that without reading tons of meaningless code.
    Nobody is good at that.

    Most importantly, this guide is not intended to "check if you are fit" to
    contribute but rather a crash course to *make you fit* to contribute. We
    are a bit picky when it comes to code quality but it's actually not at all
    hard to get to this level if you bear with us through this guide.

Step 0. Run coala
-----------------

As a preparation of joining the community you should find out what this project
is about - if you didn't do this already. We highly recommend you
`install coala <https://coala.io/install>`_ and use it on at least one of your
projects. Also, we recommend that you read
`development setup notes <http://coala.io/devsetup>`_
to learn how to set up an environment to work on coala.

Most importantly, keep notes of what could be better to make the usage easier!
What documentation was missing? What was hard to understand?

.. note::

    *Struggling with this?* We have a very verbose guide on this topic in
    `our Google Code In resources <https://github.com/coala/coala/wiki/Google-Code-In-Task-Use-coala>`_
    which can help you find a suitable repository and run coala on a bigger
    project.

Once you complete this, please take the time and
`fill this form <https://coala.io/usability>`_ so we can improve this!

Step 1. Meet the Community!
---------------------------

To get started, the first step is to meet the community. We use gitter to
communicate, and there the helpful community will guide you.
Gitter is an instant messaging service used by developers and users of GitHub.
Gitter uses chatrooms, where developers can join in and can talk about a
particular topic.
coala has 2 types of chatrooms - repository chatrooms and discussion topics.
Repository chatrooms are related to a specific repository and
discussion chatrooms are related to general discussion topics like
conferences, workshops, etc.

  * `coala <https://gitter.im/coala/coala>`_
    This is the main chatroom and repository chatroom of coala/coala.
  * `gsoc <https://gitter.im/coala/coala/gsoc>`_
    This is where you discuss about Google Summer of Code.
  * `coala-bears <https://gitter.im/coala/coala-bears>`_
    Repo chatroom for coala/coala-bears.
  * `workshop <https://gitter.im/coala/coala/workshops>`_
    Discussions related to workshops go here.
  * `conferences <https://gitter.im/coala/conferences>`_
    Everything related to conferences.
  * `offtopic <https://gitter.im/coala/coala/offtopic>`_
    Anything fun! Our gaming sessions start here.

The list of all available chatrooms are available here - `channel list <https://coala.io/channels>`_

But before joining the community, here are few things that you should
keep in mind.

  * Don't @-mention or private message people, unless its utterly important.
    @ mentions generate notifications on the various gitter clients the user
    may be signed into, you might even wake someone on the other side of the
    world up. Also it discourages other people to answer the question,
    so you might wait longer for an answer.
  * Don't use /all if you are a newcomer or do not have a critical reason.
  * Don't repeatedly @-mention people in an ongoing conversation.
  * You should ask someone before mentioning them.

Now you are ready to join coala community at `coala gitter <https://coala.io/chat>`_.
The newcomers should ping us "Hello World" to let us know they are here
because we care!

**Congratulations!** You are now part of our community.

Step 2. Grab an Invitation to the Organization
----------------------------------------------

Let us know on gitter that you are interested in contributing and ask for an
invitation to our org. This is your first step towards contributing.
A maintainer will command ``cobot`` (our gitter bot) to invite
you and be part of the Newcomer team.
The invitation will be sent by mail and you will have to accept
it to join. If you don't find the invitation, accept it `here <https://github.com/coala>`__.

Now that you are part of our organization, you can start working on issues.
If you are familiar with git, you can skip the next section and pick an issue.

Optional. Get Help With Git
---------------------------

We use GitHub to manage our repository. If you're not familiar with git, we
strongly recommend following a tutorial, such as `this one <https://try.github.io/levels/1/challenges/1>`_.

We also have a page dedicated to git commands that will help you learn the
basics: `here <http://coala.io/git>`_.

If there's anything unclear, or you are encountering problems, feel free
to contact us on `gitter <https://coala.io/chat>`_,
and we will help you!

Step 3. Picking Up an Issue
---------------------------

Now it is time to pick an issue.
It is the best way to familiarise yourself with the codebase.
Here is the link that will lead you to `Newcomers issues <https://coala.io/new>`_.

.. note::

    You need to be logged in before you follow the Newcomers issues link.

.. seealso::

    For more information about what bears are, please check the following link: `Writing Native bears <http://api.coala.io/en/latest/Developers/Writing_Native_Bears.html>`_

The easy issues that will help you get started are labeled as
``difficulty/newcomer`` and are only there to give you a glimpse of how it is
to work with us and regarding the workflow.

Now pick an issue which isn't assigned, and if you want to fix
it, then leave a comment that you would like to get assigned. This way
we don't have multiple people working on the same issue at the same time.
Now you can start working on it.

.. note::

    As stated before, you should never work on an issue without any
    assignment. Fortunately, cobot is here to help you! So, if you are
    interested in picking up an issue just write in the gitter chat the
    following command::

        cobot assign <issue_link>

    Take care to write the full link to the issue.
    Also take up the issue, only when you know what the problem is and
    how to solve it.

    You can do amazing stuff using cobot.

        * Issue assigning as stated earlier.
        * File issues::

            cobot file issue <repo> <title>
            <description>

        * You shouldn't close any PR, instead mark them as work in progress::

            cobot mark wip <full url>

        * To see all of the cobot commands, ::

            cobot help

    Before starting to write your first commit, check out this
    link: `Writing good commits <http://coala.io/commit>`_.

.. seealso::

    An important part of working on issues is documenting your work
    in such a way that it is easy for others to read and understand.
    A lot of Newcomer issues involve improving documentation.

    * For more information about writing good documentation,
      please check the following link: `Writing Documentation <https://api.coala.io/en/latest/Developers/Writing_Documentation.html>`_

    * For more information about how to style Python code
      according to the PEP8 code style convention,
      please check the following link:
      `PEP8 Style Guide for Python code <https://www.python.org/dev/peps/pep-0008/>`_

Step 4. Creating a Fork and Testing Your Changes
------------------------------------------------

This tutorial implies you working on your fork. To fork the repository, go
to the official repository of coala/coala-bears and click on the ``Fork``
button from the website interface. To add it locally, simply run:

::

    $ git remote add myfork fork_link

where ``myfork`` is the name of your fork, and ``fork_link`` is a link to your
fork repository.

.. note::
   It is important that you do not make your changes on the master branch. To
   start working on an issue, you first need to create a new branch where you
   will work.

   ::
        $ git checkout -b <branchname>

Now you need to make sure your change is actually working. For this, you will
need to test it locally before pushing it to your fork, and checking it with
concrete examples. The first time, you will need to install some requirements.
This can be done by executing the following command while in the root of the
coala project directory.

::

    $ pip3 install -r test-requirements.txt -r requirements.txt

After that, you can run coala by simply typing

::

    $ coala

into your bash. This will analyze your code and help you fix it.

.. seealso::

    `Executing tests <http://api.coala.io/en/latest/Developers/Executing_Tests.html>`_

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
