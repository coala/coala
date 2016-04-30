Auto completion
===============

If you're using bash or zsh you can setup them to have coala auto command
completion.

Bash
----

You have to install ``argcomplete``

::

    $ pip install argcomplete

After this you have to either activate it
`globally <https://github.com/kislyuk/argcomplete#activating-global-completion>`__
or add

::

    eval "$(register-python-argcomplete `which coala`)"

to your ``.bashrc``. Just make sure that coala is added to the path at that
point. If you want, or you are unsure if coala is in the PATH, you can expand
``\`which coala\``` to the path of your coala executable (you can find where it
is by running ``which coala``.

Zsh
---

You have to take the same steps as with bash (only add setting to your
``.zshrc`` instead of ``.bashrc``). Also, add to your ``.zshrc``:

::

    autoload bashcompinit
    bashcompinit
