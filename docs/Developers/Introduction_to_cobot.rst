Introduction to cobot
=====================

cobot is a chat bot built on the Hubot framework used at `our chatroom <https://coala.io/chat>`_.
You can do stuff like:

- **Invite people to your GitHub organization**

  It allows maintainers to invite users to `our organisation <https://github.com/coala>`_.
  If you're a maintainer, you can invite a user by giving the following command:
  ::

    cobot (invite|inv) <username> [to [team]]

- **File issues right from the Gitter Chat**

  It allows a member to create new issues by giving the following command:
  ::

    cobot new issue New issue heading here

- **Perform computations with Wolfram alpha**

  It searches Wolfram Alpha for the answer to the question.
  To search a question on Wolfram Alpha via cobot, type:
  ::

    cobot <wa|wolfram> <question>

- **Assign an issue to a user**

  It allow maintainers to assign an issue to a user.
  If you are a maintainer, you can assign an issue by typing :
  ::

    cobot assign <issue_link>

- **Provide information on a topic**

  It returns the information we have on your topic.
  ::

    cobot explain <topic>

- **Displays all the help commands that cobot knows about**

  It returns a set of commands that cobot understands.
  ::

    cobot help

  .. note::
      If you want to ask for a query, type:
      ::

        cobot help <query>

- **Google things for you**

  It searches your query on `Google` for you.
  To `google` anything, type:
  ::

    cobot lmgtfy <term>

- **Motivates you**

  It displays a motivation squirrel
  ::

    ship it

- **Check if your project name is spelled correctly**

  Last but not the least, it checks if the project name is typed correctly.
  In our case, if you mis-spell `coala`, it responds with:
  ::

    coala is always written with a lower case c


-----

================
More about cobot
================

You can check out the complete project `here <https://gitlab.com/coala/cobot>`_ .

In case if you find any issue, feel free to report it out
`here <https://gitlab.com/coala/cobot/issues>`__.

