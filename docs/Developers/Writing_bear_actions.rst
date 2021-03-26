Writing bear specific actions
=============================

This tutorial aims to show you how to write actions which are specific
to some bears. It assumes that you know how to use coala and are familiar
with bears.

What are actions?
-----------------

An action is a way in which user interacts with coala and decides what to
do with analysis done by coala. Bears run some analysis and communicate with
the user via results, then some action needs to be taken on these results.

coala has provided some built-in default actions like:

-  ``DoNothingAction``: As the name suggests this action does nothing, you can
   choose this action when you want to ignore the result.
-  ``ShowPatchAction``: This action displays the changes in code suggested by
   the bear.
-  ``ApplyPatchAction``: This action automatically apply the changes suggested
   by coala.
-  ``IgnoreResultAction``: This message adds an ignore comment in the part
   where coala is suggesting changes so that next time you run coala, it will
   not suggest these changes.
-  ``ShowAppliedPatchesAction``: This action shows all the changes that have
   been applied by coala.

coala determines which actions from default actions are applicable to a result
and asks the user to choose one action to apply.

What are bear specific actions?
-------------------------------

There might be some instances when a bear might suggest some changes which are
not code related, for example ``GitCommitBear`` can find that there is no
newline between shortlog and body of the commit message. In such cases there is
no patch associated with the result and none of the default actions might be
applicable.
However it is possible to write an action which can add a newline between
shortlog and body of commit message, but this action will be specific to
GitCommitBear only.

You may come across a similar situation where writing an action specific to some
bear might be helpful to you.

Writing the action
------------------

To write a bear specific action we need to create a class that implements the
logic. This should preferably be defined in ``coala-bears`` repository in the
directory where the bear is defined.

.. code:: python

    from coalib.results.result_actions.ResultAction import ResultAction

    class SomeAction(ResultAction):

        SUCCESS_MESSAGE = 'Something done successfully.'

``ResultAction`` is used as a base class for all actions and provides a unified
interface for all actions.

``SUCCESS_MESSAGE`` is the message that will get printed once the action is
successfully applied.

Every action class should have these two methods:

1. ``is_applicable`` method:
   It has the logic which determines
   whether the action is applicable or not.

   .. code:: python

           @staticmethod
           def is_applicable(result,
                             original_file_dict,
                             file_diff_dict,
                             applied_actions=()):

   It must return a boolean value, ``True`` if action is applicable for a
   particular result, ``False`` otherwise.

   ``is_applicable`` method accepts four parameters:

   -  ``result``: The result for which we want to check if action is applicable
      or not.
   -  ``original_file_dict``: A dictionary whose key is the filename and value
      is the file in the state when result was generated.
   -  ``file_diff_dict``: A dictionary whose key is the filename and value
      is a diff of file from the state in the original_file_dict to
      the current state.
   -  ``applied_actions``: List of actions names that have already been applied
      for the current result.

   .. note::

       ``is_applicable`` doesn’t have to be a static method. In this case you
       also need to prepend ``self`` to the parameters in the signature.

2. ``apply`` method:
   It has the logic for when the action is applied.

   .. code:: python

           def apply(self,
                     result,
                     original_file_dict,
                     file_diff_dict,
                     **kwargs):
               """
               Apply (S)ome Action
               """

   apply method must return ``file_diff_dict``.

   Writing a docstring for ``apply`` method is very important. The contents of
   the docstring will get displayed to the user when asked to choose an action
   to apply. The letter in parentheses can be used by the user as a way of
   selecting this action.

Apart from this you can also add other helper methods and even an ``init``
method to the action class.

Passing bear action to the result
---------------------------------

After writing bear action you have to let coala know about this.
When a bear yields a result you can pass a list action instances for that
bear by using an optional argument ``actions``.

Suppose ``SomeAction`` is an action specific to ``SomeBear``

.. code:: python

    from path.to.SomeAction import SomeAction

    class SomeBear:

        def run():

            yield Result('origin', 'message', actions=[SomeAction()])

Example of EditCommitMessageAction
----------------------------------

We will look at an example of ``EditCommitMessageAction`` for
``GitCommitBear``. Whenever GitCommitBear suggests some changes in commit
message we can provide an action to the user, which on applying
will open up an editor where user can edit the commit message.

.. code:: python

    import subprocess
    from coalib.results.result_actions.ResultAction import ResultAction

    class EditCommitMessageAction(ResultAction):

        SUCCESS_MESSAGE = 'Commit message edited successfully.'

        def apply(self, result, original_file_dict, file_diff_dict):
            """
            Edit (C)ommit Message [Note: This may rewrite your commit history]
            """
            subprocess.check_call(['git', 'commit', '-o', '--amend'])
            return file_diff_dict

Note that ``is_applicable`` method is not implemented, that is because
``ResultAction`` already implements this and it always returns True which
is what we what want in this case.

``apply`` method spawns a simple process which runs a git command which will
open up an editor to edit the commit message.
