Guide to Writing a Native Bear
==============================

Welcome. This document presents information on how to write a bear for
coala. It assumes you know how to use coala. If not, please read our
`main tutorial`_

The sample sources for this tutorial lie at our coala-tutorial
repository, go clone it with:

::

    git clone https://github.com/coala/coala-tutorial

All paths and commands given here are meant to be executed from the root
directory of the coala-tutorial repository.

.. note::

    If you want to wrap an already existing tool, please refer to
    :doc:`this tutorial instead<Writing_Linter_Bears>`.

What is a bear?
---------------

A bear is meant to do some analysis on source code. The source code will
be provided by coala so the bear doesn't have to care where it comes from
or where it goes.

There are two kinds of bears:

- LocalBears, which only perform analysis on each file itself
- GlobalBears, which are project wide, like the GitCommitBear

A bear can communicate with the user via two ways:

-  Via log messages
-  Via results

Log messages will be logged according to the users settings and are
usually used if something goes wrong. However you can use debug for
providing development related debug information since it will not be
shown to the user by default. If error/failure messages are used, the
bear is expected not to continue analysis.

A Hello World Bear
------------------

Below is the code given for a simple bear that sends a debug message for
each file:

.. code:: python

    import logging

    from coalib.bears.LocalBear import LocalBear

    class HelloWorldBear(LocalBear):
        def run(self,
                filename,
                file):
            logging.debug("Hello World! Checking file {}.".format(filename))

This bear is stored at ``./bears/HelloWorldBear.py``

In order to let coala execute this bear you need to let coala know where
to find it. We can do that with the ``-d`` (``--bear-dirs``) argument:

