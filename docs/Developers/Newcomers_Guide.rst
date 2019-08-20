Welcome to the Newcomers' Guide!
================================

.. container:: shorturl

    +----------------+-----------+
    | Redirects from | newcomer_ |
    +----------------+-----------+

.. _newcomer: https://coala.io/newcomer/
.. _coala Community: https://community.coala.io

**DO NOT WORK ON ANY ISSUE WITHOUT ASSIGNMENT!** If you do, someone else might
work on it as well, and we might have no choice but to reject one of your Pull
Requests. We hate it if someone's time is wasted. For your own sake, please
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
  - do at least a `meta-review <Meta-review.html>`_ or receive a meta-review

.. note::

    After you have solved a ``difficulty/newcomer`` issue, please don't
    take up any more. Instead, move on to more difficult issues.

Once you've run coala on a project, please fill out our
`usability survey <http://coala.io/usability>`_. And once you've got your first Pull
Request merged successfully, fill out our
`survey form <http://coala.io/newform>`_. By doing so, you can help us make your
experience better!

Once you've completed all five tasks, please fill the **promotion request form**
by logging-in on the `coala Community`_,
to get promoted to the role of developer. GitLab contributions also
count to the promotion of a newcomer to developer. In order to work on GitLab
issues, you should be a member of GitLab newcomers group. You can request
access at `GitLab newcomers group <https://gitlab.com/coala/roles/newcomers>`_.
Once you get promoted, you can do following things right from your account on
coala Community website:

  - You can apply to become a *mentor* for the upcoming Google Summer of Code
  - You can add new *calendar events* related to the organization like
    software releases, cEP(coala Enhancement Proposal) merges etc.
  - You can add new *Open Source Google Forms*. The forms which can be filled
    by any contributor and is related to any of the open-source community.

.. note::

    **Don't just fix a newcomer issue!** Supervising newcomers is really a lot
    of work. We're all volunteers and we can't keep this up if you don't help
    us in other areas as well!

Of course, the order of the steps above is not important, although we
recommend that you start with a ``newcomer`` issue, end with a ``low`` issue,
and review other PRs in the meantime!

This is a step-based guide that will help you make your first contribution
to coala, while getting you familiar with the workflow!

For more information about Pull Requests, keep reading!

.. tip::

    **You do not need to read the coala codebase to get started** - this guide
    is intended to help you do that without reading tons of meaningless code.
    Nobody is good at that.

    Most importantly, this guide is not intended to "check if you are fit" to
    contribute, but is rather a crash course to *make you fit* to contribute. We
    are a bit picky when it comes to code quality, but it's actually not at all
    hard to get to this level if you bear with us through this guide.

Step 0. Run coala
-----------------

As you prepare to join our community, you should find out what this project
is about - if you didn't do this already. We highly recommend you
`install coala <https://coala.io/install>`_ and use it on at least one of your
projects. Also, we recommend that you read our
`development setup notes <http://coala.io/devsetup>`_
to learn how to set up an environment to work on coala.

Most importantly, keep notes on what could be changed to make coala usage
easier!  What documentation was missing? What was hard to understand?

.. seealso::

    *Struggling with this?* We have a very verbose guide on this topic in
    `our Google Code In resources <https://github.com/coala/coala/wiki/Google-Code-In-Task-Use-coala>`_
    which can help you find a suitable repository and run coala on a bigger
    project.

Once you complete this, please take the time to
`fill out this form <https://coala.io/usability>`_ so we can get better!

Step 1. Meet the Community and Get an Invitation to the Organization
--------------------------------------------------------------------

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

  * Only log into Gitter using your GitHub account and not your Twitter account
    since the Gitter bot `corobo` identifies each user from their GitHub
    username which makes it possible to automate certain tasks such as asking
    the bot to assign an issue to your profile.
  * Don't @-mention or private message people, unless its utterly important.
    @ mentions generate notifications on the various gitter clients the user
    may be signed into, you might even wake someone on the other side of the
    world up. Also it discourages other people to answer the question,
    so you might wait longer for an answer.
  * Do not mention users unrelated to a particular issue/question. This also
    means you should not mention the person that was last online. For example,
    mentioning someone on a Github issue will subscribe them to that issue,
    even if they don't want to be a part of the discussion. However, mentioning
    someone is okay if they really need to see your message.
  * Don't use /all if you are a newcomer or do not have a critical reason.
  * Don't repeatedly @-mention people in an ongoing conversation.
  * You should ask someone before mentioning them.

Now you are ready to join coala community at `coala gitter <https://coala.io/chat>`_.
The newcomers should ping us "Hello World" to let us know they are here
because we care!

