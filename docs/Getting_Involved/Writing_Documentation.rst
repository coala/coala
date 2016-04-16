Writing Documentation
=====================

This document gives a short introduction on how to write documentation
for the *coala* project.

Documentation is written in reStructuredText and rendered by readthedocs.org to
our lovely users. You can view the current documentation on
http://coala.rtfd.org.

After getting the *coala* source code (see :doc:`Installation
Instructions <../Users/Install>`), you can start hacking on
existent documentation files. They reside in the ``docs`` directory and
are written in reStructuredText.

If you want to add new pages, you need to alter the ``index.rst`` file
in the *coala* ``docs`` directory. Please read
http://www.sphinx-doc.org/en/stable/markup/toctree.html#toctree-directive
for an explanation of the syntax.

You can test the documentation locally through simply running
``make html`` in the *coala* ``docs`` directory. This generates
``docs\_build\html\index.html`` that you can view on your browser. (Use
``pip3 install sphinx`` if you do not have ``sphinx`` yet.)
