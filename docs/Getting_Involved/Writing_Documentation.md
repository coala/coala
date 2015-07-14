# Writing Documentation

This document gives a short introduction on how to write documentation for
the coala project.

Documentation is written in Markdown and rendered by readthedocs.org to our
lovely users. You can view the current documentation on
<http://coala.rtfd.org>.

After getting the coala source code (see
[Installation Instructions](../Users/Install.md)), you can start hacking
on existent documentation files. They reside in the `docs` directory and are
written in markdown.

If you want to add new pages, you need to alter the `mkdocs.yml` file in the
coala root directory. Please read
<http://www.mkdocs.org/user-guide/writing-your-docs/#multilevel-documentation>
for an explanation of the syntax.

You can test the documentation locally through simply running `mkdocs serve`
in the coala root directory. (Use `pip install mkdocs` if you do not have
`mkdocs` yet.)