When you say "Hello World" in chat, ``corobo`` (our gitter bot) will invite you
to be part of the Newcomer team. The invitation will be sent by mail and you
will have to accept it to join. If you don't find the invitation, accept it
`here <https://github.com/coala>`__.

In any case if the ``corobo`` is down, you can join the community by filling
out this `joining form <https://community.coala.io/join>`_. By filling out
this form, we'll perform some automated rudimentary checks to validate whether
you're eligible to be a member of the organization or not. Once all the checks
are validated, you'll receive an *invite* to be a part of the Newcomer's team.

**Congratulations!** Now that you are part of our organization, you can start
working on issues. If you are familiar with git, you can skip the next section
and pick an issue.

.. note::

    If you have any questions, ask them in a precise and respectful way that
    maximizes your chances of getting the answer you're looking for.
    If you're unsure how to do that, please read: `How To Ask Questions
    The Smart Way <http://www.catb.org/esr/faqs/smart-questions.html>`_.

Optional. Get Help With Git
---------------------------

We use GitHub to manage our repository. If you're not familiar with
git/GitHub, we strongly recommend following a tutorial, such as `this one
<https://try.github.io/levels/1/challenges/1>`_.

We also have a `page dedicated to git commands <http://coala.io/git>`_ that
will help you learn the basics.

.. note::

    You can view some of our repositories on
    `GitLab <https://gitlab.com/coala>`_.
    For more information about it, browse to our
    `wiki page <https://github.com/coala/coala/wiki/GitLab>`_.

If anything is unclear, or you are encountering problems, feel free
to contact us on `gitter <https://coala.io/chat>`_,
and we will help you!

Step 2. Picking Up an Issue
---------------------------

Now it is time to pick an issue.
It is the best way to familiarise yourself with the codebase and the
coala contribution guidelines.

You can view `all Newcomer issues on GitHub <https://coala.io/new>`_.

.. important::

    You need to be logged in before you follow the Newcomer issues link.

.. seealso::

    For more information about what bears are, please check the following link: `Writing Native bears <http://api.coala.io/en/latest/Developers/Writing_Native_Bears.html>`_

The easy issues that will help you get started are labeled as
``difficulty/newcomer`` and are only there to give you a glimpse of what
it's like to work with us and what the workflow is like.

The coala community creates a constant supply of ``newcomer`` issues available
for people like you who are joining the organisation, so that you can learn
how to contribute according to the coala organisation development guides,
while doing a real task at the same time.

coala does **not** follow the GitHub "flow" workflow, so be sure to read
our guides carefully. You will need to use the ``git`` command line.
During the newcomer process, we will help you conquer ``git``, so that you
can become a part of our super efficient developer team.

If you do not follow the coala workflow, our bots will get grumpy, and
members of our community will try to help you in every way possible to
get your Pull Request merged, the coala way.

**Never** create a second Pull Request for your newcomer issue.
Instead, if you have troubles on your first Pull Request, seek help from
the manual or ask for guidance on `gitter chat <https://coala.io/chat>`_
to reach a resolution for your troubles.

Your Pull Request will **not** be accepted until it complies with coala
standards, even if your solution is amazingly correct. If you ignore the
bots or our developers, or if you close any Pull Request, we will have
no option except to conclude that you have abandoned the coala newcomer
process, and your amazing solution **will** be discarded.
We may nudge you to finish your Pull Request, but eventually a maintainer
will close incomplete Pull Request, and your newcomer issue will be returned
to the available queue, ready for the next person learning the coala workflow.

Now pick an issue which isn't assigned and which you would like to fix.
Leave a comment that you would like to be assigned to the issue. This way
we don't have multiple people working on the same issue at the same time.

Remember that all newcomer issues should be very simple to fix, after you
have understood the problem.
Choose one of the newcomer issues that you really understand.
If you have spent more than an hour debugging or coding, maybe your
newcomer issue was incorrectly classified as a newcomer issue.
Ask a developer to check if it should be reclassified as `low` difficulty.

.. caution::

    As stated above, you should never work on an issue without being
    assigned. Fortunately, corobo is here to help you! If you are
    interested in picking up an issue, just write the following command
    in gitter chat::

        corobo assign <issue_link>

    Be sure to copy the full link to the issue!
    Also take up the issue, only when you know what the problem is and
    how to solve it.

    You can do amazing stuff using corobo.

        * Issue assigning as stated earlier.
        * File issues::

            corobo file issue <repo> <title>
            <description>

        * You shouldn't close any PR, instead mark them as work in progress::

            corobo mark wip <full url>

        * To label a PR as pending review::

            corobo mark pending <full url>

        * To see all of the corobo commands::

            corobo help

    Before starting your first commit, check out this
    link: `Writing good commits <http://coala.io/commit>`_.

