Git Hooks
=========

This document is a guide on how to add *coala* as a git hook. Using git hooks
*coala* can be executed automatically, ensuring your code follows your quality
requirements.

Pre Commit Hooks
----------------

The pre-commit hook can be used to run *coala* before every commit action.
Hence, this does not allow any code not following the quality standars
specified unless it's done by force.

To enable this, just create the file ``.git/hooks/pre-commit`` under your
repository and add the lines:

.. code:: bash

    $ #!/bin/sh
    $ set -e
    $ coala

You can also specify arguments like ``-S autoapply=false`` which tells
*coala* to not apply any patch by itself. Or you can run specific sections with
``coala <section_name>``.

.. seealso::

    Module :doc:`Tutorial for Users <Tutorials/Tutorial>`
        Documentation on how to run *coala* which introduces the CLI arguments.

    Module :doc:`coafile Specification <coafile>`
        Documentation on how to configure *coala* using the coafile
        specification.

.. note::

    If you allow *coala* to auto apply patches, it's recommended to add
    `*.orig` to your .gitignore. *coala* creates these files while applying
    patches and they could be erroneously added to your commit.

This file needs to be executable. If it is not (or if you aren't sure), you
can make it executable by:

.. code:: bash

    $ chmod +x .git/hooks/pre-commit

and you’re done! It will run every time before you commit, and prevent
you from committing if the code has any errors.
