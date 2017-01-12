Writing Documentation
=====================

This document gives a short introduction on how to write documentation
for the coala project.

Documentation is written in reStructuredText and rendered by `Read the Docs
<https://readthedocs.io>`_ to our lovely users.
You can view the current user documentation on http://docs.coala.io.

To familiarize yourself with the reStructuredText syntax please see this
`guide <http://www.sphinx-doc.org/en/latest/rest.html>`_.

After getting the coala source code (see `Installation
Instructions`_), you can start hacking on
existent documentation files. They reside in a separate repository
that can be found `here <https://github.com/coala/documentation>`_.

If you want to add new pages, you need to alter the ``index.rst`` file
in the root of the repository. Please read
http://www.sphinx-doc.org/en/stable/markup/toctree.html#toctree-directive
for an explanation of the syntax.

You should run this command before trying to build the documentation:

::

  pip3 install -r docs-requirements.txt

You can test the documentation locally through simply running
``make html`` in the root directory. This generates
``_build\html\index.html`` that you can view on your browser.


.. _Installation Instructions: https://docs.coala.io/en/latest/Users/Install.html
