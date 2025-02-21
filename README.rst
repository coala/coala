.. image:: https://cloud.githubusercontent.com/assets/5716520/24838296/a9cf5f04-1d45-11e7-855c-47b816ce1e09.png
    :target: https://coala.io/

=====

:emphasis:`"Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live."` ― `John F. Woods <http://ruby.zigzo.com/2014/08/01/who-said-that-one-violent-psychopath-quote/>`_

=====

|Linux Build Status| |Windows Build status| |macOS Build Status|
|codecov.io| |Documentation Status| |AGPL| |OpenHub|

=====

coala: A Unified Linting and Fixing Tool for Multiple Languages
==============================================================

coala provides a **unified interface for linting and fixing code** across multiple programming languages with a **single configuration file**.
It helps developers maintain **consistent code quality** and **enforce coding standards** effortlessly.

With coala, you can:

- Run linters for multiple languages from a single tool.
- **Auto-fix** code issues with minimal manual effort.
- Use it in your **favorite editor**, integrate it into **CI/CD**, or run it via **CLI**.
- Get results in **JSON format** for further processing.
- Customize linting rules with **flexible configuration syntax**.

Why Use coala?
--------------

- **Language-Agnostic** – Works with **Python, C/C++, Java, JavaScript, CSS, Go, Rust**, and more.
- **One Configuration for All** – Define rules in a single `.coafile` instead of configuring multiple linters.
- **Editor & IDE Integration** – Compatible with **VS Code, Vim, Emacs, Sublime, Atom**, and others.
- **CI/CD Ready** – Easily integrate with **GitHub Actions, GitLab CI, Travis CI, Jenkins**, etc.
- **Customizable & Extensible** – Add custom bears (plugins) to define your own linting logic.
- **Active Community & Support** – Open-source, with an engaged community and active maintainers.

Installation
------------

Install coala using **pip**:

.. code-block:: bash

    pip install coala

Or install via **Docker**:

.. code-block:: bash

    docker pull coala/base

For detailed installation instructions, see the `Installation Guide <link-to-installation>`_.


Editor & CI Integrations
------------------------

**Editors & IDEs**

- `VS Code`_
- `Vim`_
- `Emacs`_
- `Sublime Text`_
- `Atom`_

**Continuous Integration (CI/CD)**

- `GitHub Actions`_
- `GitLab CI`_
- `Jenkins`_

Contributing
------------

We love contributions! If you want to help improve coala, check out our `Contribution Guide <https://github.com/coala/blob/master/CONTRIBUTING.rst>`_.

Ways to contribute:

- ✔ Report issues and suggest improvements.
- ✔ Fix bugs and add new features.
- ✔ Improve documentation.
- ✔ Help with community support and discussions.


License
-------

coala is released under the **GNU General Public License v3 (GPL-3.0)**. See the `LICENSE file <https://github.com/coala/blob/master/LICENSE>`_ for details.

Stay Connected
--------------
-  **Chat**: `Chat <https://coala.io/chat>`_
-  **Blog**: `Blog <http://blog.coala.io/>`_
-  **Twitter**: `Twitter <https://www.twitter.com/coala_io>`_
-  **Roadmap**: `Roadmap <https://projects.coala.io/>`_






.. |Linux Build Status| image:: https://img.shields.io/circleci/project/coala/coala/master.svg?label=linux%20build
   :target: https://circleci.com/gh/coala/coala
.. |Windows Build status| image:: https://img.shields.io/appveyor/ci/coala/coala/master.svg?label=windows%20build
   :target: https://ci.appveyor.com/project/coala/coala/branch/master
.. |macOS Build Status| image:: https://img.shields.io/travis/coala/coala/master.svg?label=macOS%20build
   :target: https://travis-ci.org/coala/coala
.. |codecov.io| image:: https://img.shields.io/codecov/c/github/coala/coala/master.svg?label=branch%20coverage
   :target: https://codecov.io/github/coala/coala?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/coala/badge/?version=latest
   :target: http://docs.coala.io/
.. |AGPL| image:: https://img.shields.io/pypi/l/coala.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
.. |OpenHub| image:: http://www.openhub.net/p/coala/widgets/project_thin_badge.gif
   :target: https://www.openhub.net/p/coala