``coala -f src/*.c -d bears -b HelloWorldBear -L DEBUG --flush-cache``

.. note::

    The given bear directories must not have any glob expressions in them. Any
    character that could be interpreted as a part of a glob expression will be
    escaped. Please use comma separated values to give several such
    directories instead. Do not forget to flush the cache (by adding the
    argument ``--flush-cache`` when running coala) if you run a new bear on a
    file which has been previously analyzed (by coala).

You should now see an output like this on your command line:

::

    [WARNING][15:07:39] Default coafile '.coafile' not found!
    Here's what you can do:
    * add `--save` to generate a config file with your current options
    * add `-I` to suppress any use of config files
    [DEBUG][15:07:39] Platform Linux -- Python 3.5.2, coalib
    0.12.0.dev20170626132008
    [DEBUG][15:07:39] The file cache was successfully flushed.
    [DEBUG][15:07:39] Files that will be checked:
    /home/LordVoldemort/programs/coa_dir/coala-tutorial/src/main.c
    [DEBUG][15:07:40] coala is run only on changed files, bears' log
    messages from previous runs may not appear. You may use the
    `--flush-cache` flag to see them.
    [DEBUG][15:07:40] Running bear HelloWorldBear...
    [DEBUG][15:07:40] Hello World! Checking file /home/LordVoldemort/
    programs/coa_dir/coala-tutorial/src/main.c .

    Notice that the last ``[DEBUG]`` message is what was coded in
    ``HelloWorldBear.py``. All the other messages are inherited from the
    ``LocalBear`` class or run by the code responsible for executing the
    bear.

.. note::

    The first ``WARNING`` message is because our directory, does not
    contain a ``.coafile``. If you have followed the instructions in
    our `main tutorial`_, you will have a ``.coafile`` in your working
    directory. Its best if you delete that file before working on this
    tutorial, else you will see a bunch of other outputs from other bears
    as well.

For more detail about Python's built-in ``logging`` facility,
see https://docs.python.org/3/library/logging.html.

Communicating with the User
---------------------------

Now we can send messages through the queue, we can do the real work.
Let's say:

-  We want some information from the user (e.g. the tab width if we rely
   on indentation).
-  We've got some useful information for the user and want to show it to
   them. There might be some issue with their code or just an information
   like the number of lines.

So let's extend our HelloWorldBear a bit, I've named the new bear with
the creative name CommunicationBear:

.. code:: python

    import logging

    from coalib.bears.LocalBear import LocalBear

    class CommunicationBear(LocalBear):

        def run(self,
                filename,
                file,
                user_input: str):
            """
            Communicates with the user.

            :param user_input: Arbitrary user input.
            """
            logging.debug("Got '{ui}' as user input of type {type}.".format(
                ui=user_input,
                type=type(user_input)))

            yield self.new_result(message="A hello world result.",
                                  file=filename)

Try executing it:

::

    coala -f=src/\*.c -d=bears -b=CommunicationBear -L=DEBUG --flush-cache

Hey, we'll get asked for the user\_input!

::

    [WARNING][15:20:18] Default coafile '.coafile' not found!
    Here's what you can do:
    * add `--save` to generate a config file with your current options
    * add `-I` to suppress any use of config files
    Please enter a value for the setting "user_input" (No description given.)
    needed by CommunicationBear for section "cli":

Wasn't that easy? Go ahead,
enter something and observe the output.

::

    Avada Kedavra
    [DEBUG][15:22:55] Platform Linux -- Python 3.5.2, coalib
    0.12.0.dev20170626132008
    [DEBUG][15:22:55] The file cache was successfully flushed.
    [DEBUG][15:22:55] Files that will be checked:
    /home/LordVoldemort/programs/coa_dir/coala-tutorial/src/main.c
    [DEBUG][15:22:55] coala is run only on changed files, bears' log messages
    from previous runs may not appear. You may use the `--flush-cache` flag to
    see them.
    [DEBUG][15:22:55] Running bear CommunicationBear...
    [DEBUG][15:22:55] Got 'Avada Kedavra' as user input of type <class 'str'>.

    **** CommunicationBear [Section: cli] ****

    !    ! [Severity: NORMAL]
    !    ! A hello world result.
    [    ] Do (N)othing
    [    ] (O)pen file
    [    ] Add (I)gnore comment
    [    ] Enter number (Ctrl-D to exit):

So, what did coala do here?

First, coala looked at the parameters of the run method and found that
we need some value named user\_input. Then it parsed our documentation
comment and found a description for the parameter which was shown to us
to help us choose the right value. After the needed values are provided,
coala converts the value into a string because we've provided the
``str`` annotation for this parameter. If no annotation is given or the
value isn't convertible into the desired data type, you will get a
``coalib.settings.Setting.Setting``.

Your docstring can also be used to tell the user what exactly your bear
does.

Try executing

::

    coala -d bears -b CommunicationBear --show-bears --show-description

This will show the user a bunch of information related to the bear like:
- A description of what the bear does - The sections which uses it - The
settings it uses (optional and required)

.. note::

    The bears are not yet installed. We still have to specify
    the bear directory using ``-d`` or ``--bear-dirs`` flag.


Install locally Written Bears
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say that we wrote a file NewBear.py that contain our NewBear and
we want to run it locally. To install our NewBear:

-  Move the ``NewBear.py`` to our clone of coala-bears in
   ``coala-bear/bears/<some_directory>``.

-  Update all bears from source with:

::

    pip3 install -U <path/to/coala-bears>

Our NewBear is installed.

Try Executing:

::

    coala --show-bears

This shows a list of all installed bears. We can find our NewBear in the list.

What Data Types are Supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Setting does support some very basic types:

-  String (``str``)
-  Float (``float``)
-  Int (``int``)
-  Boolean (``bool``, will accept values like ``true``, ``yes``,
   ``yeah``, ``no``, ``nope``, ``false``)
-  List of strings (``list``, values will be split by comma)
-  Dict of strings (``dict``, values will be split by comma and colon)

You can use shortcuts for basic types, ``str_list`` for strings,
``int_list`` for ints, ``float_list`` for floats and ``bool_list`` for
boolean values.

If you need another type, you can write the conversion function yourself
and use this function as the annotation (if you cannot convert value, be
sure to throw ``TypeError`` or ``ValueError``). We've provided a few
advanced conversions for you:

-  ``coalib.settings.Setting.path``, converts to an absolute file path
   relative to the file/command where the setting was set
-  ``coalib.settings.Setting.path_list``, converts to a list of absolute
   file paths relative to the file/command where the setting was set
-  ``coalib.settings.Setting.typed_list(typ)``, converts to a list and
   applies the given conversion (``typ``) to each element.
-  ``coalib.settings.Setting.typed_ordered_dict(key_type, value_type,
   default)``, converts to a dict while applying the ``key_type``
   conversion to all keys, the ``value_type`` conversion to all values
   and uses the ``default`` value for all unset keys. Use ``typed_dict``
   if the order is irrelevant for you.
-  ``coalib.settings.Setting.language``, converts into coala ``Language``
   object.

Results
-------

In the end we've got a result. If a file is provided, coala will show
the file, if a line is provided, coala will also show a few lines before
the affecting line. There are a few parameters to the Result
constructor, so you can e.g. create a result that proposes a code change
to the user. If the user likes it, coala will apply it automatically -
you don't need to care.

To propose a change Result class has a ``diffs`` parameter which accepts a
dictionary with key as a filename and value as a Diff object which is
basically the proposed changes in that file.
Bears also have the ability to suggest multiple changes for a single problem
and let user decide which change to make. For this along with ``diffs``
Result class also has an ``alternate_diffs`` parameter which accepts
a list of dictionaries where each element is an alternate change.

Your function needs to return an iterable of ``Result`` objects: that
means you can either return a ``list`` of ``Result`` objects or simply
yield them and write the method as a generator.

.. note::

    We are currently planning to simplify Bears for bear writers and us.
    In order to make your Bear future proof, we recommend writing your
    method in generator style.

    Don't worry: in order to migrate your Bears to our new API, you will
    likely only need to change two lines of code. For more information
    about how bears will look in the future, please read up on
    https://github.com/coala/coala/issues/725 or ask us on
    https://coala.io/chat.

Bears Depending on Other Bears
------------------------------

So we've got a result, but what if we need our Bear to depend on results from
a different Bear?

Well coala has an efficient dependency management system that would run the
other Bear before your Bear and get its results for you. All you need to do is
to tell coala which Bear(s) you want to run before your Bear.

So let's see how you could tell coala which Bears to run before yours:

.. code:: python

    from coalib.bears.LocalBear import LocalBear
    from bears.somePathTo.OtherBear import OtherBear

    class DependentBear(LocalBear):

        BEAR_DEPS = {OtherBear}

        def run(self, filename, file, dependency_results):
            results = dependency_results[OtherBear.name]


As you can see we have a `coalib.bears.Bear.Bear.BEAR_DEPS`
set which contains a list of bears we wish to depend on.
In this case it is a set with 1 item: "OtherBear".

.. note::
    The `BEAR_DEPS` set must have classes of the bear itself,
    not the name as a string.

coala gets the ``BEAR_DEPS`` before executing the ``DependentBear``
and runs all the Bears in there first.

After running these bears, coala gives all the results returned by the Bears
in the ``dependency_results`` dictionary, which has the Bear's name as a key
and a list of results as the value. E.g. in this case, we would have
``dependency_results ==
{'OtherBear' : [list containing results of OtherBear]]}``.

.. note::
    ``dependency_results`` is a keyword here and it cannot be called by
    any other name.

Hidden Results
--------------
Apart from regular Results, coala provides HiddenResults, which are used
to share data between Bears as well as giving results which are not shown to
the user. This feature is specifically for Bears that are dependencies of other
Bears, and do not want to return Results which would be displayed when the
bear is run.

Let's see how we can use HiddenResults in our Bear:

.. code:: python

    from coalib.bears.LocalBear import LocalBear
    from coalib.results.HiddenResult import HiddenResult

    class OtherBear(LocalBear):

        def run(self, filename, file):
            yield HiddenResult(self, ["Some Content", "Some Other Content"])

Here we see that this Bear (unlike normal Bears) yields a
`coalib.results.HiddenResult` instead of a ``Result``. The first
parameter in ``HiddenResult`` should be the instance of the Bear that yields
this result (in this case ``self``), and second argument should be the content
we want to transfer between the Bears. Here we use a list of strings as content
but it can be any object.

More Configuration Options
--------------------------

coala provides metadata to further configure your bear according to your needs.
Here is the list of all the metadata you can supply:

- `LANGUAGES`_
- `REQUIREMENTS`_
- `INCLUDE_LOCAL_FILES`_
- `CAN_DETECT and CAN_FIX`_
- `BEAR_DEPS`_
- `Other Metadata`_


LANGUAGES
~~~~~~~~~

To indicate which languages your bear supports, you need to give it a `set` of
strings as a value:

.. code:: python

    class SomeBear(Bear):
        LANGUAGES = {'C', 'CPP','C#', 'D'}

.. include:: ./Language_Naming_Format.rst

REQUIREMENTS
~~~~~~~~~~~~

To indicate the requirements of the bear, assign ``REQUIREMENTS`` a set with
instances of subclass of ``PackageRequirement`` such as:

- PipRequirement
- NpmRequirement
- CondaRequirement
- DistributionRequirement
- GemRequirement
- GoRequirement
- JuliaRequirement
- RscriptRequirement

.. code:: python

    class SomeBear(Bear):
        REQUIREMENTS = {
        PipRequirement('coala_decorators', '0.2.1')}

To specify multiple requirements you can use the multiple method.
This can receive both tuples of strings, in case you want a specific version,
or a simple string, in case you want the latest version to be specified.

.. code:: python

    class SomeBear(Bear):
        REQUIREMENTS = PipRequirement.multiple(
            ('colorama', '0.1'),
            'coala_decorators')

INCLUDE_LOCAL_FILES
~~~~~~~~~~~~~~~~~~~

If your bear needs to include local files, then specify it by giving strings
containing file paths, relative to the file containing the bear, to the
``INCLUDE_LOCAL_FILES``.

.. code:: python

    class SomeBear(Bear):
        INCLUDE_LOCAL_FILES = {'checkstyle.jar',
            'google_checks.xml'}

CAN_DETECT and CAN_FIX
~~~~~~~~~~~~~~~~~~~~~~

To easily keep track of what a bear can do, you can set the value of
`CAN_FIX` and `CAN_DETECT` sets.


.. code:: python

    class SomeBear(Bear):
        CAN_DETECT = {'Unused Code', 'Spelling'}

        CAN_FIX = {'Syntax', 'Formatting'}


To view a full list of possible values, check this list:

- `Syntax`
- `Formatting`
- `Security`
- `Complexity`
- `Smell`
- `Unused Code`
- `Redundancy`
- `Variable Misuse`
- `Spelling`
- `Memory Leak`
- `Documentation`
- `Duplication`
- `Commented Code`
- `Grammar`
- `Missing Import`
- `Unreachable Code`
- `Undefined Element`
- `Code Simplification`

Specifying something to `CAN_FIX` makes it obvious that it can be detected too,
so it may be omitted from `CAN_DETECT`

BEAR_DEPS
~~~~~~~~~

``BEAR_DEPS`` contains bear classes that are to be executed before this bear
gets executed. The results of these bears will then be passed to the run method
as a dict via the `dependency_results` argument. The dict will have the name of
the Bear as key and the list of its results as value:

.. code:: python

    class SomeOtherBear(Bear):
        BEAR_DEPS = {SomeBear}

For more detail see `Bears Depending on Other Bears`_.

Other Metadata
~~~~~~~~~~~~~~

Other metadata such as ``AUTHORS``, ``AUTHORS_EMAILS``, ``MAINTAINERS``,
``MAINTAINERS_EMAILS``, ``LICENSE``, ``ASCIINEMA_URL``, ``SEE_MORE``
can be used as follows:

.. code:: python

    class SomeBear(Bear):
        AUTHORS = {'Jon Snow'}
        AUTHORS_EMAILS = {'jon_snow@gmail.com'}
        MAINTAINERS = {'Catelyn Stark'}
        MAINTAINERS_EMAILS = {'catelyn_stark@gmail.com'}
        LICENSE = 'AGPL-3.0'
        ASCIINEMA_URL = 'https://asciinema.org/a/80761'
        SEE_MORE = 'https://www.pylint.org'

Aspect Bear
-----------

Aspect is a feature in coala that make configuring coala in project more easy
and language agnostic. For more detail about aspect, see cEP-0005 in
https://github.com/coala/cEPs/blob/master/cEP-0005.md.

An aspect-compliant bear MUST:

1. Declare list of aspect it can fix and detected. Note that the aspect MUST be
   a leaf aspect. You can see list of supported aspect here
   https://github.com/coala/aspect-docs.
2. Declare list of supported language. See list of supported language
   https://github.com/coala/coala/tree/master/coalib/bearlib/languages/definitions.
3. Map setting to its equivalent aspect or taste using ``map_setting_to_aspect``
   decorator.
4. Yield result with relevant aspect.

For example, let's make an aspect bear named SpellingCheckBear.

.. code:: python

    from coalib.bearlib.aspects import map_setting_to_aspect
    from coalib.bearlib.aspects.Spelling import (
        DictionarySpelling,
        OrgSpecificWordSpelling,
    )
    from coalib.bears.LocalBear import LocalBear


    class SpellingCheckBear(
            LocalBear,
            aspect={
                'detect': [
                    DictionarySpelling,
                    OrgSpecificWordSpelling,
                ],
            },
            languages=['Python']):

        @map_setting_to_aspect(
            use_standard_dictionary=DictionarySpelling,
            additional_dictionary_words=OrgSpecificWordSpelling.specific_word,
        )
        def run(self,
                filename,
                file,
                use_standard_dictionary: bool=True,
                additional_dictionary_words: list=None):
            """
            Detect wrong spelling.

            :param use_standard_dictionary:     Use standard English dictionary.
            :param additional_dictionary_words: Additional list of word.
            """
            if use_standard_dictionary:
                # Imagine this is where we save our standard dictionary.
                dictionary_words = ['lorem', 'ipsum']
            else:
                dictionary_words = []
            if additional_dictionary_words:
                dictionary_words += additional_dictionary_words

            for word in file.split():
                if word not in dictionary_words:
                    yield self.new_result(
                        message='Wrong spelling in word `{}`'.format(word),
                        aspect=DictionarySpelling('py'),
                    )

.. _main tutorial: https://docs.coala.io/en/latest/Users/Tutorial.html