.. note::

    If the ``corobo`` is down atm, you can also get assigned to an issue by
    logging-in on the `coala Community`_. There
    is a form available for it, if you want to get assigned on that issue.
    Filling up that form will perform some checks to check whether the issue
    on which you wish to work is valid or not. If valid, you'll receive an
    email to get assigned to it. Open the link in the browser to get
    successfully assigned to that issue.

.. important::

    An important part of working on issues is documenting your work
    in such a way that it is easy for others to read and understand.
    A lot of Newcomer issues involve improving documentation.

    * For more information about writing good documentation,
      please check the following link: `Writing Documentation <https://api.coala.io/en/latest/Developers/Writing_Documentation.html>`_

    * For more information about how to style Python code
      according to the PEP8 code style convention,
      please check the following link:
      `PEP8 Style Guide for Python code <https://www.python.org/dev/peps/pep-0008/>`_

Step 3. Creating a Fork and Testing Your Changes
------------------------------------------------

This tutorial assumes you are working on your own fork. To fork the
repository, go to the official repository of coala/coala-bears and click on the
``Fork`` button from the website interface. To add it locally, simply run:

::

    $ git remote add myfork fork_link

where ``myfork`` is the name of your fork, and ``fork_link`` is a link to your
fork repository.

.. important::
   It is important that you **DO NOT** make your changes on the master branch
   of your forked repository to avoid the following cases:

   - If you make a rebase to synchronize your repository to the original,
     every commit that is pushed to the remote master will be pulled in your
     master branch. Then if you make a pull request to commit your changes to
     the remote, the commits that got synced from the rebase will be
     recommitted along with your work in the pull request.

   - You cannot have two pull requests using the same branch name. Therefore,
     if your fork's master has been used in a pull request and you decide to
     work on a different issue you will have to branch eventually. Differently
     every new commit that you make on your master branch will get attached to
     the initial pull request and that will result in altering the purpose of
     that request.

   - If your fork's master has been used in a pull request, you have to keep
     the change in the branch until that get's merged to the remote master.
     That will lead to the complications listed above, if you decide to work
     on a different issue.

   In order to avoid the above mentioned cases you can create a new branch
   where you will work on the issue. To do that run:

   ::

        $ git checkout -b <branchname>

Now you need to make sure your change is actually working. For this, you will
need to test it locally before pushing it to your fork and checking it with
concrete examples. The first time, you will need to install some requirements.
This can be done by executing the following command while in the root of the
coala project directory:

::

    $ pip3 install -r test-requirements.txt -r requirements.txt


After the test dependencies have been installed
run pytest to test your changes locally:

::

    $ pytest

Incase pytest gives you an error, try;

::

    $ python3 -m pytest

After that, you can run coala by simply typing

::

    $ coala

into your bash prompt. This will analyze your code and help you fix it.

.. seealso::

    `Executing tests <http://api.coala.io/en/latest/Developers/Executing_Tests.html>`_

Step 4. Sending Your Changes
----------------------------

.. caution::

   Before committing your changes, please check that you are indeed in a
   development branch created in step 3. To check if you are in a branch, type:

   ::

         $ git branch

   Your current branch will have an asterisk (\*) next to it. Ensure that there
   is no asterisk next to the master branch.

Now that you've fixed the issue, you've tested it, and you think it is ready
to be merged, add your updated file to the staging area:

::

    $ git add <file/folder_name>

Create a commit using the following command:

::

    $ git commit

This will open a text editor to write commit message.

After saving the commit, you can check your commit message using:

::

    $ git show

If you made a mistake in the commit message, edit the commit message again:

::

    $ git commit --amend

Once you are happy that the commit message is correct,
push it to your fork using:

::

    $ git push -u myfork <branchname>

where ``myfork`` is the name of your fork that you added at the previous step.

After making the changes, it is recommended that you test the code on your
forked repository by `adding the required CI
tools <http://api.coala.io/en/latest/Developers/Adding_CI.html>`_.

.. note::

    You can also add a profile picture to your Github account so that
    you can stand out from the crowd!

Step 5. Creating a Pull Request
-------------------------------

Now that your commit has been sent to your fork, it is time
to create a ``Pull Request``. You can do this by accessing your fork on GitHub
and clicking ``New Pull Request``.

**Congratulations!** You have now created your first ``Pull Request``!

Now, before having other contributors review your work, the system will do an
automated code review and will comment the requested improvements (respecting
coding style and commit message rules, line length and spacing etc.) on your
Pull Request.

