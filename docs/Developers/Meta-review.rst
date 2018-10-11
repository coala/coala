Meta-Reviewing
==============

This document is a guide to coala's meta-review process.

What is Meta-review?
--------------------

People respond to review comments on pull requests by giving feedback. Emoji
make it much easier to give and receive feedback without a long comment thread.
Those emoji are called
`reactions <https://developer.github.com/v4/enum/reactioncontent/>`__ on GitHub
or `award emoji <https://docs.gitlab.com/ee/user/award_emojis.html>`__ on GitLab.
They are used by people to publicly express their feelings about review
comments, which provides feedback to comment authors and all other members.

There are 6 types of reactions on GitHub:

============  =============  =======  =====
 Name         Markdown       Unicode  Emoji
============  =============  =======  =====
 THUMBS_UP    ``:+1:``       U+1F44D  👍
 THUMBS_DOWN  ``:-1:``       U+1F44E  👎
 LAUGH        ``:smile:``    U+1F604  😄
 HOORAY       ``:tada:``     U+1F389  🎉
 CONFUSED     ``:confused``  U+1F615  😕
 HEART        ``:heart:``    U+FE0F   ❤️
============  =============  =======  =====

These reactions are reviews to reviews, thus we call them meta-reviews. To
encourage people to do meta-reviews, we build a meta-review system, which
collects reactions, analyze them, and use that information to improve our
review process and the quality of reviews. We give a score to people's
reviews based on reactions they receive. After scoring, a ranking list
is shown on coala community website.

At the moment, only THUMBS_UP and THUMBS_DOWN are collected and analyzed,
as they are most commonly used and express strong and clear feelings:
THUMBS_UP means the review comment is well-written and helpful, while
THUMBS_DOWN means the review comment is misleading, or even worse, violates
`coala Community Code of Conduct <https://github.com/coala/cEPs/blob/master/cEP-0006.md>`__.

.. note::

    Only GitHub is being analyzed at the moment. Support for GitLab will
    be available in the future.

Meta-review Process
-------------------

The meta-review process for coala is as follows:

1. Reviewers create their reviews.

2. Anyone, especially author of the pull request, can do meta-review (THUMBS_UP,
   THUMBS_DOWN) via reactions on GitHub.

3. Meta-review information will be collected and analyzed automatically:

   * Meta-reviewers will be given bonus points to encourage such behaviour.

   * Meta-reviewees will be given positive points (on receiving THUMBS_UP) or
     negative points (on receiving THUMBS_DOWN). Those points are weighted
     according to score of meta-reviewers. Those who have higher score in
     the meta-review system will have more impacts on others, so please do
     meta-reviews carefully.

.. note::

    Due to limitations on GitHub, review summary
    (`example <https://github.com/coala/coala-bears/pull/2517#pullrequestreview-125039346>`__)
    is not able to be meta-reviewed. If your review is not related to any
    particular line, leaving a comment
    (`example <https://github.com/coala/coala-bears/pull/2517#issuecomment-393678689>`__)
    is encouraged.

.. caution::

    Don't **edit** or **delete** your review after it has been meta-reviewed.
    If you do that, you are destroying feedback from the community. This
    is considered as an improper behaviour and a negative score will be
    given to you.

Automated Scoring Process
-------------------------

A complete ranking list can be found on
`Meta-review score ranking list <http://community.coala.io/meta-review/>`__.
Score is based on number of positive (THUMBS_UP) & negative (THUMBS_DOWN)
reactions one receives, and number of positive & negative reactions one gives
away. The formula can be found in
`cEP-0019.md <https://github.com/coala/cEPs/blob/master/cEP-0019.md#ranking-list>`__.
Calculation details can be found in
`meta_review/handler.py <https://github.com/coala/community/blob/master/meta_review/handler.py>`__.

.. note::

    The scoring process is automated, and will be polished from time to
    time. As a meta-reviewer, you don't need to care too much about the
    details of meta-review system. Just make sure you follow the meta-review
    process!

Iterative Weighting Factor
--------------------------

People receive marks when their reviews receive THUMBS_UP, while they lose
marks when their reviews receive THUMBS_DOWN. How many marks they get depends
on the weighting factor. Weighting factors are updated iteratively, everytime
when meta-review system runs. This section explains how the weight factor
is calculated.

The higher score a person has, the more impacts they have, thus their
meta-reviews are more valuable.

For example, in a previous iteration, Alice got 2 marks, Bob got
0.8 marks and Charlie got 10 marks. The calculation demo would
be as follows:

::

    >>> c = [2, 0.8, 10]
    >>> max_score = float(max(c))
    >>> result = [i / max_score for i in c]
    >>> print(result)
    [0.2, 0.08, 1.0]
    >>> result_adjust = [i * 0.9 + 0.1 for i in result]  # adjust
    >>> result_rounded = [round(i, 3) for i in result_adjust]
    >>> print(result_rounded)
    [0.28, 0.172, 1.0]

As the demo shows, weighting factors for Alice, Bob and Charlie will
be 0.28, 0.172, 1.0, respectively. This means Charlie has much more
voice than Alice and Bob. Marks you get from a THUMBS_UP given by
Charlie is almost equal to total marks from 6 separate THUMBS_UPs
given by Bob.

Anyone who gets negative marks from previous run will have weight
factor of 0.

To conclude, the weight factor is a float number ranging from 0 to 1.
