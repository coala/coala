.. coala documentation master file, created by
   sphinx-quickstart on Wed Feb  3 16:49:01 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. meta::
   :description: coala is a simple COde AnaLysis Application. Its goal is
                 to make static code analysis easy while remaining completely
                 modular and therefore extendable and language independent.
   :keywords:    coala, code analysis, static code analysis, linter,
                 language agnostic, python3, linux, unix, windows, bears,
                 coala-bears

Welcome to the coala documentation!
===================================

.. toctree::
   :caption: Home
   :hidden:

   Welcome <self>

.. toctree::
   :caption: For Users
   :hidden:

   Installation <Users/Install>
   coafile Specification <Users/coafile>
   Glob Patterns <Users/Glob_Patterns>
   Exit Codes <Users/Exit_Codes>
   External APIs <Users/External_APIs>
   Git Hooks <Users/Git_Hooks>

.. toctree::
   :caption: Tutorials
   :hidden:

   First Step <Users/Tutorials/Tutorial>
   Writing Bears <Users/Tutorials/Writing_Bears>
   Testing Bears <Users/Tutorials/Testing_Bears>
   Linter Bears <Users/Tutorials/Linter_Bears>
   Linter Bears - Suggest corrections <Users/Tutorials/Self_Correcting_Bears>
   Git Help <Users/Tutorials/Git_Help>
   Auto completion <Users/Tutorials/Auto_Completion>

.. toctree::
   :caption: Getting Involved
   :hidden:

   Newcomers <Getting_Involved/Newcomers>
   Introduction <Getting_Involved/README>
   Codestyle <Getting_Involved/Codestyle>
   Commit Style <Getting_Involved/Writing_Good_Commits>
   Executing Tests <Getting_Involved/Testing>
   Review <Getting_Involved/Review>
   Writing Tests <Getting_Involved/Writing_Tests>
   Writing Documentation <Getting_Involved/Writing_Documentation>
   MAC Hints <Getting_Involved/MAC_Hints>

.. toctree::
   :caption: General Developer Information
   :hidden:

   A Hitchhiker's Guide to Git (1): Genesis <General_Dev_Info/git_tutorial_1>

.. toctree::
   :caption: API Documentation
   :hidden:

   List of Modules<API/modules>

.. Start ignoring LineLengthBear

::

                                                         .o88Oo._
                                                        d8P         .ooOO8bo._
                                                        88                  '*Y8bo.
                                          __            YA                      '*Y8b   __
                                        ,dPYb,           YA                        68o68**8Oo.
                                        IP'`Yb            "8D                       *"'    "Y8o
                                        I8  8I             Y8     'YB                       .8D
                                        I8  8P             '8               d8'             8D
                                        I8  8'              8       d8888b          d      AY
         ,gggo,    ,ggggo,    ,gggo,gg  I8 dP    ,gggo,gg   Y,     d888888         d'  _.oP"
        dP"  "Yb  dP"  "Y8go*8P"  "Y8I  I8dP    dP"  "Y8I    q.    Y8888P'        d8
       i8'       i8'    ,8P i8'    ,8I  I8P    i8'    ,8I     "q.  `Y88P'       d8"
      ,d8,_    _,d8,   ,d8' d8,   ,d8b,,d8b,_ ,d8,   ,d8b,       Y           ,o8P
    ooP""Y8888PP*"Y8888P"   "Y8888P"`Y88P'"Y88P"Y8888P"`Y8            oooo888P"

.. Stop ignoring LineLengthBear

What is coala?
--------------

coala is a simple COde AnaLysis Application. Its goal is to make static
code analysis easy while remaining completely modular and therefore
extendable and language independent. coala is written with a lower case
"c".

Code analysis happens in python scripts while coala manages these, tries
to provide helpful libraries and provides multiple user interfaces.
(Currently we support only Console output but others will follow.)

One could say coala unites all language independent parts of a linter
and is arbitrarily extensible.

To get started, take a look at our :doc:`Installation
Instructions <Users/Install>` and the
:doc:`Tutorial <Users/Tutorials/Tutorial>`.

What do I get?
--------------

As a User
~~~~~~~~~

coala allows you to simply check your code against certain quality
requirements. The checking routines are named **Bears** in coala. You
can easily define a simple project file to check your project with all
bears either shipped with coala or ones you found in the internet and
trust.

As a Developer
~~~~~~~~~~~~~~

If you are not satisfied with the functionality given by the bears we
provide, you can easily write own bears. coala is written with easiness
of extension in mind. That means: no big boilerplate, just write one
small object with one routine, add the parameters you like and see how
coala automates the organization of settings, user interaction and
execution parallelization. You shouldn't need to care about anything
else than just writing your algorithm!

See :doc:`Writing Bears <Users/Tutorials/Writing_Bears>` for more information on
this.

Also, coala provides an external API using the dbus message protocol.
This allows other applications to easily use the code analysis
functionalities coala provides in their applications.

See :doc:`External APIs <Users/External_APIs>` for more information.

Status and Stability of the Project
-----------------------------------

We are currently working hard to make this project reality. coala is currently
usable, in beta stage and already provides more features than most
language dependent alternatives. Every single commit is fully reviewed and
checked with various automated methods including our testsuite covering all
branches. Our master branch is continuously prereleased to our users so you can
rely on the upcoming release being rock stable.

If you want to see how the development progresses, check out

https://github.com/coala-analyzer/coala

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
