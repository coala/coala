The .coafile Specification
==========================

This document gives a short introduction into the specification of a
*coala* configuration file. It is meant to be rather factual, if you wish
to learn by example, please take a look at the :doc:`Tutorials/Tutorial`.

Naming, Scope and Location
--------------------------

You can use up to three coafiles to configure your project.

1. A project-wide coafile.
2. A user-wide coafile.
3. A system-wide coafile.

Project-Wide coafile
~~~~~~~~~~~~~~~~~~~~

It is a convention that the project-wide coafile is named ``.coafile``
and lies in the project root directory. If you follow this convention,
simply executing ``coala`` from the project root will execute the
configuration specified in that file.

Settings given in the project-wide coafile override all settings given
by other files and can only be overridden by settings given via the
command line interface.

User-Wide and System-Wide coafile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can place a ``.coarc`` file in your home directory to set certain
settings user wide. Those settings will automatically be taken for all
projects executed with that user.

All settings specified here override only settings given by the system
wide coafile which has the lowest priority. The ``default_coafile`` must
lie in the *coala* installation directory and is valid for everyone using
this *coala* installation.

Setting Inheritance
-------------------

Every coafile consists out of one or more sections. Section names are
case insensitive. The ``default`` section is implicitly available and
all settings which have no section specified belong to it. The
``default`` section is special because all settings residing in it are
automatically inherited to all other sections specified in the same
coafile.

This is an example coafile:

::

    enabled = True
    overridable = 2

    [section-1]
    overridable = 3
    other = 4

    [section-2]
    overridable = 5
    other = 2

This coafile would be interpreted the very same as this one, written a
bit more explicitly:

::

    [default]
    enabled = True
    overridable = 2

    [section-1]
    enabled = True
    overridable = 3
    other = 4

    [section-2]
    enabled = True
    overridable = 5
    other = 2

Comments, Escaping and Multiline Values and Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comments are simply done with a preceding ``#``. If you want to use a
``#`` within a value, you can simply escape it:

::

    a_key = a\#value # And a comment at the end!

Any line not containing an unescaped ``=`` is simply appended to the
value of the last key:

::

    a_key = a
    value
    # this is not part of the value
    that /= is
    very long!

Similarly, you can also set a value to multiple keys:
``key_1, key_2 = value`` is equivalent to ``key_1 = value`` and
``key_2 = value`` in separate lines.

As the backslash is the escape character it is recommended to use
forward slashes as path seperator even on windows (to keep relative
paths platform independent), use double-backslashes if you really mean a
backslash in all places.