.. important::

    It is **never** allowed to close your Pull Request. **Never!**

    It is **always** possible to modify your Pull Request using
    `git <https://coala.io/git>`_.

    By no means should you delete your branch or your fork, close your
    ``Pull Request`` or open a new one. All of those actions will create
    a mess.

    It is highly recommended that you use the tools provided by ``git`` to
    apply certain modifications to your Pull Request, and not open another one
    for the same issue.

.. note::

    Do not delete your comments on Github, because that makes it hard for other
    developers to follow that issue. If there is a typo or a task list to be
    updated, you can edit your comment instead. If you need to add new
    information, make a new comment.

If you know you have more work to do on this ``Pull Request`` before it is
ready to be accepted, you can indicate this to other
developers by starting your ``Pull Request`` title with ``wip``
(case-insensitive, stands for "Work in Progress").

Step 6. Waiting for Review
--------------------------

After creating a Pull Request, your PR moves to the review process (all will
be explained in the next step), and all you can do is wait. The best thing you
can do at this step is review other people's PRs. Not only will this help
the maintainers with the workload, but this is one of the three core steps
towards becoming a full-blown coalaian.  Never close a Pull Request unless you
are told to do so.

For more information about reviewing code, check out this `link <http://coala.io/reviewing>`_.

.. note::

    Reviewing code helps you to learn from other people's mistakes so you can
    avoid making those same mistakes yourself in the future! Thus, you are
    improving yourself in the process.

    **We highly encourage you to do reviews.** Don't be afraid of doing
    something wrong - there will always be someone looking over it before
    merging it to master.

Step 7. Review Process
----------------------

After creating your ``Pull Request``, it enters the review process. You can
see that's the case from the ``process/pending review`` label. Now all you have
to do is wait, or let the other developers know on Gitter that you have
published your changes.

.. important::

    Do not tag the reviewers every time you push a change. They review PRs
    consistently whenever they have time!

Now there are two possibilities:

- your ``Pull Request`` gets accepted, and your commits will get merged into
  the master branch
- your ``Pull Request`` doesn't get accepted, and therefore you will
  need to modify it as per the review comments

.. caution::

    Wait until the reviewer has reviewed your whole Pull Request
    and has labeled it ``process/wip``. If you push again before that happens,
    and their comments disappear, it can be considered rude.

.. note::

    You might be wondering what those CI things on your ``Pull Request`` are.
    For more detailed info about them, see `this page`_.

It's highly unlikely that your ``Pull Request`` will be accepted on the first
attempt - but don't worry, that's just how it works. It helps us keep
coala **clean** and **stable**.

.. seealso::

    `Review Process <http://api.coala.io/en/latest/Developers/Review.html>`_.

Now, if you need to modify your code, you can simply edit it again, add it, and
commit it using

::

    $ git commit -a --amend

This will edit your last commit message. If your commit message was considered
acceptable by our reviewers, you can simply send it again (without any
changes). If not, edit it and send it. You have successfully edited your last
commit!

.. note::

    Don't forget! After editing your commit, you will have to push it again.
    This can be done using:

::

    $ git push --force myfork

The meaning of ``myfork`` is explained
`in step 3 of this guide
<http://api.coala.io/en/latest/Developers/Newcomers_Guide.html#step-3-creating-a-fork-and-testing-your-changes>`__.
The ``Pull Request`` will automatically update with the newest changes.

**Congratulations!** Your PR just got accepted! You're awesome.
Now you should `tell us about your experience <https://coala.io/newform>`_ and
go for `a low issue <https://coala.io/low>`__ - they are really rewarding!


.. attention::

    Do not delete the fork subsequent to Pull Request for review or
    after it is merged!

.. note::

    **Do not just fix a newcomer issue!** It is highly recommended that you
    fix one newcomer issue to get familiar with the workflow at coala and
    then proceed to a ``difficulty/low`` issue.

    However, those who are familiar with opensource projects can start with
    ``difficulty/low`` issues.

    We highly encourage you to start `reviewing <https://coala.io/review>`__
    other's issues after you complete your newcomer issue, as reviewing helps
    you to learn more about coala and python.

.. note::

    If you need help picking up an issue, you can always ask us. The community
    is extremely helpful, so `don't ask to ask, just ask
    <http://sol.gfxile.net/dontask.html>`__.

    If you ever have problems in finding links, you may find
    the solution in our :doc:`useful links section <Useful_Links>`.

.. _this page: https://docs.coala.io/en/latest/Help/FAQ.html#what-are-those-things-failing-passing-on-my-pull-request
